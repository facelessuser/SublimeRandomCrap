import sublime_plugin
import sublime


class FindCaretCommand(sublime_plugin.ApplicationCommand):
    def save(self):
        self.settings = sublime.load_settings("Preferences.sublime-settings")
        self.width = self.settings.get("caret_extra_width", 0)
        self.top = self.settings.set("caret_extra_top", 0)
        self.bottom = self.settings.get("caret_extra_bottom", 0)
        self.inverse = self.settings.get("inverse_caret_state", False)
        self.style = self.settings.get("caret_style", "smooth")

    def restore(self):
        self.settings.set("caret_extra_width", self.width)
        self.settings.set("caret_extra_bottom", self.bottom)
        self.settings.set("caret_extra_top", self.top)
        self.settings.set("inverse_caret_state", self.inverse)
        self.settings.set("caret_style", self.style)

    def high_visibility(self):
        self.settings.set("caret_extra_width", 10)
        self.settings.set("caret_extra_bottom", 0)
        self.settings.set("caret_extra_top", 0)
        self.settings.set("inverse_caret_state", False)
        self.settings.set("caret_style", "smooth")

    def show_at_center(self):
        win = sublime.active_window()
        if win is not None:
            view = win.active_view()
            if view is not None:
                sel = view.sel()
                if len(sel) == 1:
                    view.show_at_center(sel[0])

    def run(self, show_at_center=False):
        self.save()
        self.high_visibility()
        if show_at_center:
            self.show_at_center()
        sublime.set_timeout(self.restore, 3000)
