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
    WordCloudText,
    StopWord,
    WordCloudWord,
    NamedEntity,
)


class WordCloudTextAdmin(admin.ModelAdmin):
    """
        Word Cloud Text add/change admin panel
    """

    list_display = [
        'name',
        'entity'
    ]


class WordCloudWordAdmin(admin.ModelAdmin):
    """
        Word Cloud Word add/change admin panel
    """

    list_display = [
        'word',
        'text',
        'entity',
    ]


admin.site.register(WordCloudText, WordCloudTextAdmin)
admin.site.register(StopWord)
admin.site.register(NamedEntity)
admin.site.register(WordCloudWord, WordCloudWordAdmin)
