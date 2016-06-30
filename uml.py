import sublime
import sublime_plugin
import io
import os
import subprocess
import base64
import tempfile

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



class UmlCommand(sublime_plugin.TextCommand):

    plantuml = packages_path('Packages/SublimeRandomCrap/plantuml.jar')

    def run(self, edit):

        self.view.erase_phantoms("uml")
        self.snippets = []
        for region in  self.view.find_all(r'^@startuml[\s\S]*?@enduml'):
            self.snippets.append((self.view.substr(region).encode('utf-8'), region))

        sublime.set_timeout_async(self.render, 100)


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

        for snippet, region in self.snippets:
            print(snippet)
            with TempFile() as png:
                if sublime.platform() == "windows":
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    process = subprocess.Popen(
                        cmd,
                        startupinfo=startupinfo,
                        stdin=subprocess.PIPE,
                        stdout=png,
                        shell=False
                    )
                else:
                    process = subprocess.Popen(
                        cmd,
                        stdin=subprocess.PIPE,
                        stdout=png,
                        shell=False
                    )

                process.communicate(input=snippet)

                png.file.seek(0)

                if process.returncode:
                    phantom = '<span class="invalid">Conversion failed!</span>'
                else:
                    phantom = '<img src="data:image/png;base64,%s">' % base64.b64encode(png.file.read()).decode('ascii')

                sublime.set_timeout(
                    lambda phantom=phantom, region=sublime.Region(region.begin(), region.end() - 7):
                        self.add_phantom(phantom, region),
                    500
                )

    def add_phantom(self, phantom, region):

        self.view.add_phantom(
            "uml",
            region,
            phantom,
            sublime.LAYOUT_BLOCK
        )
