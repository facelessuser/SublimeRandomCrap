"""Popup test module."""
import sublime_plugin
from . import md_popup


test_content = '''

### Header

Here is some text **bold** text and *italic* text. And a link: www.google.com.  And some inline normal inline `backtic`.

> Block quotes?
> Yup!

![image](res://Packages/ColorHelper/tt_theme/images/back_dark.png)
[test](sublime:whatever;3)

- **Test** inline highlight ```:::python import whatever```.
- *Test* fenced highlight

    ```python
    import sublime
    import sublime_plugin
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name
    from pygments.formatters import find_formatter_class
    import re
    import markdown
    ```

!!! tip "Tip"
    Here is a tip, `admonition` blocks are great!.
'''


class MdPopupTestCommand(sublime_plugin.TextCommand):
    """Markdown Popup Test Command."""

    def run(self, edit):
        """Run command."""

        css = md_popup.get_css('Packages/SublimeRandomCrap/themes/dark.css')
        md_popup.show_popup(
            self.view, test_content, css=css,
            max_width=700, max_height=500,
        )
