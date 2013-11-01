import sublime
import sublime_plugin
import webbrowser


class ShowSublimeApiCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        version = int(sublime.version())
        if version >= 3000 and version < 4000:
            webbrowser.open("http://www.sublimetext.com/docs/3/api_reference.html")
        elif version >= 2000 and version < 3000:
            webbrowser.open("http://www.sublimetext.com/docs/2/api_reference.html")
        else:
            sublime.error_message("Version %d not supported" % version)
