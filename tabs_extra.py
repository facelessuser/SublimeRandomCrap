import sublime_plugin
import sublime


def is_persistent():
    return sublime.load_settings("tabs_extra.sublime-settings").get("persistent_marks", False)


def respect_marks():
    return sublime.load_settings("tabs_extra.sublime-settings").get("all_commands_respect_marks", False)


class ClearAllTabMarksCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, force=False):
        if group == -1:
            return
        persistent = is_persistent()
        views = self.window.views_in_group(group)
        if not persistent or force:
            for v in views:
                v.settings().erase("tabs_extra_marked")


class CloseTabCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        check_marks = respect_marks
        views = self.window.views_in_group(group)
        v = views.pop(index)
        if not check_marks or (check_marks and not v.settings().get("tabs_extra_marked", False)):
            if not persistent:
                v.settings().erase("tabs_extra_marked")
            self.window.focus_view(v)
            self.window.run_command("close_file")
        elif not persistent:
            v.settings().erase("tabs_extra_marked")

        # Clear all marks
        if not persistent and len(views):
            self.window.run_command("clear_all_tab_marks", {"group": group})


class CloseTabsAllCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        check_marks = respect_marks
        views = self.window.views_in_group(group)
        for v in views:
            if not check_marks or (check_marks and not v.settings().get("tabs_extra_marked", False)):
                if not persistent:
                    v.settings().erase("tabs_extra_marked")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not persistent:
                v.settings().erase("tabs_extra_marked")


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
        view = self.window.views_in_group(group)[index]
        if view.settings().get("tabs_extra_marked", False):
            view.settings().erase("tabs_extra_marked")

    def is_visible(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        return self.window.views_in_group(group)[index].settings().get("tabs_extra_marked", False)


class CloseTabsMarkedCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        views = self.window.views_in_group(group)
        for v in views:
            if v.settings().get("tabs_extra_marked", False):
                if not persistent:
                    v.settings().erase("tabs_extra_marked")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not persistent:
                v.settings().erase("tabs_extra_marked")


class CloseTabsUnmarkedCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        views = self.window.views_in_group(group)
        for v in views:
            if not v.settings().get("tabs_extra_marked", False):
                if not persistent:
                    v.settings().erase("tabs_extra_marked")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not persistent:
                v.settings().erase("tabs_extra_marked")


class CloseTabsToLeftCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        check_marks = respect_marks()
        views = self.window.views_in_group(group)
        for v in views[:index]:
            if not check_marks or (check_marks and not v.settings().get("tabs_extra_marked", False)):
                if not persistent:
                    v.settings().erase("tabs_extra_marked")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not persistent:
                v.settings().erase("tabs_extra_marked")

        if not persistent and len(views[index:]):
            self.window.run_command("clear_all_tab_marks", {"group": group})


class CloseTabsToRightCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        check_marks = respect_marks()
        views = self.window.views_in_group(group)
        if len(views) > index:
            for v in self.window.views_in_group(group)[index + 1:]:
                if not check_marks or (check_marks and not v.settings().get("tabs_extra_marked", False)):
                    if not persistent:
                        v.settings().erase("tabs_extra_marked")
                    self.window.focus_view(v)
                    self.window.run_command("close_file")
                elif not persistent:
                    v.settings().erase("tabs_extra_marked")

        if not persistent and len(views[:index + 1]):
            self.window.run_command("clear_all_tab_marks", {"group": group})


class CloseTabsOtherCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        check_marks = respect_marks()
        views = self.window.views_in_group(group)
        views.pop(index)
        for v in views:
            if not check_marks or (check_marks and not v.settings().get("tabs_extra_marked", False)):
                if not persistent:
                    v.settings().erase("tabs_extra_marked")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not persistent:
                v.settings().erase("tabs_extra_marked")

        if not persistent:
            self.window.run_command("clear_all_tab_marks", {"group": group})


class TabsExtraListener(sublime_plugin.EventListener):
    def on_window_command(self, window, command_name, args):
        if command_name == "close_by_index":
            command_name = "close_tab"
            return (command_name, args)
        elif command_name == "close_others_by_index":
            command_name = "close_tabs_other"
            return (command_name, args)
        elif command_name == "close_to_right_by_index":
            command_name = "close_tabs_to_right"
            return (command_name, args)
        return None
