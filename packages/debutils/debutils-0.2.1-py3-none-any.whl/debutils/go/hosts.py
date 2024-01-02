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

# Known hosts and their Debian counterpart.
# Taken from https://github.com/Debian/dh-make-golang/blob/master/make.go#L574
# with a few additions.

KNOWN_HOSTS = {
    # dh-make-golang's known hosts
    "bazil.org": "bazil",
    "bitbucket.org": "bitbucket",
    "blitiri.com.ar": "blitiri",
    "cloud.google.com": "googlecloud",
    "code.google.com": "googlecode",
    "filippo.io": "filippo",
    "fyne.io": "fyne",
    "git.sr.ht": "sourcehut",
    "github.com": "github",
    "gitlab.com": "gitlab",
    "go.cypherpunks.ru": "cypherpunks",
    "go.mongodb.org": "mongodb",
    "go.opentelemetry.io": "opentelemetry",
    "go.step.sm": "step",
    "go.uber.org": "uber",
    "go4.org": "go4",
    "gocloud.dev": "gocloud",
    "golang.org": "golang",
    "google.golang.org": "google",
    "gopkg.in": "gopkg",
    "honnef.co": "honnef",
    "howett.net": "howett",
    "k8s.io": "k8s",
    "modernc.org": "modernc",
    "pault.ag": "pault",
    "rsc.io": "rsc",
    "salsa.debian.org": "debian",
    "sigs.k8s.io": "k8s-sigs",
    "software.sslmate.com": "sslmate",
    # extra hosts
    "gitea.com": "gitea",
    "code.gitea.io": "code-gitea",
    "codeberg.org": "codeberg",
}
