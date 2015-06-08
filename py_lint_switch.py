"""
PyLintSwitch Sublime Plugin.

Allows the switching of python version in Sublme Linter plugin.

Doesn't really work well in Windows due to the way Python environments are added
to the windows registery etc.  But on OSX (and probably Linunx) it works well.

Overtime though, I have found myself just allowing PY3 lint to lint PY2.

Add the following command:

```js
    //////////////////////////////////
    // Lint Switch
    //////////////////////////////////
    {
        "caption": "LintSwitch: Toggle Python Version",
        "command": "py_lint_switch"
    },
```

Licensed under MIT
Copyright (c) 2014-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import sublime
import sublime_plugin
import sys

if not sys.platform.startswith('win'):
    class PyLintSwitchCommand(sublime_plugin.TextCommand):

        """Switch Python version for specific linters."""

        def run(self, edit):
            """Run the command."""

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

        """Listener for PyLintSwitch."""

        def on_activated(self, view):
            """On activated, specify Python version."""
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
