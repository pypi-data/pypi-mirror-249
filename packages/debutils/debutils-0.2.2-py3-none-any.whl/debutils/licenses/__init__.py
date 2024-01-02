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

from pathlib import Path

# Dict that maps SPDX license names to Debian license names
KNOWN_LICENSES = {
    "AGPL-3.0-or-later": "AGPL-3+",
    "Apache-2.0": "Apache-2.0",
    "BSD-2-Clause": "BSD-2-Clause",
    "BSD-3-Clause": "BSD-3-Clause",
    "MIT": "Expat",
    "GPL-2.0-or-later": "GPL-2+",
    "GPL-3.0-or-later": "GPL-3+",
}


def get_license_text(lic: str) -> str:
    return (Path(__file__).parent / f"{lic}.txt").read_text()
