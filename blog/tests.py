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


import json
from django.core.urlresolvers import reverse
from django.core.management import settings
from rest_framework import status
from rest_framework.test import APITestCase

# End Points to test for list method
ep_list = [
    'category',
    'post',
    'comment',
]

# End points to test for retrieve method
ep_detail = [
    'category',
]

# List of defined API versions
version_list = [
    'v1',
]


class APIEndpointTests(APITestCase):
    """
        Check for API End Point availability.
    """

    fixtures = [
        'blog-test',
        'candidate-test']

    def test_eps_up(self):
        """
            Test the end points for list and retrieve method.
        """
        for ep in ep_list:
            for ver in version_list:
                eplist = ep + '-list'

                url = reverse(eplist, kwargs={'version': ver})
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, status.HTTP_200_OK)

                url = url.replace('/v1/', '/v0/')
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        for ep in ep_detail:
            for ver in version_list:
                epdetail = ep + '-detail'
                print epdetail

                url = reverse(epdetail, kwargs={'version': ver, 'pk': 1})
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, status.HTTP_200_OK)

                url = url.replace('/v1/', '/v0/')
                resp = self.client.get(url)
                self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class APIContentTests(APITestCase):
    """
        Check for API End Points contents
    """

    fixtures = [
        'blog-test',
        'candidate-test']

    def check_answers(self, res, answer, exceptions=[]):
        """
            Helper method to check the results against a dictionary

            The dictionary has 'required' parameters which should exist in
            the results and 'optional' parameters which if exist should match
            the value.

            Args:
            res: Results returned by the API endpoint
            answer: Dictionary of the expected values
            exceptions: A list of properties not to check. In case we're using the
                same dictionary for more than one end point.
        """

        # check_url(res['url'], rec_id)
        if 'required' in answer:
            for item in answer['required']:
                if item in exceptions:
                    continue
                self.assertIn(item, res)
                self.assertEqual(res[item], answer['required'][item])
        if 'optional' in answer:
            for item in answer['optional']:
                if item in exceptions:
                    continue
                if item in res:
                    self.assertEqual(res[item], answer['optional'][item])

    def check_post(self, url, res, rec_id=None):
        """
            Helper method to check the Post model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'published_date': u'1390-12-05 11:00:00+0000',
                    'title': u'This is a post title',
                    'content': u'<p>This is the content of the same post</p>',
                    'tag': u'Post, Content',
                    'summary': u'<p>This is the summary of the post</p>',
                    'slug': u'post',
                    'status': 'p',
                    'comment_allowed': True,
                    'candidate_tag': [
                        u'test candidate'
                    ]
                },
            },
            '2': {
                'required': {
                    'published_date': u'1390-12-05 11:00:00+0000',
                    'title': u'یه پست مخصوص',
                    'content': u'<p>این یه پست مخصوص. بنابرین &nbsp;جدی بگیرین&nbsp;</p>',
                    'tag': u'پست, مخصوص',
                    'summary': u'<p>خلاصه پست مخصوص&nbsp;</p>',
                    'slug': u'post_makhsoos',
                    'status': 'p',
                    'comment_allowed': True,
                    'candidate_tag': [
                        u'test candidate',
                        u'حسن روحانی'
                    ]
                },
            },
            '3': {
                'required': {
                    'published_date': u'1390-12-06 12:10:00+0000',
                    'title': u'A post',
                    'content': u'<p>This is a test post</p>',
                    'tag': u'post',
                    'summary': u'',
                    'slug': u'post1',
                    'status': 'p',
                    'comment_allowed': False,
                    'candidate_tag': [
                        u'حسن روحانی'
                    ]
                },
            },
            '4': {
                'required': {
                    'published_date': u'1390-12-06 12:55:00+0000',
                    'title': u'Relevant Post',
                    'content': u'<p>Relevant Post Content</p>',
                    'tag': u'Relevant, post, content',
                    'summary': u'<p>Relevant Summary Test</p>',
                    'slug': u'relevant',
                    'status': 'p',
                    'comment_allowed': True,
                    'candidate_tag': [
                        u'Mahmoud Ahmadinejad'
                    ]
                },
            },

        }

        self.assertIn('url', res)
        # self.check_url(url, res['url'], rec_id)
        self.assertIn('last_modified_date', res)

        if rec_id is None:
            if 'id' in res:
                rec_id = res['id']
                # self.check_url(url, res['url'], rec_id)
            else:
                if 'url' in res:
                    rec_id = res['url'][-2]

        if str(rec_id) in answers:
            self.check_answers(res, answers[str(rec_id)])

    def check_author(self, url, res, rec_id=None):
        """
            Helper method to check the Author model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'first_name': u'',
                    'last_name': u'',
                    'groups': [],
                },
            },
        }

        self.assertIn('url', res)
        # self.check_url(url, res['url'], rec_id)

        if rec_id is None:
            if 'id' in res:
                rec_id = res['id']
                # self.check_url(url, res['url'], rec_id)
            else:
                if 'url' in res:
                    rec_id = res['url'][-2]

        if str(rec_id) in answers:
            self.check_answers(res, answers[str(rec_id)])

    def check_category(self, url, res, rec_id=None):
        """
            Helper method to check the Category model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        if settings.BUILD_ENV == 'production':
            server = u'https://s3.amazonaws.com/ewatch'
        else:
            server = u'http://testserver'

        answers = {
            '1': {
                'required': {
                    'name': u'Educational',
                    'logo': server + u'/media/blog/logos/education-logo-23746383.jpg',
                },
            },
            '2': {
                'required': {
                    'name': u'Analysis',
                    'logo': server + u'/media/blog/logos/71513-200.png',
                },
            },
        }

        self.assertIn('url', res)
        # self.check_url(url, res['url'], rec_id)
        self.assertIn('last_modified_date', res)

        if rec_id is None:
            if 'id' in res:
                rec_id = res['id']
                # self.check_url(url, res['url'], rec_id)
            else:
                if 'url' in res:
                    rec_id = res['url'][-2]

        if str(rec_id) in answers:
            self.check_answers(res, answers[str(rec_id)])

    def check_comment(self, url, res, rec_id=None):
        """
            Helper method to check the Comment model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'comment_date': u'1390-12-08 13:14:00.000076+0000',
                    'email': u'tester@example.com',
                    'name': u'Mr. Tester',
                    'title': u'To Test Comments',
                    'content': u'I am testing the comments',
                    'approved': True,
                    'post': u'http://testserver/api/v1/ewatch/posts/post/'
                },
            }
        }

        if rec_id is None:
            if 'id' in res:
                rec_id = res['id']
                # self.check_url(url, res['url'], rec_id)
            else:
                if 'url' in res:
                    rec_id = res['url'][-2]

        if str(rec_id) in answers:
            self.check_answers(res, answers[str(rec_id)])

    def test_cat_api_list(self):
        """
            Test for Category list End point
        """

        url = reverse('category-list', kwargs={'version': 'v1'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = json.loads(resp.content)

        self.assertIn('count', content)
        self.assertIn('next', content)
        self.assertIn('previous', content)
        self.assertIn('results', content)
        self.assertEqual(content['count'], 2)
        self.assertIsNone(content['next'])
        self.assertIsNone(content['previous'])
        results = content['results']
        self.assertEqual(len(results), 2)

        for res in results:
            self.check_category(url, res)

    def test_cat_api_detail(self):
        """
            Text for Category detail End Point
        """

        for rec_id in range(1, 3):
            url = reverse('category-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_category(url, content)

    def test_post_api_list(self):
        """
            Test for Post list End point
        """

        url = reverse('post-list', kwargs={'version': 'v1'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = json.loads(resp.content)

        self.assertIn('count', content)
        self.assertIn('next', content)
        self.assertIn('previous', content)
        self.assertIn('results', content)
        self.assertEqual(content['count'], 4)
        self.assertIsNone(content['next'])
        self.assertIsNone(content['previous'])
        results = content['results']
        self.assertEqual(len(results), 4)

        for res in results:
            self.check_post(url, res)
            self.assertIn('category', res)
            self.check_category(url, res['category'])
            self.assertIn('author', res)
            self.check_author(url, res['author'])

    def test_post_api_detail(self):
        """
            Text for Post detail End Point
        """

        for slug in ['post', 'post_makhsoos', 'post1', 'relevant']:
            url = reverse('post-detail', kwargs={'version': 'v1', 'slug': slug})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_post(url, content)

    def test_comment_api_list(self):
        """
            Test for Comment list End point
        """

        url = reverse('comment-list', kwargs={'version': 'v1'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = json.loads(resp.content)

        self.assertIn('count', content)
        self.assertIn('next', content)
        self.assertIn('previous', content)
        self.assertIn('results', content)
        self.assertEqual(content['count'], 0)
        self.assertIsNone(content['next'])
        self.assertIsNone(content['previous'])
        results = content['results']
        self.assertEqual(len(results), 0)

        url += '?post=post'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = json.loads(resp.content)

        self.assertIn('count', content)
        self.assertIn('next', content)
        self.assertIn('previous', content)
        self.assertIn('results', content)
        self.assertEqual(content['count'], 1)
        self.assertIsNone(content['next'])
        self.assertIsNone(content['previous'])
        results = content['results']
        self.assertEqual(len(results), 1)

        for res in results:
            self.check_comment(url, res)
