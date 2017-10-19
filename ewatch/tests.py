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


from django.test import TestCase
import os
from django.core.management import settings


class Pep8TestCase(TestCase):
    """
        Runs PEP8 test against the code.

        This test uses the flake8 module.
    """

    def test_pep8(self):
        """
            Run a shell script to run flake8 against the
            code.
        """

        self.assertEqual(0, os.system(os.path.join(settings.BASE_DIR, 'linters.sh')))
