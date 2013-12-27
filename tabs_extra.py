import sublime_plugin
import sublime


def is_persistent():
    return sublime.load_settings("tabs_extra.sublime-settings").get("persistent_sticky", False)


def respect_sticky():
    return sublime.load_settings("tabs_extra.sublime-settings").get("all_commands_respect_sticky", False)


class TabsExtraClearAllStickyCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, force=False):
        if group == -1:
            return
        persistent = is_persistent()
        views = self.window.views_in_group(group)
        if not persistent or force:
            for v in views:
                v.settings().erase("tabs_extra_sticky")

    def is_visible(self, group=-1, force=False):
        marked = False
        views = self.window.views_in_group(group)
        for v in views:
            if v.settings().get("tabs_extra_sticky", False):
                marked = True
                break
        return marked


class TabsExtraToggleStickyCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        view = self.window.views_in_group(group)[index]
        if not view.settings().get("tabs_extra_sticky", False):
            view.settings().set("tabs_extra_sticky", True)
        else:
            view.settings().erase("tabs_extra_sticky")

    def is_checked(self, group=-1, index=-1):
        if group == -1 or index == -1:
            return False
        return self.window.views_in_group(group)[index].settings().get("tabs_extra_sticky", False)


class TabsExtraCloseStickyCommand(sublime_plugin.WindowCommand):
    def run(self, group=-1, index=-1, invert=False):
        if group == -1 or index == -1:
            return
        persistent = is_persistent()
        views = self.window.views_in_group(group)
        for v in views:
            sticky = v.settings().get("tabs_extra_sticky", False)
            if (not invert and sticky) or (invert and not sticky):
                if not persistent:
                    v.settings().erase("tabs_extra_sticky")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not persistent:
                v.settings().erase("tabs_extra_sticky")


class TabsExtraCommand(sublime_plugin.WindowCommand):
    def init(self, close_type, group, index):
        self.persistent = is_persistent()
        self.check_sticky = respect_sticky()
        views = self.window.views_in_group(group)
        assert(close_type in ["single", "left", "right", "other", "all"])

        if close_type == "single":
            self.targets = [views.pop(index)]
            self.cleanup = bool(len(views[:index] + views[index + 1:]))
        elif close_type == "left":
            self.targets = views[:index]
            self.cleanup = bool(len(views[index:]))
        elif close_type == "right":
            self.targets = views[index + 1:]
            self.cleanup = bool(len(views[:index + 1]))
        elif close_type == "other":
            self.targets = views[:index] + views[index + 1:]
            self.cleanup = True
        elif close_type == "all":
            self.targets = views[:]
            self.cleanup = False

    def run(self, group=-1, index=-1, close_type="single"):
        if group == -1 or index == -1:
            return
        self.init(close_type, group, index)

        for v in self.targets:
            if not self.check_sticky or (self.check_sticky and not v.settings().get("tabs_extra_sticky", False)):
                if not self.persistent:
                    v.settings().erase("tabs_extra_sticky")
                self.window.focus_view(v)
                self.window.run_command("close_file")
            elif not self.persistent:
                v.settings().erase("tabs_extra_sticky")

        if not self.persistent and self.cleanup:
            self.window.run_command("tabs_extra_clear_all_sticky", {"group": group})


class TabsExtraListener(sublime_plugin.EventListener):
    def on_window_command(self, window, command_name, args):
        if command_name == "close_by_index":
            command_name = "tabs_extra"
            args["close_type"] = "single"
            return (command_name, args)
        elif command_name == "close_others_by_index":
            command_name = "tabs_extra"
            args["close_type"] = "other"
            return (command_name, args)
        elif command_name == "close_to_right_by_index":
            command_name = "tabs_extra"
            args["close_type"] = "right"
            return (command_name, args)
        return None
