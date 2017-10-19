#!/usr/bin/env python
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


import os
import sys

if __name__ == "__main__":
    assert "BUILD_ENV" in os.environ, "BUILD_ENV not set in environment"
    build_env = os.environ["BUILD_ENV"]
    os.environ["DJANGO_SETTINGS_MODULE"] = "ewatch.settings." + build_env

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
