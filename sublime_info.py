"""
SublimeInfo Sublime Plugin

Show info about the system and the current Sublime Text instance.

```js
    //////////////////////////////////
    // Info Commands
    //////////////////////////////////
    {
        "caption": "Sublime Info",
        "command": "sublime_info"
    },
```

Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
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
