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


from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from blog.views import (
    CategoryViewSet,
    PostViewSet,
    CommentViewSet,
    AuthorViewSet,
    LatestPostsFeed,
)
from candidate.views import (
    PartyViewSet,
    CandidateViewSet,
    FigureViewSet,
)
from timeline.views import (
    TimelineViewSet,
)
from preferences.views import (
    TextViewSet,
)
from questionnaire.views import (
    QuestionnaireViewSet,
    QuestionSetViewSet,
    QuestionCategoryViewSet,
    QuestionViewSet,
    ChoiceViewSet,
    ChoiceSetViewSet,
    ResponseViewSet,
    ParticipantViewSet,
    ParticipantDetailViewSet,
    ResultViewSet,
)
from wordcloud.views import WordCloudViewSet
from views import (
    DetailSearchViewSet,
    CandidateSearchViewSet,
    TagViewSet,
)

router = DefaultRouter()
# Blog End Point
router.register(r'ewatch/categories', CategoryViewSet)
router.register(r'ewatch/posts', PostViewSet)
router.register(r'ewatch/comments', CommentViewSet, base_name='comment')
router.register(r'ewatch/authors', AuthorViewSet)
# Timeline End Point
router.register(r'ewatch/timeline', TimelineViewSet)
# Candidate End Point
router.register(r'ewatch/parties', PartyViewSet)
router.register(r'ewatch/figures', FigureViewSet)
router.register(r'ewatch/candidates', CandidateViewSet)
# Questionnaire End Point
router.register(r'questionnaire/questionnaires', QuestionnaireViewSet)
router.register(r'questionnaire/questionsets', QuestionSetViewSet)
router.register(r'questionnaire/questions', QuestionViewSet)
router.register(r'questionnaire/questioncategory', QuestionCategoryViewSet)
router.register(r'questionnaire/choices', ChoiceViewSet)
router.register(r'questionnaire/choicesets', ChoiceSetViewSet)
router.register(r'questionnaire/responses', ResponseViewSet, base_name='response')
router.register(r'questionnaire/participants', ParticipantViewSet, base_name='participant')
router.register(r'questionnaire/participantsdetail', ParticipantDetailViewSet, base_name='participantdetail')
router.register(r'questionnaire/participant/(?P<pid>[0-9]+)/result', ResultViewSet, base_name='result')
# Word Cloud End Point
router.register(r'ewatch/candidate/(?P<candid>[0-9]+)/wordcloud', WordCloudViewSet, base_name='word-cloud')
# Preferences End Point
router.register(r'preferences/texts', TextViewSet)
# Search
router.register(r'ewatch/search', DetailSearchViewSet, base_name='search')
router.register(r'ewatch/candidate-search', CandidateSearchViewSet, base_name='candidate-search')
router.register(r'ewatch/tags', TagViewSet, base_name='tag')

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/(?P<version>(v1))/', include(router.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^posts/rss/$', LatestPostsFeed()),
]
