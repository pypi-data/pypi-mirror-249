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

from urllib.parse import quote

import click
from ldap3 import ALL_ATTRIBUTES, AUTO_BIND_NO_TLS, SAFE_SYNC, Connection, Server


@click.command()
@click.option("--first", help="First name")
@click.option("--last", help="Last name")
@click.option(
    "--login",
    help="Login (the part that comes before @debian.org in the email address)",
)
@click.option("--irc", help="IRC nickname (usually on OFTC)")
@click.option("--fingerprint", help="GPG key fingerprint in the Debian keyring")
def search_db(first, last, login, irc, fingerprint):
    """
    Search for developers in the Debian LDAP directory.
    """
    server = Server("db.debian.org")
    conn = Connection(server, client_strategy=SAFE_SYNC, auto_bind=AUTO_BIND_NO_TLS)
    filters = []
    if first is not None:
        filters.append(f"(cn={quote(first, safe='*')})")
    if last is not None:
        filters.append(f"(sn={quote(last, safe='*')})")
    if login is not None:
        filters.append(f"(uid={quote(login, safe='*')})")
    if irc is not None:
        filters.append(f"(ircNick={quote(irc, safe='*')})")
    if fingerprint is not None:
        filters.append(f"(keyFingerPrint={quote(fingerprint)})")

    if len(filters) == 1:
        query = filters[0]
    elif len(filters) > 1:
        query = f'(&{"".join(filters)})'
    else:
        click.echo("No search filters passed.")
        raise NoSearchFiltersError

    status, result, response, _ = conn.search("ou=users,dc=debian,dc=org", query, attributes=ALL_ATTRIBUTES)

    if status:
        for user in response:

            def get(field, user=user):
                if field in user["attributes"]:
                    return user["attributes"][field][0]
                return click.style('none', fg=238)

            click.secho(f"{get('cn')} {get('sn')}", bold=True)
            click.echo(f"Login: {get('uid')}")
            click.echo(f"IRC: {get('ircNick')}")
            click.echo(f"URL: {get('labeledURI')}")
            click.echo(f"GPG fingerprint: {get('keyFingerPrint')}")
            click.echo("")
    elif result["result"] == 0:
        click.echo("No matches were found")
    else:
        click.echo("Unable to search LDAP directory")
        raise LDAPSearchError


class NoSearchFiltersError(Exception):
    pass


class LDAPSearchError(Exception):
    pass
