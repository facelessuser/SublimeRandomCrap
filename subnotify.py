import sys
from os.path import join, exists
from os import makedirs
import sublime
import sublime_plugin
import SublimeRandomCrap.icons as icons

notify = None
PLUGIN_SETTINGS = "sub_notify.sublime-settings"
SUB_NOTIFY_READY = False


def log(msg, status=False):
    string = str(msg)
    print("SubNotify: %s" % string)
    if status:
        sublime.status_message(string)


def debug_log(s):
    if sublime.load_settings(PLUGIN_SETTINGS).get("debug", False):
        log(s)


class SubNotifyInfoCommand(sublime_plugin.ApplicationCommand):
    def run(self, title="", msg=""):
        notify.info(title, msg)


class SubNotifyIsReadyCommand(sublime_plugin.ApplicationCommand):
    @classmethod
    def is_ready(cls):
        return SUB_NOTIFY_READY

    def run(self):
        ready = SubNotifyIsReadyCommand.is_ready()
        if ready:
            log("Ready for messages!")


def plugin_loaded():
    global notify
    global SUB_NOTIFY_READY
    sys.path.insert(0, join(sublime.packages_path(), "SublimeRandomCrap", "gntp"))

    from SublimeRandomCrap.lib import notify

    user = join(sublime.packages_path(), "User", "SubNotify")
    if not exists(user):
        makedirs(user)
    notify.setup_notifications("Sublime Text", icons.notify_png.GetData(), None, user)
    notify.enable_growl(sublime.load_settings(PLUGIN_SETTINGS).get("enable_growl", False))
    SUB_NOTIFY_READY = True
