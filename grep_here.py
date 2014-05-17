"""
GrepWin Sublime Plugin

Licensed under MIT
Copyright (c) 2013 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sublime_plugin
import sublime
import subprocess
from os.path import exists
import traceback

NO_GREP = 0
NO_TARGET = 1

NO_GREP = "Nothing to grep!"
CALL_FAILURE = "SubProcess Error:\n%s"


class GrepHereBase(object):
    def fail(self, msg, alert=True):
        if alert:
            sublime.error_message(msg)
        else:
            print("GrepHere: %s" % msg)

    def call_grep(self, target):
        call = None
        for value in sublime.load_settings("grep_here.sublime-settings").get("grep_call", []):
            platform = value.get("platform", None)
            if platform is not None and platform == sublime.platform():
                call = value.get("cmd", None)
                break
        if call is not None:
            index = 0
            for item in call:
                call[index] = item.replace("${PATH}", target)
                index += 1
            try:
                subprocess.Popen(call)
            except:
                self.fail(CALL_FAILURE % str(traceback.format_exc()))


class GrepHere(GrepHereBase):
    def is_text_cmd(self):
        return isinstance(self, sublime_plugin.TextCommand)

    def is_win_cmd(self):
        return isinstance(self, sublime_plugin.WindowCommand)

    def get_target(self, paths=[]):
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

    def grep(self, paths=[]):
        target = self.get_target(paths)
        if target is None:
            return

        self.call_grep(target)


class GrepHereFileCommand(sublime_plugin.TextCommand, GrepHere):
    def run(self, edit):
        self.grep()


class GrepHereFolderCommand(sublime_plugin.WindowCommand, GrepHere):
    def run(self, paths=[]):
        self.grep(paths)
