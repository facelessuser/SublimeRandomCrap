import sublime
import sublime_plugin
from os.path import join

TEMPLATE_NAME = "custom-template.html"


def set_template():
    path = join(sublime.packages_path(), "User", TEMPLATE_NAME)
    settings = sublime.load_settings("MarkdownPreview.sublime-settings")
    if settings.get("html_template") != path:
        print("setting")
        settings.set("html_template", path)
        sublime.save_settings("MarkdownPreview.sublime-settings")


class SetMarkdownTemplate(sublime_plugin.ApplicationCommand):
    def run(self):
        set_template()


def plugin_loaded():
    set_template()
