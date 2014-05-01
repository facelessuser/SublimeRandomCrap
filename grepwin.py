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
from os.path import exists, abspath, normpath, isdir, dirname

NO_GREPWIN = 0
NO_TARGET = 1

ERRS = {
    NO_GREPWIN: "Nothing to grep!",
    NO_TARGET: "Cannot find grepWin Binary!"
}


class GrepWinBase(object):
    def fail(self, code, alert=True):
        if alert:
            sublime.error_message(ERRS[code])
        else:
            print(ERRS[code])

    def get_rummage(self):
        binary = None
        for value in sublime.load_settings("grepwin.sublime-settings").get("grepwin_binary", []):
            platform = value.get("platform", None)
            if platform is not None and platform == sublime.platform():
                binary = value.get("binary", None)
                break
        if binary is not None and not exists(binary):
            binary = None
        return binary


class GrepWin(GrepWinBase):
    def is_text_cmd(self):
        return isinstance(self, sublime_plugin.TextCommand)

    def is_win_cmd(self):
        return isinstance(self, sublime_plugin.WindowCommand)

    def get_target(self, paths=[]):
        target = None
        fail_code = NO_GREPWIN
        if len(paths):
            target = paths[0]
        elif self.is_text_cmd():
            filename = self.view.file_name()
            if filename is not None and exists(filename):
                target = filename
            else:
                self.fail(fail_code)
        else:
            self.fail(fail_code)
        return target

    def grepwin(self, paths=[]):
        target = self.get_target(paths)
        if target is None:
            return

        binary = self.get_rummage()

        if binary is not None:
            subprocess.Popen(
                [binary, "/searchpath:" + target]
            )
        else:
            self.fail(NO_TARGET)


class GrepWinFileCommand(sublime_plugin.TextCommand, GrepWin):
    def run(self, edit):
        self.grepwin()


class GrepWinFolderCommand(sublime_plugin.WindowCommand, GrepWin):
    def run(self, paths=[]):
        self.grepwin(paths)
