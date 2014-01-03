import sys
from os.path import join, exists
from os import makedirs
import sublime
import sublime_plugin
import SublimeRandomCrap.icons as icons

notify = None

class SubNotifyInfoCommand(sublime_plugin.ApplicationCommand):
    def run(self, title="", msg=""):
        notify.info(title, msg)


def plugin_loaded():
    global notify
    sys.path.insert(0, join(sublime.packages_path(), "SublimeRandomCrap", "gntp"))

    from SublimeRandomCrap.lib import notify

    user = join(sublime.packages_path(), "User", "SubNotify")
    if not exists(user):
        makedirs(user)
    notify.setup_notifications("Sublime Text", icons.notify_png.GetData(), None, user)
    notify.enable_growl(True)
