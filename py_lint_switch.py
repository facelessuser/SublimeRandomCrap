import sublime
import sublime_plugin


class PyLintSwitchCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view_ver = self.view.settings().get("pylintswitch", 0)

        if view_ver == 3:
            py_ver = 2
        elif view_ver == 2:
            py_ver = 3
        else:
            py_ver = 3

        settings = sublime.load_settings("SublimeLinter.sublime-settings")
        user = settings.get("user")
        linters = user.get("linters", {})
        flake8 = linters.get("flake8", {})
        lint_ver = flake8.get("@python", 0)

        if py_ver == 0:
            if lint_ver == 0:
                py_ver = 3
            elif lint_ver == 2:
                py_ver = 3
            else:
                py_ver = 2

        self.view.settings().set("pylintswitch", py_ver)

        if py_ver != lint_ver:
            flake8["@python"] = py_ver
            linters["flake8"] = flake8
            user["linters"] = linters
            settings.set("user", user)
            print("PyLintSwitch: Set to Python%d" % py_ver)
        else:
            print("PyLintSwitch: Current Version is Python%d" % py_ver)


class PyLintSwitchListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        view_ver = view.settings().get("pylintswitch", 0)
        if view_ver == 0:
            view_ver = 3
            view.settings().set("pylintswitch", view_ver)

        settings = sublime.load_settings("SublimeLinter.sublime-settings")
        user = settings.get("user")
        linters = user.get("linters", {})
        flake8 = linters.get("flake8", {})
        lint_ver = flake8.get("@python", 0)

        if lint_ver != view_ver:
            flake8["@python"] = view_ver
            linters["flake8"] = flake8
            user["linters"] = linters
            settings.set("user", user)
            # print("PyLintSwitch: Set to Python%d" % view_ver)
        else:
            pass
            # print("PyLintSwitch: Current Version is Python%d" % view_ver)
