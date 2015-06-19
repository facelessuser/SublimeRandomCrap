r"""
GrepHere Sublime Plugin.

Sends a sidebar path or current view path to your favorite grep gui program.
Multiple entries can be defined and you can limit them to a specific platform:

```js
    "grep_call": {
        "win": {
            "caption": "Grep Here...",
            "cmd": ["C:\\Program Files\\grepWin\\grepWin.exe", "/searchpath:${PATH}"],
            "platform": ["windows"]
        },
        "win_rummage": {
            "caption": "Rummage Here...",
            "cmd": ["C:\\Program Files (x86)\\Rummage\\Rummage.exe", "-s", ":${PATH}"],
            "platform": ["windows"]
        },
        "osx": {
            "caption": "Rummage Here...",
            "cmd": ["/Applications/Rummage.app/Contents/MacOS/Rummage", "-s", "${PATH}"],
            "platform": ["osx"]
        }
    }
```

You can then define actual commands for the context menu or sidebar context menu:

    Context menu:
    ```js
        {"command": "grep_here_file", "args": {"key": "osx"}},
        {"command": "grep_here_file", "args": {"key": "win"}},
        {"command": "grep_here_file", "args": {"key": "win_rummage"}},
    ```

    Sidebar menu:

    ```js
        {"command": "grep_here_folder", "args": {"paths": [], "key": "osx"}},
        {"command": "grep_here_folder", "args": {"paths": [], "key": "win"}},
        {"command": "grep_here_folder", "args": {"paths": [], "key": "win_rummage"}}
    ```

Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

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
import sublime_plugin
import sublime
import subprocess
from os.path import exists
import traceback
import sys

NO_GREP = 0
NO_TARGET = 1

NO_GREP = "Nothing to grep!"
CALL_FAILURE = "SubProcess Error:\n%s"

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"


def get_environ():
    """Get environment and force utf-8."""

    import os
    env = {}
    env.update(os.environ)

    if _PLATFORM != 'windows':
        shell = env['SHELL']
        p = subprocess.Popen(
            [shell, '-l', '-c', 'echo "#@#@#${PATH}#@#@#"'],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        result = p.communicate()[0].decode('utf8').split('#@#@#')
        if len(result) > 1:
            bin_paths = result[1].split(':')
            if len(bin_paths):
                env['PATH'] = ':'.join(bin_paths)

    env['PYTHONIOENCODING'] = 'utf8'
    env['LANG'] = 'en_US.UTF-8'
    env['LC_CTYPE'] = 'en_US.UTF-8'

    return env


class GrepHereBase(object):

    """Grep Base class."""

    def fail(self, msg, alert=True):
        """Display failure."""

        if alert:
            sublime.error_message(msg)
        else:
            print("GrepHere: %s" % msg)

    def call_grep(self, target, key):
        """Call grep program."""

        call = None
        setting = sublime.load_settings("grep_here.sublime-settings").get('grep_call', {})
        obj = setting.get(key, None)
        if obj is not None:
            call = obj.get('cmd', [])
        if call is not None:
            index = 0
            for item in call:
                call[index] = item.replace("${PATH}", target)
                index += 1
            try:
                if sublime.platform() == "windows":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    subprocess.Popen(call, startupinfo=startupinfo, env=get_environ())
                else:
                    subprocess.Popen(call, env=get_environ())
            except Exception:
                self.fail(CALL_FAILURE % str(traceback.format_exc()))


class GrepHere(GrepHereBase):

    """Grep Here."""

    def is_text_cmd(self):
        """Detect if TextCommand."""

        return isinstance(self, sublime_plugin.TextCommand)

    def is_win_cmd(self):
        """Detect if WindowCommand."""

        return isinstance(self, sublime_plugin.WindowCommand)

    def get_target(self, paths=[]):
        """Get the target."""

        target = None
        fail_msg = NO_GREP
        if len(paths):
            target = paths[0]
        elif self.is_text_cmd():
            filename = self.view.file_name()
            if filename is not None and exists(filename):
                target = filename
            else:
                self.fail(fail_msg)
        else:
            self.fail(fail_msg)
        return target

    def grep(self, paths=[], key=None):
        """Call grep program."""

        if key is None:
            return
        target = self.get_target(paths)
        if target is None:
            return

        self.call_grep(target, key)


class GrepHereFileCommand(sublime_plugin.TextCommand, GrepHere):

    """Grep the file."""

    def run(self, edit, key):
        """Run the command."""

        self.grep(paths=[], key=key)

    def description(self, key=None):
        """Get command description."""

        caption = None
        if key is not None:
            setting = sublime.load_settings("grep_here.sublime-settings").get('grep_call', {})
            obj = setting.get(key, None)
            if obj is not None:
                caption = obj.get('caption', None)
        return caption

    def is_enabled(self, key=None):
        """Check if command is enabled."""

        enabled = False
        if key is not None:
            setting = sublime.load_settings("grep_here.sublime-settings").get('grep_call', {})
            obj = setting.get(key, None)
            if key is not None:
                platform = obj.get('platform', [])
                if len(platform):
                    if '*' in platform or sublime.platform() in platform:
                        enabled = True
        return enabled

    is_visible = is_enabled


class GrepHereFolderCommand(sublime_plugin.WindowCommand, GrepHere):

    """Grep the folder."""

    def run(self, paths=[], key=None):
        """Run the command."""

        self.grep(paths=paths, key=key)

    def description(self, paths=[], key=None):
        """Get command description."""

        caption = None
        if key is not None:
            setting = sublime.load_settings("grep_here.sublime-settings").get('grep_call', {})
            obj = setting.get(key, None)
            if obj is not None:
                caption = obj.get('caption', None)
        return caption

    def is_enabled(self, paths=[], key=None):
        """Check if command is enabled."""

        enabled = False
        if key is not None:
            setting = sublime.load_settings("grep_here.sublime-settings").get('grep_call', {})
            obj = setting.get(key, None)
            if key is not None:
                platform = obj.get('platform', [])
                if len(platform):
                    if '*' in platform or sublime.platform() in platform:
                        enabled = True
        return enabled

    is_visible = is_enabled
