import sublime
import sublime_plugin
from os.path import basename, dirname, exists, splitext
import codecs
import subprocess
import sys
import traceback
try:
    from SubNotify.sub_notify import SubNotifyIsReadyCommand as Notify
except:
    class Notify:
        @classmethod
        def is_ready(cls):
            return False

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"


def notify(msg):
    settings = sublime.load_settings("reg_replace.sublime-settings")
    if settings.get("use_sub_notify", False) and Notify.is_ready():
        sublime.run_command("sub_notify", {"title": "Mdown", "msg": msg})
    else:
        sublime.status_message(msg)


def error(msg):
    settings = sublime.load_settings("reg_replace.sublime-settings")
    if settings.get("use_sub_notify", False) and Notify.is_ready():
        sublime.run_command("sub_notify", {"title": "Mdown", "msg": msg, "level": "error"})
    else:
        sublime.error_message("Mdown:\n%s" % msg)


def parse_file_name(file_name):
    if file_name is None or not exists(file_name):
        title = "Untitled"
        basepath = None
    else:
        title = basename(file_name)
        basepath = dirname(file_name)
    return title, basepath


class MdownInsertText(sublime_plugin.TextCommand):
    wbfr = None

    def run(self, edit, save=False):
        self.view.insert(edit, 0, MdownInsertText.wbfr)
        MdownInsertText.clear_wbfr()
        if save:
            self.view.run_command('save')

    @classmethod
    def set_wbfr(cls, text):
        cls.wbfr = text

    @classmethod
    def clear_wbfr(cls):
        cls.wbfr = None


class MdownCommand(sublime_plugin.TextCommand):
    message = "<placeholder>"

    def setup(self, alternate_settings=None):
        self.title, self.basepath = parse_file_name(self.view.file_name())
        self.binary = sublime.load_settings("mdown.sublime-settings").get("binary", {}).get(_PLATFORM, "")
        self.reject = sublime.load_settings("mdown.sublime-settings").get("critic_reject", False)
        self.settings = alternate_settings
        self.cmd = [self.binary, "--title=%s" % self.title]
        if self.basepath is not None:
            self.cmd += ["--basepath=%s" % self.basepath]
        if self.settings is not None and exists(self.settings):
            self.cmd += ["-s", self.settings]

    def convert(self, edit):
        pass

    def call(self):
        print(self.cmd)
        if _PLATFORM == "windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            p = subprocess.Popen(
                self.cmd, startupinfo=startupinfo,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        else:
            p = subprocess.Popen(
                self.cmd,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        sels = self.view.sel()
        regions = []
        if len(sels):
            for sel in sels:
                if sel.size():
                    regions.append(sel)
        if len(regions) == 0:
            regions.append(sublime.Region(0, self.view.size()))
        for region in regions:
            for line in self.view.lines(region):
                p.stdin.write((self.view.substr(line) + '\n').encode('utf-8'))
        text = p.communicate()[0].decode("utf-8")
        self.returncode = p.returncode
        return text

    def error_message(self):
        error(self.message)


class MdownPreviewCommand(MdownCommand):
    message = "mdown failed to generate html!"

    def run(self, edit, target="browser", plain=False, alternate_settings=None):
        self.setup(alternate_settings)
        self.target = target
        self.plain = plain
        if self.binary:
            self.convert(edit)

    def output(self, rbfr):
        if self.target == "browser":
            # Nothing to do
            notify("Conversion complete!\nOpening in browser...")
        elif self.target == "clipboard":
            sublime.set_clipboard(rbfr)
            notify("Conversion complete!\nResult copied to clipbaord.")
        elif self.target == "sublime":
            window = self.view.window()
            if window is not None:
                view = window.new_file()
                MdownInsertText.set_wbfr(rbfr)
                view.run_command("mdown_insert_text")
                notify("Conversion complete!\nResult exported to Sublime.")
            else:
                error("Could not export!\nView has no window")
        elif self.target == "save":
            save_location = self.view.file_name()
            if save_location is None or not exists(save_location):
                # Save as...
                window = self.view.window()
                if window is not None:
                    view = window.new_file()
                    if view is not None:
                        MdownInsertText.set_wbfr(rbfr)
                        view.run_command("mdown_insert_text", {"save": True})
                        notify("Conversion complete!\nReady to save...")
                    else:
                        error("Failed to create new view!")
                else:
                    error("Could not save!\nView has no window")
            else:
                # Save
                htmlfile = splitext(save_location)[0] + '.html'
                try:
                    with codecs.open(htmlfile, "w", encoding="utf-8") as f:
                        f.write(rbfr)
                    notify("Conversion complete!\nHtml saved.")
                except:
                    print(traceback.format_exc())
                    error("Failed to save file!")

    def convert(self, edit):
        if self.target == "browser":
            self.cmd.append("-p")
        else:
            self.cmd.append("-q")

        if self.plain:
            self.cmd.append("-P")

        if self.reject:
            self.cmd.append("-r")
        else:
            self.cmd.append('-a')

        rbfr = self.call()

        if self.returncode:
            if self.target == "browser":
                print(rbfr)
            self.error_message()
        else:
            self.output(rbfr)


class MdownCriticPreviewCommand(MdownCommand):
    message = "mdown failed to generate your preview!"

    def run(self, edit, alternate_settings=None):
        self.setup(alternate_settings)
        if self.binary:
            self.convert(edit)

    def convert(self, edit):
        self.cmd.append("-p")
        self.cmd.append("-c")

        print(self.call())
        if self.returncode:
            self.error_message()
        else:
            notify("Conversion complete!\nOpening in browser...")


class MdownCriticStripCommand(MdownCommand):
    message = "mdown failed to strip your critic comments!"

    def run(self, edit, reject=False, alternate_settings=None):
        self.setup(alternate_settings)
        self.reject = reject
        if self.binary:
            self.convert(edit)

    def convert(self, edit):
        self.cmd += ["--critic-dump", "-p", "-q"]
        if self.reject:
            self.cmd.append("-r")
        else:
            self.cmd.append("-a")

        text = self.call()
        if self.returncode:
            self.error_message()
        else:
            self.view.replace(edit, sublime.Region(0, self.view.size()), text)
            notify("Critic stripping succesfully completed!")
