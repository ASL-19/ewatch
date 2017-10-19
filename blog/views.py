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


from django.contrib.auth import get_user_model
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.urls import reverse
from rest_framework import mixins
from ewatch.generics import ReadOnlyViewSet
from serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
    AuthorSerializer,
)
from models import (
    Category,
    Post,
    Comment,
)


class LatestPostFeedGen(Rss201rev2Feed):

    def rss_attributes(self):
        """
            Define RSS attributes based on Django feedgenerator
            and yahoo.com mrss standard
        """

        attrs = super(LatestPostFeedGen, self).rss_attributes()
        attrs['xmlns:media'] = 'http://search.yahoo.com/mrss/'

        return attrs

    def add_item_elements(self, handler, item):
        """
            Override item elements to support url and media
            description
        """

        super(LatestPostFeedGen, self).add_item_elements(handler, item)

        if 'content_url' in item:
            content = dict(url=item['content_url'])
            handler.addQuickElement(u'media:content', '', content)

        if 'media:description' in item:
            handler.addQuickElement(u'media:description', item['description'])


class LatestPostsFeed(Feed):
    """
        RSS feed for latest feeds
    """

    feed_type = LatestPostFeedGen
    title = 'Yekray'
    link = '/posts/rss'
    description = 'Latest posts on Yekray'

    def items(self):
        """
            feed items

            Returns:
            The 10 latest published posts ordered by published date
        """

        return Post.objects.filter(status='p').order_by('-published_date')[:10]

    def item_title(self, item):
        """
            feed item title

            Returns:
            The title of the post for each item
        """

        return item.title

    def item_description(self, item):
        """
            feed item description

            Returns:
            The summary of the post for each item
        """

        return item.summary

    def item_link(self, item):
        """
            feed item link

            Returns:
            URL to a post for each item
        """

        return item.get_post_link() 

    def item_pubdate(self, item):
        """
            feed item published date

            Returns:
            item's published date for each post
        """

        return item.published_date

    def item_author(self, item):
        """
            feed item's author

            Returns:
            item's author for each post
        """

        return item.author

    def item_categories(self, item):
        """
            feed item category

            Returns:
            item's category name for each post
        """

        return [str(item.category)]

    def item_extra_kwargs(self, obj):
        """
            feed item extra information that we
            added: content_url and media:description

            Returns:
            A dictionary containing content_url pointing to image URL
            and the descripton containing the image caption
        """

        if isinstance(obj, Post):
            item = obj
        else:
            return {}

        extra = {
            u'content_url': item.feature_image.url,
            u'media:description': item.feature_image_caption,
        }

        return extra


class CategoryViewSet(ReadOnlyViewSet):
    """
        View Blog Categories
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(ReadOnlyViewSet):
    """
        View Blog Posts
    """

    queryset = Post.objects.filter(status='p').order_by('-published_date').all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_func = 'text_search'

    def queyset(self):
        """
            Override queryset to only include the published
            posts and add a filter for featured posts

            Returns:
            A queryset of published posts
        """

        queryset = Post.objects.filter(status='p').all()
        featured = self.request.query_params.get('featured', None)
        if featured is not None and featured.lower() == 'true':
            queryset = queryset.filter(homepage_feature=True)

        return queryset


class CommentViewSet(ReadOnlyViewSet, mixins.CreateModelMixin):
    """
        View Blog Comments
    """

    serializer_class = CommentSerializer

    @property
    def queryset(self):
        """
            Modifies the default QuerySet to include filters for
            narrowing down the data.

            It checks for the following parameters in the query params:
            'approved' to return either approved or not approved comments
            'postid' to return comments only for a post

            Returns:
            A QuerySet filtered by provided parameters in query parameters.
        """

        queryset = Comment.objects

        # No approved, return all
        approved = self.request.query_params.get('approved', None)
        if approved is not None:
            if approved.lower() == 'true':
                queryset = queryset.filter(approved=True)
            elif approved.lower() == 'false':
                queryset = queryset.filter(approved=False)

        postslug = self.request.query_params.get('post', None)
        if postslug is None:
            return queryset.none()
        else:
            queryset = queryset.filter(post__slug=postslug)
            return queryset.all()

        # Wrong postid return none
        return queryset.none()


class AuthorViewSet(ReadOnlyViewSet):
    """
        View Blog Authors
    """

    queryset = get_user_model().objects.all()
    serializer_class = AuthorSerializer
