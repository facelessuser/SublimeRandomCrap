import sublime_plugin
import sublime


class FindCaretCommand(sublime_plugin.ApplicationCommand):
    def restore(self):
        self.settings.set("caret_extra_width", self.width)
        self.settings.set("caret_extra_bottom", self.bottom)
        self.settings.set("caret_extra_top", self.top)
        self.settings.set("inverse_caret_state", self.inverse)
        self.settings.set("caret_style", self.style)

    def run(self):
        self.settings = sublime.load_settings("Preferences.sublime-settings")
        self.width = self.settings.get("caret_extra_width", 0)
        self.top = self.settings.set("caret_extra_top", 0)
        self.bottom = self.settings.get("caret_extra_bottom", 0)
        self.inverse = self.settings.get("inverse_caret_state", False)
        self.style = self.settings.get("caret_style", "smooth")
        self.settings.set("caret_extra_width", 10)
        self.settings.set("caret_extra_bottom", 0)
        self.settings.set("caret_extra_top", 0)
        self.settings.set("inverse_caret_state", False)
        self.settings.set("caret_style", "smooth")
        sublime.set_timeout(self.restore, 3000)
