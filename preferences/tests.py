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
    'text',
]

# End points to test for retrieve method
ep_detail = [
    'text',
]

# List of defined API versions
version_list = [
    'v1',
]


class APIEndpointTests(APITestCase):
    """
        Check for API End Point availability.
    """

    fixtures = ['preferences-test']

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

        for ep in ep_list:
            for ver in version_list:
                epdetail = ep + '-detail'

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

    fixtures = ['preferences-test']

    def check_text(self, url, res, rec_id=None):
        """
            Helper method to check the Text model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        if rec_id is None:
            if 'id' in res:
                rec_id = res['id']
                # self.check_url(url, res['url'], rec_id)
            else:
                if 'url' in res:
                    rec_id = res['url'][-2]

        self.assertIn('language', res)
        self.assertIn('last_modified', res)
        self.assertIn('about', res)
        self.assertIn('contact_email', res)
        self.assertIn('privacy_policy', res)
        self.assertIn('terms_of_service', res)

        if rec_id == 1:
            self.assertEqual(res['language'], u'en')
            self.assertEqual(res['about'], u'<p>About Election Watch</p>')
            self.assertEqual(res['contact_email'], u'ewatch@ewatch.com')
            self.assertEqual(res['privacy_policy'], u'<p>Election Watch privacy policy</p>')
            self.assertEqual(res['terms_of_service'], u'<p>Election Watch terms of Service</p>')

    def test_text_api_list(self):
        """
            Test for Text list End point
        """

        url = reverse('text-list', kwargs={'version': 'v1'})
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
            self.check_text(url, res)

    def test_text_api_detail(self):
        """
            Text for text detail End Point
        """

        for rec_id in range(1, 2):
            url = reverse('text-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_text(url, content)
