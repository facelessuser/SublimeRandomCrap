import sublime_plugin


class CloseTabCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        v = self.window.views_in_group(group).pop(index)
        self.window.focus_view(v)
        self.window.run_command("close_file")


class CloseTabsAllCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        views = self.window.views_in_group(group)
        for v in views:
            self.window.focus_view(v)
            self.window.run_command("close_file")


class MarkTabCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        view = self.window.views_in_group(group)[index]
        if not view.settings().get("tabs_extra_marked", False):
            view.settings().set("tabs_extra_marked", True)


    def is_visible(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        return not self.window.views_in_group(group)[index].settings().get("tabs_extra_marked", False)


class UnmarkTabCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        if view.settings().get("tabs_extra_marked", False):
            view.settings().set("tabs_extra_marked", False)

    def is_visible(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        return self.window.views_in_group(group)[index].settings().get("tabs_extra_marked", False)


class CloseTabsMarkedCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        views = self.window.views_in_group(group)
        for v in views:
            if v.settings().get("tabs_extra_marked", False):
                self.window.focus_view(v)
                self.window.run_command("close_file")


class CloseTabsUnmarkedCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        views = self.window.views_in_group(group)
        for v in views:
            if not v.settings().get("tabs_extra_marked", False):
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


class TabsExtraListener(sublime_plugin.EventListener):
    def on_window_command(self, window, command_name, args):
        # if command_name == "close_by_index":
        #     command_name = "close_tab"
        #     return (command_name, args)
        # elif command_name == "close_others_by_index":
        #     command_name = "close_tabs_other"
        #     return (command_name, args)
        # elif command_name == "close_to_right_by_index":
        #     command_name = "close_tabs_to_right"
        #     return (command_name, args)
        return None
