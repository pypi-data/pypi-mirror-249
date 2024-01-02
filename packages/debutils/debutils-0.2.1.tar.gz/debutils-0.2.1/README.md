# debutils

[![PyPI - Version](https://img.shields.io/pypi/v/debutils.svg)](https://pypi.org/project/debutils)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/debutils.svg)](https://pypi.org/project/debutils)

Utilities to help Debian package maintainers.

This tool is currently very unstable. Feel free to use it, but please report
any bugs you find. If you have an idea for a new feature or commands, then
please let me know! [More info](#opening-issues)

-----

**Table of Contents**

- [Installation](#installation)
- [Contributing](#contributing)
  - [Opening issues](#opening-issues)
  - [Pull requests](#pull-requests)
- [Developing](#developing)
- [Why](#why)
- [Acknowledgements](#acknowledgements)
- [Packaging for Debian](#packaging-for-debian)
- [License](#license)

## Installation

To install from git:
```console
pip install git+https://codeberg.org/Maytha8/debutils.git
# I recommend using pipx instead of pip
```

To install from pypi:
```console
pip install debutils
# I recommend using pipx instead of pip
```

## Contributing

There are several ways you can contribute to debutils.

### Opening issues

If you find any bugs, or have any ideas for new functionality, please don't
hesitate to [open an issue](https://codeberg.org/Maytha8/debutils/issues/new).

### Pull requests

There's a long list of TODOs. Some of them can be found in [TODO](./TODO), and
others are strewn throughout the code as TODO comments.

You can help out by taking on one of these tasks and opening a pull request
with your changes.

## Developing

Clone this repo, and either use `hatch run ./main.py` or `hatch shell &&
./main.py` to run the CLI. (using `hatch run debutils` will install debutils
inside the venv, changes to the code aren't applied)

## Why

I had a few useful scripts lying around, so I decided to put them together and
create debutils. (e.g. [itpwriter](https://codeberg.org/Maytha8/itpwriter) is
now part of debutils.)

Additionally, dh-make-golang's make command failed to work some of the time,
leading to me having to manually follow dh-make-golang's source code and
assemble a package myself, and the estimate command *always* failed when I
tried it, even when I installed straight from the repo's HEAD.

## Acknowledgements

- [dh-make-golang](https://github.com/Debian/dh-make-golang) - the `go`
  subcommands are partially based on the work at dh-make-golang

## Packaging for Debian

I haven't packaged this for Debian (yet) because there isn't enough interest.
AFAIK I'm the only one using this.

If you reckon my work is worth having a package in Debian, feel free to file an
RFP at the Debian BTS (and X-Debbugs-CC me), or even better, package this
yourself (please add me to uploaders and let me know if you do so).

## License

```txt
debutils -- Utilities to help Debian package maintainers.
Copyright (C) 2023 Maytham Alsudany <maytha8thedev@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
