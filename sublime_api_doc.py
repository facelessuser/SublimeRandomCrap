"""
SublimeApiDoc Sublime Plugin.

Show Sublime's API Doc site:

```
    //////////////////////////////////
    // Doc Commands
    //////////////////////////////////
    {
        "caption": "Sublime API Docs",
        "command": "show_sublime_api"
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
import webbrowser


class ShowSublimeApiCommand(sublime_plugin.ApplicationCommand):
    """Show the Sublime API in the web browser."""

    def run(self):
        """Run the command."""

        version = int(sublime.version())
        if version >= 4000 and version < 5000:
            webbrowser.open("https://www.sublimetext.com/docs/api_reference.html#ver-dev")
        elif version >= 3000 and version < 4000:
            webbrowser.open("https://www.sublimetext.com/docs/api_reference.html#ver-3.2")
        else:
            sublime.error_message("Version %d not supported" % version)
