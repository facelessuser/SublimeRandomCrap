import socket
import sublime
import sublime_plugin
import urllib.request as urllibReq
import traceback


INFO = '''
Platform:        %(platform)s
Hostname:        %(hostname)s
Sublime Version: %(version)s
Architecture:    %(arch)s
IP:              %(ip)s
External IP:     %(e_ip)s
'''


def external_ip():
    e_ip = "???"
    try:
        with urllibReq.urlopen("http://myip.dnsdynamic.org/") as url:
            e_ip = url.read().decode("utf-8")
    except:
        print(traceback.format_exc())
    return e_ip


class SublimeInfoCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        info = {
            "platform": sublime.platform(),
            "hostname": socket.gethostname().lower(),
            "version": sublime.version(),
            "arch": sublime.arch(),
            "ip": socket.gethostbyname(socket.gethostname()),
            "e_ip": external_ip()
        }

        msg = INFO % info

        # Show in a dialog, console, and copy to clipboard
        sublime.message_dialog(msg)
        sublime.set_clipboard(msg)
        print("\nSublimeInfo: %s" % msg)
