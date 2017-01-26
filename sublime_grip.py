"""
Github Readme GitHub Readme Instant Preview.

Licensed under MIT
Copyright (c) 2016 Isaac Muse <isaacmuse@gmail.com>
"""
import sublime
import sublime_plugin
import os
import subprocess
import urllib.request
import webbrowser

proc = None


def get_environ():
    """Get environment and force utf-8."""

    import os
    env = {}
    env.update(os.environ)

    if sublime.platform() != 'windows':
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


class GripKillCommand(sublime_plugin.ApplicationCommand):
    """Command to kill last process."""

    def run(self):
        """Run command."""
        kill_process()


class GripCommand(sublime_plugin.TextCommand):
    """Run grip."""

    def run(self, edit, livereload=False):
        """Run command."""

        global proc
        # Kill running process
        kill_process()
        proc = None

        settings = sublime.load_settings('sublime-grip.sublime-settings')
        port = settings.get('port', '6419')
        timeout = settings.get('timeout', 5)

        # Get auth token
        oauth_token = settings.get('oauth_token', None)
        if not isinstance(oauth_token, str):
            oauth_token = None

        # Prepare command
        file_name = self.view.file_name()
        cmd = [settings.get('grip_exe').get(sublime.platform())]
        assert os.path.exists(cmd[0]), "Can't find grip!"
        if not livereload:
            cmd.append("--norefresh")

        if oauth_token:
            cmd += ["--pass", oauth_token]

        if file_name is not None and os.path.exists(file_name):
            cmd.append(file_name)
            cmd.append(port)
            text = None
        else:
            cmd.append('--title=Untitled - Grip ')
            cmd.append('-')
            cmd.append(port)
            text = self.view.substr(sublime.Region(0, self.view.size()))

        p = get_process(cmd)

        # Send input if executing on buffer
        if text is not None:
            p.stdin.write(text.encode('utf-8'))
        p.stdin.close()
        proc = p
        sublime.set_timeout(lambda: check_status(timeout, port), 2000)


def get_process(cmd):
    """Execute command."""
    if sublime.platform() == "windows":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(
            cmd,
            startupinfo=startupinfo,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=get_environ()
        )
    else:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=get_environ()
        )
    return p


def check_status(count, port):
    """Check status."""

    if proc.poll() is not None:
        print('GripLive: Process died :(')
        return

    try:
        if urllib.request.urlopen("http://localhost:%s" % port).getcode() == 200:
            webbrowser.open('http://localhost:%s' % port)
            return
    except Exception:
        pass

    if count:
        count -= 1
        sublime.set_timeout(lambda: check_status(count, port), 2000)
    else:
        print('GripLive: Process timed out :(')
        kill_process()


def kill_process():
    """Kill the last process (if there is one)."""

    if sublime.platform() == "windows":
        cmd = ['taskkill', '/f', '/t', '/im', 'grip.exe']
        p = get_process(cmd)
        p.communicate()
    else:
        cmd = ['pkill', '-f', r'[pP]ython.*grip']
        p = get_process(cmd)
        p.communicate()


def plugin_loaded():
    """Kill process on load (if process exists)."""

    kill_process()


def plugin_unloaded():
    """Kill process on unload (if process exists)."""

    kill_process()
