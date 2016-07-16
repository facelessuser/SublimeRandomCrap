"""Github Readme GitHub Readme Instant Preview."""
import sublime
import sublime_plugin
import os
import subprocess

# Don't redefine proc if it already exists.
if 'proc' not in globals():
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
        setting = sublime.load_settings('sublime-grip.sublime-settings')
        file_name = self.view.file_name()
        if file_name is not None and os.path.exists(file_name):
            # Kill running process
            if proc is not None:
                kill_process()

            # Prepare command
            cmd = setting.get('python_cmd')
            cmd += ["-m", "grip"]
            if not livereload:
                cmd.append("--norefresh")
            cmd.append('-b')
            cmd.append(file_name)

            # Execute command
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

            # Save proc for livereload
            proc = p


def kill_process():
    """Kill the last process (if there is one)."""

    global proc
    if proc is not None:
        proc.kill()
        proc = None


def plugin_loaded():
    """Kill process on load (if process exists)."""

    kill_process()


def plugin_unloaded():
    """Kill process on unload (if process exists)."""

    kill_process()
