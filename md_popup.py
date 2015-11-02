"""
Markdown popup.

A markdown tooltip for SublimeText.
"""
import sublime
import markdown
from . import file_strip
import traceback


class MdWrapper(markdown.Markdown):
    """
    Wrapper around Python Markdown's class.

    This allows us to gracefully continue when a module doesn't load.
    """

    Meta = {}

    def __init__(self, *args, **kwargs):
        """Call original init."""

        super(MdWrapper, self).__init__(*args, **kwargs)

    def registerExtensions(self, extensions, configs):  # noqa
        """
        Register extensions with this instance of Markdown.

        Keyword arguments:

        * extensions: A list of extensions, which can either
           be strings or objects.  See the docstring on Markdown.
        * configs: A dictionary mapping module names to config options.

        """

        from markdown import util
        from markdown.extensions import Extension

        for ext in extensions:
            try:
                if isinstance(ext, util.string_type):
                    ext = self.build_extension(ext, configs.get(ext, {}))
                if isinstance(ext, Extension):
                    ext.extendMarkdown(self, globals())
                    # print(
                    #     'Successfully loaded extension "%s.%s".'
                    #     % (ext.__class__.__module__, ext.__class__.__name__)
                    # )
                elif ext is not None:
                    raise TypeError(
                        'Extension "%s.%s" must be of type: "markdown.Extension"'
                        % (ext.__class__.__module__, ext.__class__.__name__)
                    )
            except Exception:
                # We want to gracefully continue even if an extension fails.
                print(str(traceback.format_exc()))
                continue

        return self


def get_css(css_file):
    """
    Get css file.

    Strip out comments and carriage returns.
    """

    css = ''
    try:
        css = file_strip.comments.Comments('css').strip(
            sublime.load_resource(css_file).replace('\r', '')
        )
    except Exception as e:
        print(e)
        pass
    return css


def show_popup(
    view, content, md=True, location=-1,
    max_width=320, max_height=240,
    on_navigate=None, on_hide=None,
    css=None
):
    """Parse the color scheme if needed and show the styled pop-up."""

    extensions = [
        "markdown.extensions.attr_list",
        "markdown.extensions.codehilite",
        "SublimeRandomCrap.mdx.superfences",
        "SublimeRandomCrap.mdx.betterem",
        "SublimeRandomCrap.mdx.magiclink",
        "SublimeRandomCrap.mdx.inlinehilite",
        "markdown.extensions.nl2br",
        "markdown.extensions.admonition"
    ]

    configs = {
        "SublimeRandomCrap.mdx.inlinehilite": {
            "style_plain_text": True,
            "css_class": "inlinehilite",
            "use_codehilite_settings": False,
            "guess_lang": False
        },
        "markdown.extensions.codehilite": {
            "guess_lang": False
        }
    }

    if md:
        content = MdWrapper(
            extensions=extensions,
            extension_configs=configs,
        ).convert(content).replace('&quot;', '"').replace('\n', '')

    html = "<style>%s</style>" % css if css else ''
    html += '<div class="content">%s</div>' % content

    view.show_popup(
        html, location=location, max_width=max_width,
        max_height=max_height, on_navigate=on_navigate, on_hide=on_hide
    )
