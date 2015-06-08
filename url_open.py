"""
Overrides the default url open plugin command in Sublime Text.

This gives me control over the regex so I can imrpove it over time.
"""
import sublime_plugin
import webbrowser
import re

rex = re.compile(
    r'''(?x)(?i)
    \b(?:
        https?://(?:(?:[a-z\d\-_]+(?:\.[a-z\d\-._]+)+)|localhost)|  # http://
        w{3}\.[a-z\d\-_]+(?:\.[a-z\d\-._]+)+                        # www.
    )
    /?[a-z\d\-._?,!'(){}\[\]/+&@%$#=:"|~;]*                         # url path and querry stuff
    [a-z\d\-_~/#@$*+=]                                              # allowed end chars
    '''
)


class OpenContextUrlCommand(sublime_plugin.TextCommand):

    """Open the URL from the context menu."""

    def run(self, edit, event):
        """Run the command."""

        url = self.find_url(event)
        webbrowser.open_new_tab(url)

    def is_visible(self, event):
        """Check if command should be visible in the context menu."""

        return self.find_url(event) is not None

    def find_url(self, event):
        """Check if cursor is on a URL."""

        pt = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(pt)

        line.a = max(line.a, pt - 1024)
        line.b = min(line.b, pt + 1024)

        text = self.view.substr(line)

        it = rex.finditer(text)

        for match in it:
            if match.start() <= (pt - line.a) and match.end() >= (pt - line.a):
                url = text[match.start():match.end()]
                if url[0:3] == "www":
                    return "http://" + url
                else:
                    return url

        return None

    def description(self, event):
        """Show the URL in the command description."""
        url = self.find_url(event)
        if len(url) > 64:
            url = url[0:64] + "..."
        return "Open " + url

    def want_event(self):
        """Check if event wanted."""

        return True
