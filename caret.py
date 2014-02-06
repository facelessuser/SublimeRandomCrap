import sublime_plugin
import sublime
import time


class FindCaretCommand(sublime_plugin.TextCommand):
    def save_item(self, defaults, src, dest):
        """
        Save the item if setting is available.
        """

        setting = self.settings.get(dest, None)
        if setting is not None:
            defaults[src] = setting

    def save(self):
        """
        Save the view's caret settings.
        """

        self.settings = self.view.settings()
        if self.settings.get("caret_defaults", None) is None:
            defaults = {}
            self.save_item(defaults, "width", "caret_extra_width")
            self.save_item(defaults, "top", "caret_extra_top")
            self.save_item(defaults, "bottom", "caret_extra_bottom")
            self.save_item(defaults, "style" , "caret_style")
            self.save_item(defaults, "inverse", "inverse_caret_state")
            self.settings.set("caret_defaults", defaults)

    def restore_item(self, defaults, src, dest):
        """
        Restore item if setting is available. Erase item if it is not.
        """

        setting = defaults.get(src, None)
        self.settings.set(dest, setting) if setting is not None else self.settings.erase(dest)

    def restore(self, t):
        """
        Restore the view's caret settings.
        """

        if self.settings.get("caret_last_change", "") == t:
            defaults = self.settings.get("caret_defaults", None)
            if defaults is not None:
                self.restore_item(defaults, "width", "caret_extra_width")
                self.restore_item(defaults, "top", "caret_extra_top")
                self.restore_item(defaults, "bottom", "caret_extra_bottom")
                self.restore_item(defaults, "style", "caret_style")
                self.restore_item(defaults, "inverse", "inverse_caret_state")
            self.settings.erase("caret_defaults")

    def high_visibility(self):
        """
        Make the caret highly visible
        """

        self.time = time.time()
        self.settings.set("caret_extra_width", 10)
        self.settings.set("caret_extra_bottom", 0)
        self.settings.set("caret_extra_top", 0)
        self.settings.set("inverse_caret_state", False)
        self.settings.set("caret_style", "smooth")
        self.settings.set("caret_last_change", str(self.time))

    def show_at_center(self, show_at_center):
        """
        Show the next caret at the given index.
        """

        if show_at_center is None or show_at_center not in [1, -1]:
            return
        direction = show_at_center
        index = int(self.settings.get("caret_last_index", -1))
        sel = self.view.sel()
        if len(sel):
            index += 1 * direction
            if index < 0:
                index = len(sel) - 1
            elif index >= len(sel):
                index = 0
            self.view.show_at_center(sel[index])
            self.settings.set("caret_last_index", index)

    def run(self, edit, show_at_center=None):
        """
        Show the cursor and the carets in a highly visible way, then revert them back to normal.
        """

        self.save()
        self.high_visibility()
        self.show_at_center(int(show_at_center) if show_at_center is not None else show_at_center)
        sublime.set_timeout(lambda t=str(self.time): self.restore(t), 3000)


class CaretListener(sublime_plugin.EventListener):
    def on_selection_modified_async(self, view):
        """
        If selection was modified, erase the tracked last index.
        """

        view.settings().erase("caret_last_index")
