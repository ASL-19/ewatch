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


from django.contrib import admin
from models import (
    Category,
    Post,
    Comment,
)


class PostAdmin(admin.ModelAdmin):
    """
        Post add/change panel
    """

    list_display = (
        'title',
        'category',
        'status',
        'homepage_feature'
    )


class CommentAdmin(admin.ModelAdmin):
    """
        Comment change panel
    """

    list_display = (
        'approved',
        'name',
        'title'
    )

    def has_add_permission(self, request):
        """
            Remove the ability to add to comments for admin
        """

        return False


class CategoryAdmin(admin.ModelAdmin):
    """
        Category add/change panel
    """

    list_display = (
        'admin_thumbnail',
        'name',
    )

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
