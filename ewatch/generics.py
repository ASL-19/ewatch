# -*- coding: utf-8 -*-
# Election Watch - To enable responsive governance and informed engagement with presidential elections
#
# Copyright (C) 2016  ASL19
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.shortcuts import get_object_or_404
from ckeditor_uploader.fields import RichTextUploadingField
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.renderers import (
    JSONRenderer,
    BrowsableAPIRenderer
)
from rest_framework import (
    viewsets,
    permissions,
    status,
)


###################################################
# Models
###################################################


class OrderedMixin(models.Model):
    """
        A mixin to add order to a model
    """

    order = models.PositiveIntegerField(
        verbose_name=_('Order'),
        unique=True,
        null=True,
        blank=True)

    class Meta:

        abstract = True
        ordering = ('order', )


class SearchableQuerySet(models.QuerySet):
    """
        A class to provide a QuerySet that helps with searching

        It provides a text_search filter to search records based on trigram similarity
    """

    def text_search(self, keyword, min_sim=0.1, related_list=[], fields_list=[]):
        """
            A method to search records based on trigram similarity.

            By default the method searches in title, content and tag columns

            Args:
            keyword: the keyword to search for (string)
            min_sim: minimum simliarity value to select records (float)
                default to 0.1
            related_list: list of related field to search beside title, content and tag (list of strings)
        """

        # Create a similarity tuple to extract similar records
        sim_tuple = (
            TrigramSimilarity('title', keyword),
            TrigramSimilarity('content', keyword),
            TrigramSimilarity('tag', keyword))

        for fld in fields_list:
            sim_tuple += (TrigramSimilarity(fld, keyword),)

        for rel in related_list:
            sim_tuple += (
                TrigramSimilarity(rel + '__title', keyword),
                TrigramSimilarity(rel + '__content', keyword),
                TrigramSimilarity(rel + '__tag', keyword))

        return self.annotate(similarity=Greatest(*sim_tuple)) \
            .filter(similarity__gt=min_sim) \
            .order_by('-similarity')

    def tag_search(self, keyword, min_sim=0.1, tag_fields=[]):
        """
            A method to search records based on trigram similarity.

            By default the method searches in title, content and tag columns

            Args:
            keyword: the keyword to search for (string)
            min_sim: minimum simliarity value to select records (float)
                default to 0.1
            related_list: list of related field to search beside title, content and tag (list of strings)
        """

        sim_tuple = (0,)

        # Create a similarity tuple to extract similar records
        for fld in tag_fields:
            sim_tuple += (TrigramSimilarity(fld, keyword),)

        return self.annotate(similarity=Greatest(*sim_tuple)) \
            .filter(similarity__gt=min_sim) \
            .order_by('-similarity')


class SearchableModel(models.Model):
    """
        An abstract class to present classes that needs to be searchable

        The class has three default properties that are needed for a
        model to be searchable. It also uses the SearchableQuerySet
        as its objects manager.
    """

    last_modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Modified Time'))
    title = models.CharField(
        max_length=256,
        verbose_name=_('Title'))
    content = RichTextUploadingField(
        null=True,
        blank=True,
        verbose_name=_('Content'))
    tag = models.TextField(
        max_length=8192,
        null=True,
        blank=True,
        verbose_name=_('Tags'))

    objects = SearchableQuerySet.as_manager()

    @property
    def objtype(self):
        """
            In order to identify different search outputs, objtype
            has to be defined in each inherited classes

            Returns:
            A string containing the object type for the search
        """

        pass

    class Meta:

        abstract = True


###################################################
# Views
###################################################


class SecureJSONRenderer(JSONRenderer):

    charset = 'utf-8'


@method_decorator(cache_page(60 * 15), name='dispatch')
class ReadOnlyViewSet(viewsets.GenericViewSet):
    """
        A base ViewSet to be used for different models.

        This class defines the list, and retrieve method, for GET
        requests.

        The class is read-only, in a sense that it does not provide
        any write method like PUT, DELETE and POST.
    """

    # filter_func defines the function to be used for searching.
    filter_func = None
    renderer_classes = (BrowsableAPIRenderer, SecureJSONRenderer)

    def is_search_defined(self):
        """
            This method defines if an object is searchable or not.

            Returns:
            True if object is searchable, False otherwise.
        """

        if self.filter_func is None:
            return False

        search_func = getattr(self.queryset, self.filter_func, None)
        if callable(search_func):
            return True

        return False

    def list(self, request, *args, **kwargs):
        """
            List method to return response to GET requests for /

            It checks for 'q' parameters in query params for trigram search.

            Args:
            request: The request object from client
            *args, **kwargs: Extra arguments passed into the function

            Returns:
            Paginated response object containing the result of the request.
        """

        if self.is_search_defined():
            keyword = self.request.query_params.get('q', None)
            if keyword is None:
                data = self.queryset
            else:
                data = self.queryset.text_search(keyword)
        else:
            data = self.queryset

        page = self.paginate_queryset(data)
        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(
            data,
            many=True,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)

    def retrieve(self, request, version, pk=None, slug=None):
        """
            Retrieve method to return response to GET request for a
            specific pk or in case of blog/post a slug.

            Args:
            request: The request object from client
            version: The API version
            pk: The primary key of the object to return, the default is None.

            Returns:
            Response object containing the result of the request.
        """

        if version not in api_settings.ALLOWED_VERSIONS:
            return Response(status=status.HTTP_501_NOT_IMPLEMENTED)

        if pk is None and slug is not None:
            data = get_object_or_404(self.queryset, slug=slug)
        else:
            data = get_object_or_404(self.queryset, pk=pk)

        serializer = self.get_serializer(
            data,
            context={'request': request})
        resp_data = serializer.data
        return Response(resp_data)


class OnlyLoggedInCreate(permissions.BasePermission):
    """
        Define a permission class to allow only authenticated
        users to add/change.
    """

    def has_permission(self, request, view):
        """
            Let only logged in authenticated user to create
            (POST) to the View

            Args:
            request: Request object
            view: View object for the permission

            Returns:
            True if permitted, False otherwise
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' and request.user and request.user.is_authenticated():
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
            Allow admin user to have permission over the object.

            Args:
            request: Request object
            view: View object for permission
            obj: Object for the permission

            Returns:
            True if permitted, False otherwise.
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user:
            return False

        return request.user.is_staff
