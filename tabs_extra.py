import sublime_plugin


class CloseTabCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        v = self.window.views_in_group(group).pop(index)
        self.window.focus_view(v)
        self.window.run_command("close_file")


class CloseTabsToLeftCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        views = self.window.views_in_group(group)
        for v in views[:index]:
            self.window.focus_view(v)
            self.window.run_command("close_file")


class CloseTabsToRightCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        views = self.window.views_in_group(group)
        if len(views) > index:
            for v in self.window.views_in_group(group)[index + 1:]:
                self.window.focus_view(v)
                self.window.run_command("close_file")


class CloseTabsOtherCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        views = self.window.views_in_group(group)
        views.pop(index)
        for v in views:
            self.window.focus_view(v)
            self.window.run_command("close_file")
