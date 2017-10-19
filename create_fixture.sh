#!/bin/bash
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


###############################################################################
#
# Company: ASL19
# Web: asl19.org
#
# Program:
#   Run manage.py dumpdata to create fixture with proper configuration
#
# Requirement:
#   Python should be on the PATH. Django is required of course. 
#
###############################################################################

./manage.py dumpdata blog --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output blog/fixtures/blog.json
./manage.py dumpdata candidate --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output candidate/fixtures/candidate.json
./manage.py dumpdata timeline --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output timeline/fixtures/timeline.json
./manage.py dumpdata questionnaire --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output questionnaire/fixtures/questionnaire.json
./manage.py dumpdata preferences --indent=4 --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --output preferences/fixtures/preferences.json
