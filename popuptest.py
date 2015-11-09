"""Popup test module."""
import sublime_plugin
import mdpopups

test_content2 ='''

- **Test** inline highlight ```:::python yield 0, '<code class="%s">' % self.cssclass```.
- *Test* fenced highlight

    ```html
    <span style="color: #FFCC66;">SublimeInlineHtmlFormatter</span>
    ```

    ```python
    class SublimeInlineHtmlFormatter(HtmlFormatter):
    """Format the code blocks."""

    def wrap(self, source, outfile):
        """Overload wrap."""

        return self._wrap_code(source)
    ```

    ```js hl_lines="1 3"
    function isUndef(obj) {
      return obj === void 0;
    }

    function isNull(obj) {
      return obj === null;
    }
    ```

'''

insert_text = '''function isUndef(obj) {
  return obj === void 0;
}

function isNull(obj) {
  return obj === null;
}
'''

test_content = '''
# Testing Headers

Testing **bold** text and testing *italic* text. Testing a link: www.google.com.  Testing inline `code`.

```
Testing a fenced block.

Testing a fenced block.
```

> Testing
> Blockquotes

Testing
:   Description

    Lists

![Testing images](res://Packages/ColorHelper/tt_theme/images/back_dark.png)
[Testing sublime href commands](sublime:whatever;3)

- Testing lists
    - Testing lists
    - Testing lists

- Testing lists
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

    def _wrap_code(self, source):
        """
        Wrap the pygmented code.

        Sublime popups don't really support 'code', but since it doesn't
        hurt anything, we leave it in for the possiblity of future support.
        We get around the lack of proper 'code' support by converting any
        spaces after the intial space to nbsp.  We go ahead and convert tabs
        to 4 spaces as well.
        """

        yield 0, '<code class="%s">' % self.cssclass
        for i, t in source:
            text = ''
            matched = False
            for m in html_re.finditer(t):
                matched = True
                if m.group(1):
                    text += m.group(1)
                elif m.group(3):
                    text += m.group(3)
                else:
                    text += multi_space.sub(
                        replace_nbsp, m.group(2).replace('\t', ' ' * 4)
                    ).replace('&#39;', '\'').replace('&quot;', '"')
            if not matched:
                text = multi_space.sub(
                    replace_nbsp, t.replace('\t', ' ' * 4)
                ).replace('&#39;', '\'').replace('&quot;', '"')
            yield i, text
        yield 0, '</code>'
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

more = '''
'''


class MdPopupTestCommand(sublime_plugin.TextCommand):
    """Markdown Popup Test Command."""

    def run(self, edit):
        """Run command."""

        mdpopups.show_popup(
            self.view, test_content2, css=more,
            max_width=700, max_height=500,
        )
