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
from rest_framework import status
from rest_framework.test import APITestCase

# End Points to test for list method
ep_list = [
    'timeline',
]

# End points to test for retrieve method
ep_detail = [
    'timeline',
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
        'timeline-test',
        'blog-test',
        'candidate-test',
    ]

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
        'timeline-test',
        'blog-test',
        'candidate-test',
    ]

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

    def check_timeline(self, url, res, rec_id=None):
        """
            Helper method to check the Timeline model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'title': u'News 1',
                    'content': u'<p>News 1 content</p>',
                    'tag': u'news, timeline',
                    'timestamp': u'1390-12-05 11:45:00+0000',
                    'candidate_tag': [
                        u'Mahmoud Ahmadinejad',
                        u'test candidate'
                    ]
                }
            },
            '2': {
                'required': {
                    'title': u'خبر ۲',
                    'content': u'<p>خبر درباره محمودی&nbsp;</p>',
                    'tag': u'خبر , محمودی',
                    'timestamp': u'1390-12-02 07:45:00+0000',
                    'candidate_tag': [
                        u'Mahmoud Ahmadinejad',
                    ]
                }
            },
            '3': {
                'required': {
                    'title': u'test news',
                    'content': u'<p>Test news content</p>',
                    'tag': u'test, news',
                    'timestamp': u'1390-11-25 17:50:00+0000',
                    'candidate_tag': [
                        u'test candidate',
                        u'حسن روحانی',
                    ]
                }
            }
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

    def test_timeline_api_list(self):
        """
            Test for Timeline list End point
        """

        url = reverse('timeline-list', kwargs={'version': 'v1'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = json.loads(resp.content)

        self.assertIn('count', content)
        self.assertIn('next', content)
        self.assertIn('previous', content)
        self.assertIn('results', content)
        self.assertEqual(content['count'], 3)
        self.assertIsNone(content['next'])
        self.assertIsNone(content['previous'])
        results = content['results']
        self.assertEqual(len(results), 3)

        for res in results:
            self.check_timeline(url, res)
            self.assertIn('category', res)

    def test_timeline_api_detail(self):
        """
            Text for Timeline detail End Point
        """

        for rec_id in range(1, 4):
            url = reverse('timeline-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_timeline(url, content)
            self.assertIn('category', content)
