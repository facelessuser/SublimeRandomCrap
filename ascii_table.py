import sublime_plugin


ASCII_INFO = {
    0: {"char": "NUL", "info": "(null)"},
    1: {"char": "SOH", "info": "(start of heading)"},
    2: {"char": "STX", "info": "(start of text)"},
    3: {"char": "ETX", "info": "(end of text)"},
    4: {"char": "EOT", "info": "(end of transmission)"},
    5: {"char": "ENQ", "info": "(enquiry)"},
    6: {"char": "ACK", "info": "(acknowledge)"},
    7: {"char": "BEL", "info": "(bell)"},
    8: {"char": "BS", "info": "(backspace)"},
    9: {"char": "TAB", "info": "(horizontal tab)"},
    10: {"char": "LF", "info": "(line feed)"},
    11: {"char": "VT", "info": "(vertical tab)"},
    12: {"char": "FF", "info": "(form feed)"},
    13: {"char": "CR", "info": "(carriage return)"},
    14: {"char": "SO", "info": "(shift out)"},
    15: {"char": "SI", "info": "(shift in)"},
    16: {"char": "DLE", "info": "(data link escape)"},
    17: {"char": "DC1", "info": "(device control 1)"},
    18: {"char": "DC2", "info": "(device control 2)"},
    19: {"char": "DC3", "info": "(device control 3)"},
    20: {"char": "DC4", "info": "(device control 4)"},
    21: {"char": "NAK", "info": "(negative acknowledge)"},
    22: {"char": "SYN", "info": "(synchronous idle)"},
    23: {"char": "ETB", "info": "(end of transmission block)"},
    24: {"char": "CAN", "info": "(cancel)"},
    25: {"char": "EM", "info": "(endo of medium)"},
    26: {"char": "SUB", "info": "(substitute)"},
    27: {"char": "ESC", "info": "(escape)"},
    28: {"char": "FS", "info": "(file separator)"},
    29: {"char": "GS", "info": "(group separator)"},
    30: {"char": "RS", "info": "(record separator)"},
    31: {"char": "US", "info": "(unit separator)"},
    32: {"char": "SPACE"},
    127: {"char": "DEL", "info": "(delete)"}
}

ASCII_HEADER = "DEC    HEX     OCT        CHR    INFO\n"
ASCII_LINE = "%3d    0x%02x    0o%03o    % 5s%s"


def display_ascii(code):
    """
    Format and return ascii line
    """

    entry = ASCII_INFO.get(code, {"char": chr(code)})
    char = entry["char"]
    info = ("    " + entry.get("info", "")).rstrip()
    return ASCII_LINE % (
        code,  # decimal
        code,  # hex
        code,  # octal
        char,  # char
        info   # info
    )


class AsciiTableWriteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, ASCII_HEADER + '\n'.join([display_ascii(x) for x in range(0, 128)]))


class AsciiTableCommand(sublime_plugin.WindowCommand):
    def run(self):
        for view in self.window.views():
            if view.settings().get("ascii_table_view", False):
                self.window.focus_view(view)
                return

        view = self.window.new_file()
        if view is not None:
            view.run_command("ascii_table_write")
            view.set_read_only(True)
            view.set_scratch(True)
            view.set_name(".ascii_table")
            view.settings().set("ascii_table_view", True)
            view.set_syntax_file("Packages/SublimeRandomCrap/ascii_table.hidden-tmLanguage")
