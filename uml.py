"""
@startuml
bob -> kate
@enduml
"""
import sublime
import sublime_plugin
import io
import os
import subprocess
import base64
import tempfile
import mdpopups
import re

PLANTUML = 'Packages/SublimeRandomCrap/plantuml.jar'


def packages_path(pth):
    """Get packages path."""

    return os.path.join(os.path.dirname(sublime.packages_path()), os.path.normpath(pth))


class TempFile(object):
    """Open either a temporary HTML or one at the save location."""

    def __enter__(self):
        """Setup HTML file."""

        self.file = tempfile.NamedTemporaryFile(mode='bw+', delete=True, suffix='png')
        return self.file

    def __exit__(self, type, value, traceback):
        """Tear down HTML file."""

        self.file.close()


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


class UmlCommand(sublime_plugin.TextCommand):

    plantuml = packages_path('Packages/SublimeRandomCrap/plantuml.jar')

    def run(self, edit):
        for x in range(self.view.settings().get('uml.regions', 0)):
            self.view.erase_regions("uml%d" % x)
        self.view.settings().set('uml.regions', 0)
        mdpopups.erase_phantoms(self.view, "uml")
        self.snippets = []
        count = 0
        for region in  self.view.find_all(r'@startuml[\s\S]*?@enduml|@startdot[\s\S]*?@enddot|@startditaa[\s\S]*?@endditaa'):
            self.snippets.append(self.view.substr(region).encode('utf-8'))
            self.view.add_regions(
                "uml%d" %  count,
                [region],
                "",
                "",
                sublime.HIDDEN
            )
            count += 1
        self.view.settings().set('uml.regions', count)

        sublime.set_timeout_async(self.render, 100)

    def escape_code(self, text, tab_size=4):
        """Format text to HTML."""

        encode_table = {
            '&': '&amp;',
            '>': '&gt;',
            '<': '&lt;',
            '\t': ' ' * tab_size,
            '\n': '<br>'
        }

        return re.sub(
            r'(?!\s($|\S))\s',
            '&nbsp;',
            ''.join(
                encode_table.get(c, c) for c in text
            )
        )

    def render(self):

        cmd = [
            'java',
            '-splash:no',
            '-jar',
            self.plantuml,
            '-pipe',
            '-tpng'
            '-charset',
            'UTF-8'
        ]

        count = 0
        for snippet in self.snippets:
            print(snippet)
            with TempFile() as png:
                if sublime.platform() == "windows":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    process = subprocess.Popen(
                        cmd,
                        startupinfo=startupinfo,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        stdout=png,
                        shell=True,
                        env=get_environ()
                    )
                else:
                    process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        stdout=png,
                        shell=True,
                        env=get_environ()
                    )

                output = process.communicate(input=snippet)

                png.file.seek(0)

                if process.returncode:
                    phantom = '<span class="invalid">Conversion failed!</span>\n\n<hr>\n\n<div class="highlight"><pre>%s</pre></div>\n' % (
                        self.escape_code(png.file.read().decode('utf-8'))
                    )
                else:
                    with open('c:\\test%d.png' % count, 'wb') as f:
                        f.write(png.file.read())
                    png.file.seek(0)
                    phantom = '<img src="data:image/png;base64,%s"/>' % base64.b64encode(png.file.read()).decode('ascii')

                sublime.set_timeout(
                    lambda phantom=phantom, index=count:
                        self.add_phantom(phantom, index),
                    500
                )
            count += 1

    def add_phantom(self, phantom, index):

        key = 'uml%d' % index
        regions = self.view.get_regions(key)

        if regions:
            mdpopups.add_phantom(
                self.view,
                "uml",
                regions[0],
                phantom,
                0,
                md=False,
            )
        self.view.erase_regions(key)
        self.view.settings().set('uml.regions', self.view.settings().get('uml.regions', 0) - 1)
