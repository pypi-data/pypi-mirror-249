# debutils -- Utilities to help Debian package maintainers.
# Copyright (C) 2023 Maytham Alsudany <maytha8thedev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import re

import requests

WNPP_BUG_PATTERN = re.compile(
    r'<a href="https://bugs.debian.org/(?P<id>\d+)">(?P<package>[A-Za-z0-9\-\.]+): (?P<description>[\S ]+)</a>'
)


def get_all_itps():
    html = requests.get("https://www.debian.org/devel/wnpp/being_packaged", timeout=60).text
    return WNPP_BUG_PATTERN.findall(html)


def search_itps(package):
    itps = get_all_itps()
    return [itp for itp in itps if package in itp[1]]


def get_itp(package):
    itps = get_all_itps()
    for itp in itps:
        if package == itp[1]:
            return itp
    return None


def get_all_rfps():
    html = requests.get("https://www.debian.org/devel/wnpp/requested", timeout=60).text
    return WNPP_BUG_PATTERN.findall(html)


def search_rfps(package):
    rfps = get_all_rfps()
    return [rfp for rfp in rfps if package in rfp[1]]


def get_rfp(package):
    rfps = get_all_rfps()
    for rfp in rfps:
        if package == rfp[1]:
            return rfp
    return None
