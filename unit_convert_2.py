import sublime_plugin
import sublime
import re


IS_INT = re.compile(r'^(0|[1-9][0-9]*)$')
IS_HEX = re.compile(r'(?i)^(0x[\da-z]+)$')
IS_BIN = re.compile(r'(?i)^(0b[0-1])$')


def unit_converter(regex, converter, text):
    converted = False
    if regex.match(text) is not None:
        try:
            text = converter(text)
            converted = True
        except:
            pass
    return converted, text


class UnitConvertCommand(sublime_plugin.TextCommand):
    def run(self, edit, to_unit):
        try:
            self.command = getattr(self, to_unit)
        except:
            return

        for sel in reversed(self.view.sel()):
            if sel.size():
                text = self.command(self.view.substr(sel))
                self.view.replace(edit, sel, text)

    def to_hex(self, text):
        status, text = unit_converter(IS_INT, lambda text: "0x%X" % int(text), text)
        if not status:
            status, text = unit_converter(IS_BIN, lambda text: "0x%X" % int(text, 2), text)
        return text

    def to_dec(self, text):
        status, text = unit_converter(IS_HEX, lambda text: "%d" % int(text, 16), text)
        if not status:
            status, text = unit_converter(IS_BIN, lambda text: "%s" % int(text, 2), text)
        return text

    def to_bin(self, text):
        status, text = unit_converter(IS_INT, lambda text: "%s" % bin(int(text)), text)
        if not status:
            status, text = unit_converter(IS_HEX, lambda text: "%s" % bin(int(text, 16)), text)
