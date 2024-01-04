"""sopel-factoriomods

A Sopel plugin to show information about linked Factorio mods.
"""
from __future__ import annotations

from datetime import datetime, timezone

import requests

from sopel import plugin, tools


MOD_PORTAL_API_TEMPLATE = 'https://mods.factorio.com/api/mods/{}/full'


class ModPortalError(Exception):
    pass


class NoSuchModError(ModPortalError):
    pass


def get_mod_info(name):
    """Get info about the <name> mod from Factorio's portal.

    Most error conditions are translated into ModPortalError or a subclass, to
    simplify handling for client code.
    """
    try:
        r = requests.get(MOD_PORTAL_API_TEMPLATE.format(name))
    except requests.exceptions.ConnectTimeout:
        raise ModPortalError("Connection timed out.")
    except requests.exceptions.ConnectionError:
        raise ModPortalError("Couldn't connect to server.")
    except requests.exceptions.ReadTimeout:
        raise ModPortalError("Server took too long to send data.")
    if r.status_code == 404:
        raise NoSuchModError(
            "Couldn't find a Factorio mod named '{}'. Are you sure it exists?"
            .format(name))
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ModPortalError("HTTP error: " + e.args[0])
    try:
        data = r.json()
    except ValueError:
        raise ModPortalError("ValueError when decoding: " + r.content)

    return data


def get_latest_release(release_list):
    """Given a single release dict, pick out just the latest version."""
    most_recent = None
    for release in release_list:
        if not most_recent or release['released_at'] > most_recent['released_at']:
            most_recent = release

    return release


def format_mod_info(data):
    """Format a Factorio mod data dict for output."""
    name = data['title']
    latest = get_latest_release(data['releases'])
    creation_date = datetime.strptime(
        data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
    ).replace(tzinfo=timezone.utc)
    creation_relative = tools.time.seconds_to_human(
        datetime.now(timezone.utc) - creation_date
    )
    version = latest['version']
    factorio_version = latest['info_json']['factorio_version']
    release_date = datetime.strptime(
        latest['released_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
    ).replace(tzinfo=timezone.utc)
    release_relative = tools.time.seconds_to_human(
        datetime.now(timezone.utc) - release_date
    )
    owner = data['owner'] or '(unknown name)'
    summary = data['summary']

    return " | ".join((
        "{name} by {owner}",
        "Created {creation_relative}",
        "Latest: {version} for Factorio {factorio_version} ({release_relative})",
        "{summary}",
    )).format(
        name=name,
        owner=owner,
        creation_relative=creation_relative,
        version=version,
        factorio_version=factorio_version,
        release_relative=release_relative,
        summary=summary,
    )


def say_info(bot, mod):
    """Fetch, format, and output the mod info to IRC."""
    try:
        data = get_mod_info(mod)
    except NoSuchModError as e:
        bot.say(e.args[0])
        return
    except ModPortalError:
        bot.say("Sorry, there was an error accessing the Mod Portal. Please try again later.")
        return

    bot.say(format_mod_info(data), truncation=' […]')


@plugin.url(r'https?:\/\/mods\.factorio\.com\/mod\/([\w\-\.]+)(?!\/)')
@plugin.output_prefix('[Factorio Mod] ')
def factorio_mod_link(bot, trigger, match):
    """Show information about a Factorio mod link in the chat."""
    say_info(bot, match.group(1))
