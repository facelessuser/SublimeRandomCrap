"""Popup test module."""
import sublime
import sublime_plugin
import mdpopups

test_content = '''
# H1
## H2
### H3
#### H4
##### H5
###### H6
Testing **bold** text and testing *italic* text.
Testing autolink: www.google.com.
Testing inline `code`.

    Testing indented code blocks

```
Testing a fenced block.
```

> Testing
> Blockquotes

Testing
:   Description

    Lists

- Testing lists
    - Testing lists
    - Testing lists

- Testing ordered lists (ST will not show numbers :()
    1. Testing lists
    2. Testing lists

- **Test** inline highlight ```:::python yield 0, '<code class="%s">' % self.cssclass```.
- *Test* fenced highlight

    ```python
    class SublimeInlineHtmlFormatter(HtmlFormatter):
    """Format the code blocks."""

    def wrap(self, source, outfile):
        """Overload wrap."""

        return self._wrap_code(source)
    ```

---

!!! danger "Tip"
    Testing, admonition blocks.

!!! tip "Tip"
    Testing, admonition blocks.

!!! attention "Tip"
    Testing, admonition blocks.

!!! caution "Tip"
    Testing, admonition blocks.

!!! danger "Tip"
    Testing, admonition blocks.

!!! note "Tip"
    Testing, admonition blocks.
'''


class MdPopupTestCommand(sublime_plugin.TextCommand):
    """Markdown Popup Test Command."""

    def run(self, edit, st_highlight=False):
        """Run command."""

        settings = sublime.load_settings('Preferences.sublime-settings')
        original = settings.get('mdpopups_use_sublime_highlighter', False)
        if not st_highlight:
            settings.set('mdpopups_use_sublime_highlighter', False)
        else:
            settings.set('mdpopups_use_sublime_highlighter', True)
        mdpopups.show_popup(
            self.view, test_content,
            max_width=700, max_height=500,
        )
        settings.set('mdpopups_use_sublime_highlighter', original)
