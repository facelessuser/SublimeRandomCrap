"""Unit convert."""
import sublime_plugin
import re


IS_INT = re.compile(r'^(0|[1-9][0-9]*)$')
IS_HEX = re.compile(r'(?i)^(0x[\da-z]+)$')


def unit_converter(regex, converter, text):
    """Convert the unit."""

    converted = False
    if regex.match(text) is not None:
        try:
            text = converter(text)
            converted = True
        except Exception:
            pass
    return converted, text


class UnitConvertCommand(sublime_plugin.TextCommand):

    """Sublime unit convet command."""

    def run(self, edit, to_unit):
        """Run the command."""

        try:
            self.command = getattr(self, to_unit)
        except Exception:
            return

        for sel in reversed(self.view.sel()):
            if sel.size():
                text = self.command(self.view.substr(sel))
                self.view.replace(edit, sel, text)

    def to_hex(self, text):
        """Convert to hex."""

        status, text = unit_converter(IS_INT, lambda text: "0x%X" % int(text), text)
        return text

    def to_dec(self, text):
        """Convert to decimal."""

        status, text = unit_converter(IS_HEX, lambda text: "%d" % int(text, 16), text)
        return text
