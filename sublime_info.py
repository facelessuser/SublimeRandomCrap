import socket
import sublime
import sublime_plugin

INFO = \
'''
Platform:        %(platform)s
Hostname:        %(hostname)s
Sublime Version: %(version)s
Architecture:    %(arch)s
IP:              %(ip)s
'''


class SublimeInfoCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        info = {
            "platform": sublime.platform(),
            "hostname": socket.gethostname().lower(),
            "version":  sublime.version(),
            "arch":     sublime.arch(),
            "ip":       socket.gethostbyname(socket.gethostname())
        }

        msg = INFO % info

        # Show in a dialog, console, and copy to clipboard
        sublime.message_dialog(msg)
        sublime.set_clipboard(msg)
        print("\nSublimeInfo: %s" % msg)
