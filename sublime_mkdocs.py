"""
Mkdocs Instant Preview.

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


class MkdocsKillCommand(sublime_plugin.ApplicationCommand):
    """Command to kill last process."""

    def run(self):
        """Run command."""
        kill_process()


class MkdocsCommand(sublime_plugin.TextCommand):
    """Run mkdocs."""

    def run(self, edit, livereload=False):
        """Run command."""
        global proc
        # Kill running process
        kill_process()
        proc = None

        settings = sublime.load_settings('sublime-mkdocs.sublime-settings')

        # Prepare command
        file_name = self.view.file_name()
        cmd = [settings.get('mkdocs_location')]
        port = settings.get('port', '8000')
        timeout = settings.get('timeout', 5)
        assert os.path.exists(cmd[0]), "Can't find mkdocs!"

        if file_name is not None and os.path.exists(file_name) and os.path.splitext(file_name)[1].lower() == '.yml':
            cmd.extend(['serve', '-f', file_name, '-a', 'localhost:%s' % port])
            if not livereload:
                cmd.append('--no-livereload')
            p = get_process(cmd, os.path.dirname(file_name))
            p.stdin.close()
            proc = p
            sublime.set_timeout(lambda: check_status(timeout, port), 0)
        else:
            print('MkDocsLive: Please provide a valid mkdocs.yml file!')


def check_status(count, port):
    """Check status."""

    if proc.poll() is not None:
        print('MkDocsLive: Process died :(')
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
        print('MkDocsLive: Process timed out :(')
        kill_process()


def get_process(cmd, cwd=None):
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
            env=get_environ(),
            cwd=cwd
        )
    else:
        p = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=get_environ(),
            cwd=cwd
        )
    return p


def kill_process():
    """Kill the last process (if there is one)."""

    if sublime.platform() == "windows":
        cmd = ['taskkill', '/f', '/t' '/im', 'mkdocs.exe']
        p = get_process(cmd)
        p.communicate()
    else:
        # TODO: add 'nix stuff here
        pass


def plugin_loaded():
    """Kill process on load (if process exists)."""

    kill_process()


def plugin_unloaded():
    """Kill process on unload (if process exists)."""

    kill_process()
