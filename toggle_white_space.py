"""
ToggleWhiteSpace Sublime Plugin.

Toggle showing white space in Sublime Text.

```
    //////////////////////////////////
    // Toggle White Space Command
    //////////////////////////////////
    {
        "caption": "Toggle White Space",
        "command": "toggle_white_space"
    },
```

Licensed under MIT
Copyright (c) 2013-2019 Isaac Muse <isaacmuse@gmail.com>

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


class ToggleWhiteSpaceCommand(sublime_plugin.ApplicationCommand):
    """Toggle the showing of whitespace in Sublime."""

    def run(self):
        """Run the command."""

        settings = sublime.load_settings("Preferences.sublime-settings")
        white_space = "selection" if settings.get("draw_white_space", "selection") != "selection" else "all"
        settings.set("draw_white_space", white_space)
        sublime.save_settings("Preferences.sublime-settings")
