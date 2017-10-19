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


from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from models import (
    Category,
    Post,
    Comment,
)


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
        Blog category deserializer
    """

    class Meta:

        model = Category
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'name',
            'logo')


class GroupSerializer(serializers.ModelSerializer):
    """
        Blog Users Group serializer
    """

    class Meta:

        model = Group
        fields = (
            'name',)


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    """
        Blog Users deserializer
    """

    groups = GroupSerializer(many=True)

    class Meta:

        model = get_user_model()
        fields = (
            'id',
            'url',
            'first_name',
            'last_name',
            'groups')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
        Blog posts deserializer
    """

    author = AuthorSerializer()
    candidate_tag = serializers.StringRelatedField(many=True, read_only=True)
    published_date = serializers.SerializerMethodField()

    def get_published_date(self, obj):

        return unicode(obj.published_date)

    class Meta:

        model = Post
        depth = 1
        lookup_field = 'slug'
        fields = (
            'id',
            'url',
            'last_modified_date',
            'published_date',
            'title',
            'content',
            'tag',
            'category',
            'summary',
            'slug',
            'author',
            'status',
            'comment_allowed',
            'homepage_feature',
            'feature_image',
            'feature_image_caption',
            'candidate_tag')
        extra_kwargs = {
            'url': {
                'lookup_field': 'slug'
            }
        }


class PostSearchSerializer(serializers.HyperlinkedModelSerializer):
    """
        Blog posts deserializer
    """

    author = AuthorSerializer()
    similarity = serializers.DecimalField(max_digits=6, decimal_places=3)
    published_date = serializers.SerializerMethodField()

    def get_published_date(self, obj):

        return unicode(obj.published_date)

    class Meta:

        model = Post
        depth = 1
        fields = (
            'id',
            'url',
            'last_modified_date',
            'similarity',
            'published_date',
            'title',
            'content',
            'tag',
            'category',
            'summary',
            'slug',
            'author',
            'status',
            'comment_allowed',
            'homepage_feature',
            'feature_image',
            'feature_image_caption',
            'candidate_tag')


class CommentSerializer(serializers.ModelSerializer):
    """
        Post comments deserializer
    """

    post = serializers.HyperlinkedRelatedField(queryset=Post.objects.all(), view_name='post-detail', lookup_field='slug')
    comment_date = serializers.SerializerMethodField()

    def get_comment_date(self, obj):

        return unicode(obj.comment_date)

    class Meta:

        model = Comment
        depth = 1
        fields = (
            'id',
            'comment_date',
            'email',
            'name',
            'title',
            'content',
            'approved',
            'post')
