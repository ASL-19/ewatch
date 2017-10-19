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
    'candidate',
    'party',
]

# End points to test for retrieve method
ep_detail = [
    'candidate',
    'party',
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

    fixtures = ['candidate-test']

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

    def check_candidate_list(self, url, res, rec_id=None):
        """
            Helper method to check the Candidate model API against expected
            values from test fixture. This check is for candidate list

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
                    'title': u'حسن روحانی',
                    'content': u'<p>حسن روحانی اولین&nbsp;<a href="https://fa.wikipedia.org/wiki/%D8%B1%D8%A6%DB%8C%D8%B3_%D8%AC%D9%85%D9%87%D9%88%D8%B1" title="رئیس جمهور">رئیس جمهور</a>&nbsp;ایران است که بعد از انقلاب ایران، با رئیس جمهور&nbsp;<a href="https://fa.wikipedia.org/wiki/%D8%A7%DB%8C%D8%A7%D9%84%D8%A7%D8%AA_%D9%85%D8%AA%D8%AD%D8%AF%D9%87_%D8%A2%D9%85%D8%B1%DB%8C%DA%A9%D8%A7" title="ایالات متحده آمریکا">ایالات متحده آمریکا</a>، ارتباط برقرار نمود</p>',
                    'tag': u'حسن ,روحانی',
                    'photo': server + u'/media/candidate/photos/Hassan_Rouhani_in_Saadabad.jpg',
                    'status': True,
                    'status_text': u'حسن ایز اکتیو'
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

    def check_candidate(self, url, res, rec_id=None):
        """
            Helper method to check the Candidate model API against expected
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
                    'title': u'حسن روحانی',
                    'content': u'<p>حسن روحانی اولین&nbsp;<a href="https://fa.wikipedia.org/wiki/%D8%B1%D8%A6%DB%8C%D8%B3_%D8%AC%D9%85%D9%87%D9%88%D8%B1" title="رئیس جمهور">رئیس جمهور</a>&nbsp;ایران است که بعد از انقلاب ایران، با رئیس جمهور&nbsp;<a href="https://fa.wikipedia.org/wiki/%D8%A7%DB%8C%D8%A7%D9%84%D8%A7%D8%AA_%D9%85%D8%AA%D8%AD%D8%AF%D9%87_%D8%A2%D9%85%D8%B1%DB%8C%DA%A9%D8%A7" title="ایالات متحده آمریکا">ایالات متحده آمریکا</a>، ارتباط برقرار نمود</p>',
                    'tag': u'حسن ,روحانی',
                    'photo': server + u'/media/candidate/photos/Hassan_Rouhani_in_Saadabad.jpg',
                    'bio': u'<p>حسن روحانی در سال ۱۳۲۷ در&nbsp;<a href=\"https://fa.wikipedia.org/wiki/%D8%B4%D9%87%D8%B1%D8%B3%D8%AA%D8%A7%D9%86_%D8%B3%D8%B1%D8%AE%D9%87\" title=\"شهرستان سرخه\">شهرستان سرخه</a>&nbsp;در&nbsp;<a href=\"https://fa.wikipedia.org/wiki/%D8%A7%D8%B3%D8%AA%D8%A7%D9%86_%D8%B3%D9%85%D9%86%D8%A7%D9%86\" title=\"استان سمنان\">استان سمنان</a>&nbsp;زاده شد.</p>',
                    'political_background': u'<p>فردا که آیت&zwnj;الله شدید، مردم شما را آیت&zwnj;الله فریدون بخوانند</p>',
                    'platform': u'<p dir=\"rtl\">دیدگاه&zwnj;های حسن روحانی در خصوص سیاست داخلی؛ تأکید بر فراجناحی بودن و شایسته&zwnj;سالار محوری کابینه، عدم تعهد دولت به احزاب و جناح&zwnj;های مختلف و وام&zwnj;دار نبودن به آنها، تثبیت جامعه به سمت رسانه&zwnj;های داخلی و خوش&zwnj;آمدگویی به تکثر و تنوع دیدگاه&zwnj;ها و دوری گزیدن از هر گونه خودسری؛ افراط و تفریط می&zwnj;باشد</p>',
                    'website': u'https://fa.wikipedia.org/wiki/%D8%AD%D8%B3%D9%86_%D8%B1%D9%88%D8%AD%D8%A7%D9%86%DB%8C',
                    'email': u'fereidoon@rouhani.com',
                    'telephone': u'98217656545433',
                    'fax': u'98217656545434',
                    'facebook': u'https://facebook.com/rouhani',
                    'twitter': u'@rouhani_twitter',
                    'instagram': u'@rouhani_insta',
                    'telegram': u'@rouhani_telegram',
                    'status': True,
                    'status_text': u'حسن ایز اکتیو'
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

    def check_party(self, url, res, rec_id=None):
        """
            Helper method to check the Party model API against expected
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
                    'title': u'اصلاح طلب',
                    'content': u'<p>اصلاح طلب گروه جالبه&nbsp;</p>',
                    'tag': u'اصلاح , طلب',
                    'logo': server + u'/media/candidate/logos/elahtalab_SyeaWMP.jpg',
                    'link': u'https://fa.wikipedia.org/wiki/%D8%A7%D8%B5%D9%84%D8%A7%D8%AD%E2%80%8C%D8%B7%D9%84%D8%A8%D8%A7%D9%86_%D8%A7%D9%81%D8%BA%D8%A7%D9%86%D8%B3%D8%AA%D8%A7%D9%86'
                },
            },
            '2': {
                'required': {
                    'title': u'جبهه پایداری انقلاب اسلامی',
                    'content': u'<h1>جبهه پایداری انقلاب اسلامی خیلی جالبه&nbsp;</h1>',
                    'tag': u'جبهه, پایداری ,انقلاب, اسلامی',
                    'logo': server + u'/media/candidate/logos/jebheh.jpg',
                    'link': u'https://fa.wikipedia.org/wiki/%D8%AC%D8%A8%D9%87%D9%87_%D9%BE%D8%A7%DB%8C%D8%AF%D8%A7%D8%B1%DB%8C_%D8%A7%D9%86%D9%82%D9%84%D8%A7%D8%A8_%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C'
                },
            },
            '3': {
                'required': {
                    'title': u'test party',
                    'content': u'<p>Test Party content</p>',
                    'tag': u'test, party',
                    'logo': server + u'/media/candidate/logos/firetweet-01.png',
                    'link': u'https://example.com/test_party'
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

    def test_candidate_api_list(self):
        """
            Test for Candidate list End point
        """

        url = reverse('candidate-list', kwargs={'version': 'v1'})
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
            self.check_candidate_list(url, res)

    def test_candidate_api_detail(self):
        """
            Text for Candidate detail End Point
        """

        for rec_id in range(1, 2):
            url = reverse('candidate-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_candidate(url, content)
            self.assertIn('party', content)
            for party in content['party']:
                self.check_party(url, party)

    def test_party_api_list(self):
        """
            Test for Party list End point
        """

        url = reverse('party-list', kwargs={'version': 'v1'})
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
            self.check_party(url, res)

    def test_party_api_detail(self):
        """
            Text for Party detail End Point
        """

        for rec_id in range(1, 4):
            url = reverse('party-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_party(url, content)
