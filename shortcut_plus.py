"""
Shortcut Plus

Copyright (c) 2012 Isaac Muse <isaacmuse@gmail.com>
License: MIT

Example:  This shows how to define two shortcut profiles bound to shortcuts

    // Shortcut Plus Toggle
    {
        "keys": ["alt+`"],
        "command": "toggle_shortcut_plus",
        "args": {"profile": "MyProfile1"}
    },
    // Shortcut Plus Toggle
    {
        "keys": ["ctrl+alt+`"],
        "command": "toggle_shortcut_plus",
        "args": {"profile": "MyProfile2"}
    },

Example: This shows how to create shortcuts that execute only in a given shorcut profile
         The first is bound to Myprofile1 and shows a dialog when all selections are empty
         and the escape key is pressed.

         The other is bound to MyProfile2 and shows the inverse when escape is pressed.

         "shortcut_plus_test" is command only for testing.  You can use any command you want.

    // Shortcut Plus Test
    {
        "keys": ["escape"],
        "command": "shortcut_plus_test",
        "context":
        [
            {"key": "shortcut_plus(profile):MyProfile1"},
            {"key": "selection_empty", "operator": "equal", "operand": true, "match_all": true}
        ],
        "args": {
            "msg": "All selection are empty!"
        }
    },
    // Shortcut Plus Test
    {
        "keys": ["escape"],
        "command": "shortcut_plus_test",
        "context":
        [
            {"key": "shortcut_plus(profile):MyProfile2"},
            {"key": "selection_empty", "operator": "equal", "operand": false, "match_all": true}
        ],
        "args": {
            "msg": "All selections are not empty!"
        }
    }
"""

import sublime
import sublime_plugin
import socket
from datetime import datetime, timedelta
import time

CURRENT_PLATFORM = sublime.platform()
CURRENT_HOSTNAME = socket.gethostname().lower()


def total_seconds(t):
    return int((t.microseconds + (t.seconds + t.days * 24 * 3600) * 10 ** 6) / 10 ** 6)


def get_current_time():
    now = datetime.now()
    seconds = total_seconds(timedelta(hours=now.hour, minutes=now.minute, seconds=now.second))
    return seconds, now


def translate_time(t):
    mn, mx = t.replace(" ", "").split('-')
    t_min = time.strptime(mn, '%H:%M')
    t_max = time.strptime(mx, '%H:%M')
    return (
        total_seconds(timedelta(hours=t_min.tm_hour, minutes=t_min.tm_min, seconds=t_min.tm_sec)),
        total_seconds(timedelta(hours=t_max.tm_hour, minutes=t_max.tm_min, seconds=t_max.tm_sec))
    )

class ShortcutMode(object):
    enabled = False
    profile = ""


class ShortcutPlusModeListener(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        handeled = False
        if ShortcutMode.enabled and key.startswith("shortcut_plus(profile):"):
            if ShortcutMode.profile == key[len("shortcut_plus(profile):"):len(key)]:
                handeled = True
        elif key.startswith("shortcut_plus(platform):"):
            if CURRENT_PLATFORM == key[len("shortcut_plus(platform):"):len(key)]:
                handeled = True
        elif key.startswith("shortcut_plus(hostname):"):
            if CURRENT_HOSTNAME == key[len("shortcut_plus(hostname):"):len(key)]:
                handeled = True
        elif key.startswith("shortcut_plus(ip):"):
            if socket.gethostbyname(socket.gethostname()) == key[len("shortcut_plus(ip):"):len(key)]:
                handeled = True
        elif key.startswith("shortcut_plus(timeframe):"):
            current_time, _ = get_current_time()
            t_min, t_max = translate_time(key[len("shortcut_plus(timeframe):"):len(key)])
            if t_min < t_max and t_min <= current_time < t_max:
                handeled = True
            elif t_min > t_max and (t_min <= current_time or current_time < t_max):
                handled = True
        return handeled


class ToggleShortcutPlusCommand(sublime_plugin.ApplicationCommand):
    def run(self, profile):
        if profile == "" or ShortcutMode.profile == profile:
            ShortcutMode.enabled = False
            ShortcutMode.profile = ""
        elif profile != ShortcutMode.profile:
            ShortcutMode.enabled = True
            ShortcutMode.profile = profile
        msg = "Shortcut Plus: %s" % (
            "%s Enabled" % ShortcutMode.profile if ShortcutMode.enabled else "Disabled"
        )
        sublime.status_message(msg)


class ShortcutPlusTestCommand(sublime_plugin.WindowCommand):
    def run(self, msg):
        sublime.message_dialog(msg)
