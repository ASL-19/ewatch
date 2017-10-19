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
    'questionnaire',
    'questionset',
    # 'question',
    # 'choice',
]

# End points to test for retrieve method
ep_detail = [
    'questionnaire',
    'questionset',
    # 'question',
    # 'choice',
]

# List of defined API versions
version_list = [
    'v1',
]


class APIEndpointTests(APITestCase):
    """
        Check for API End Point availability.
    """

    fixtures = ['questionnaire-test']

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

    fixtures = ['questionnaire-test']

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

    def check_choice(self, url, res, rec_id=None):
        """
            Helper method to check the Choice model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'text': u'Very Satisfied',
                    'order': 1,
                    'value': 1
                }
            },
            '2': {
                'required': {
                    'text': u'Satisfied',
                    'order': 2,
                    'value': 2
                }
            },
            '3': {
                'required': {
                    'text': u'OK',
                    'order': 3,
                    'value': 3
                }
            },
            '4': {
                'required': {
                    'text': u'Not Satisfied',
                    'order': 4,
                    'value': 4
                }
            },
            '5': {
                'required': {
                    'text': u'Extremely not satisfied',
                    'order': 5,
                    'value': 5
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

    def check_question(self, url, res, rec_id=None):
        """
            Helper method to check the Question model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '4': {
                'required': {
                    'text': u'<p>Do you agree to question 1?</p>',
                    'extra': u'',
                    'qtype': u'MCH',
                    'order': 1,
                    'required': True,
                    'enabled': True,
                },
            },
            '5': {
                'required': {
                    'text': u'<p>Do you agree to question 2?</p>',
                    'extra': u'',
                    'qtype': u'MCH',
                    'order': 2,
                    'required': True,
                    'enabled': True,
                },
            },
            '6': {
                'required': {
                    'text': u'<p>Do you agree to question economic&nbsp;1?</p>',
                    'extra': u'',
                    'qtype': u'MCH',
                    'order': 3,
                    'required': True,
                    'enabled': True,
                },
            },
            '7': {
                'required': {
                    'text': u'<p>Do you agree to question economic 2?</p>',
                    'extra': u'',
                    'qtype': u'MCH',
                    'order': 4,
                    'required': True,
                    'enabled': True,
                },
            },
            '8': {
                'required': {
                    'text': u'<p>What is your cultural percentage?</p>',
                    'extra': u'',
                    'qtype': u'PER',
                    'order': 1,
                    'required': True,
                    'enabled': True,
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

    def check_questionset(self, url, res, rec_id=None):
        """
            Helper method to check the Question Set model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'name': u'QS1',
                    'description': u'<p>cedwqw werv wervwaerv</p>',
                    'order': 1,
                },
            },
            '2': {
                'required': {
                    'name': u'QS2',
                    'description': u'<p>csa &nbsp;wdfv sdfb sdbsdfgbsdb</p>',
                    'order': 2,
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

    def check_questionnaire(self, url, res, rec_id=None):
        """
            Helper method to check the Questionnaire model API against expected
            values from test fixture.

            Args:
            url: URL of the request
            res: Results returned by the endpoint
            rec_id: Record ID of the result, if None it extracts it from url.
        """

        answers = {
            '1': {
                'required': {
                    'name': u'Sanjeh',
                    'description': '<p>Dvdv sdfbv sdfb vsdfb sdfbsdfgb</p>',
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

    # def test_choice_api_list(self):
    #     """
    #         Test for Choice list End point
    #     """

    #     url = reverse('choice-list', kwargs={'version': 'v1'})
    #     resp = self.client.get(url)
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #     content = json.loads(resp.content)

    #     self.assertIn('count', content)
    #     self.assertIn('next', content)
    #     self.assertIn('previous', content)
    #     self.assertIn('results', content)
    #     self.assertEqual(content['count'], 5)
    #     self.assertIsNone(content['next'])
    #     self.assertIsNone(content['previous'])
    #     results = content['results']
    #     self.assertEqual(len(results), 5)

    #     for res in results:
    #         self.check_choice(url, res)

    # def test_choice_api_detail(self):
    #     """
    #         Test for Choice detail End Point
    #     """

    #     for rec_id in range(1, 6):
    #         url = reverse('choice-detail', kwargs={'version': 'v1', 'pk': rec_id})
    #         resp = self.client.get(url)
    #         self.assertEqual(resp.status_code, status.HTTP_200_OK)
    #         content = json.loads(resp.content)
    #         self.check_choice(url, content)

    def test_question_api_list(self):
        """
            Test for Question list End point
        """

        url = reverse('question-list', kwargs={'version': 'v1'})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        content = json.loads(resp.content)

        self.assertIn('count', content)
        self.assertIn('next', content)
        self.assertIn('previous', content)
        self.assertIn('results', content)
        self.assertEqual(content['count'], 5)
        self.assertIsNone(content['next'])
        self.assertIsNone(content['previous'])
        results = content['results']
        self.assertEqual(len(results), 5)

        for res in results:
            self.check_question(url, res)
            self.assertIn('question_set', res)
            self.check_questionset(url, res['question_set'])

    def test_question_api_detail(self):
        """
            Text for Question detail End Point
        """

        for rec_id in range(4, 9):
            url = reverse('question-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_question(url, content)

    def test_questionset_api_list(self):
        """
            Test for Question Set list End point
        """

        url = reverse('questionset-list', kwargs={'version': 'v1'})
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
            self.check_questionset(url, res)
            self.assertIn('questionnaire', res)
            self.check_questionnaire(url, res['questionnaire'])
            self.assertIn('question', res)
            for q in res['question']:
                self.check_question(url, q)

    def test_questionset_api_detail(self):
        """
            Text for Question Set detail End Point
        """

        for rec_id in range(1, 3):
            url = reverse('questionset-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_questionset(url, content)

    def test_questionnaire_api_list(self):
        """
            Test for Questionnaire list End point
        """

        url = reverse('questionnaire-list', kwargs={'version': 'v1'})
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
            self.check_questionnaire(url, res)
            self.assertIn('question_set', res)
            for qs in res['question_set']:
                self.check_questionset(url, qs)

    def test_questionnaire_api_detail(self):
        """
            Text for Questionnaire detail End Point
        """

        for rec_id in range(1, 2):
            url = reverse('questionnaire-detail', kwargs={'version': 'v1', 'pk': rec_id})
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, status.HTTP_200_OK)
            content = json.loads(resp.content)
            self.check_questionnaire(url, content)
            self.assertIn('question_set', content)
            for qs in content['question_set']:
                self.check_questionset(url, qs)
