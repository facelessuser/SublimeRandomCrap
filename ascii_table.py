# -*- coding: utf-8 -*-
"""
ASCII Table Sublime Plugin.

Display an extended ascii table in Sublime for reference.  Allows searching the table for specific info.

Just define the commands below:

```js
    //////////////////////////////////
    // ASCII Table
    //////////////////////////////////
    {
        "caption": "ASCII Table: Show",
        "command": "ascii_table"
    },
    {
        "caption": "ASCII Table: Search Decimal",
        "command": "ascii_table_search",
        "args": {"info_type": "dec"}
    },
    {
        "caption": "ASCII Table: Search Hexidecimal",
        "command": "ascii_table_search",
        "args": {"info_type": "hex"}
    },
    {
        "caption": "ASCII Table: Search Octal",
        "command": "ascii_table_search",
        "args": {"info_type": "oct"}
    },
    {
        "caption": "ASCII Table: Search Character",
        "command": "ascii_table_search",
        "args": {"info_type": "chr"}
    },
    {
        "caption": "ASCII Table: Search Info",
        "command": "ascii_table_search",
        "args": {"info_type": "inf"}
    },
```

Licensed under MIT
Copyright (c) 2014-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import sublime_plugin
import sublime

USE_ST_SYNTAX = int(sublime.version()) >= 3092
ST_SYNTAX = "sublime-syntax" if USE_ST_SYNTAX else 'tmLanguage'

DEC = 0
HEX = 1
OCT = 2
CHR = 3
HTM = 4
INF = 5


ASCII_INFO = {
    0: {"char": "NUL", "info": "Null"},
    1: {"char": "SOH", "info": "Start of heading"},
    2: {"char": "STX", "info": "Start of text"},
    3: {"char": "ETX", "info": "End of text"},
    4: {"char": "EOT", "info": "End of transmission"},
    5: {"char": "ENQ", "info": "Enquiry"},
    6: {"char": "ACK", "info": "Acknowledge"},
    7: {"char": "BEL", "info": "Bell"},
    8: {"char": "BS", "info": "Backspace"},
    9: {"char": "TAB", "info": "Horizontal tab"},
    10: {"char": "LF", "info": "Line feed"},
    11: {"char": "VT", "info": "Vertical tab"},
    12: {"char": "FF", "info": "Form feed"},
    13: {"char": "CR", "info": "Carriage return"},
    14: {"char": "SO", "info": "Shift out"},
    15: {"char": "SI", "info": "Shift in"},
    16: {"char": "DLE", "info": "Data link escape"},
    17: {"char": "DC1", "info": "Device control 1"},
    18: {"char": "DC2", "info": "Device control 2"},
    19: {"char": "DC3", "info": "Device control 3"},
    20: {"char": "DC4", "info": "Device control 4"},
    21: {"char": "NAK", "info": "Negative acknowledge"},
    22: {"char": "SYN", "info": "Synchronous idle"},
    23: {"char": "ETB", "info": "End of transmission block"},
    24: {"char": "CAN", "info": "Cancel"},
    25: {"char": "EM", "info": "End of medium"},
    26: {"char": "SUB", "info": "Substitute"},
    27: {"char": "ESC", "info": "Escape"},
    28: {"char": "FS", "info": "File separator"},
    29: {"char": "GS", "info": "Group separator"},
    30: {"char": "RS", "info": "Record separator"},
    31: {"char": "US", "info": "Unit separator"},
    32: {"char": "SPACE", "info": "Space"},
    33: {"info": "Exclamation mark"},
    34: {"html_name": "quot", "info": "Double quotes (or speech marks)"},
    35: {"info": "Number"},
    36: {"info": "Dollar"},
    37: {"info": "Procenttecken"},
    38: {"html_name": "amp", "info": "Ampersand"},
    39: {"info": "Single quote"},
    40: {"info": "Open parenthesis (or open bracket)"},
    41: {"info": "Close parenthesis (or close bracket)"},
    42: {"info": "Asterisk"},
    43: {"info": "Plus"},
    44: {"info": "Comma"},
    45: {"info": "Hyphen"},
    46: {"info": "Period, dot or full stop"},
    47: {"info": "Slash or divide"},
    48: {"info": "Zero"},
    49: {"info": "One"},
    50: {"info": "Two"},
    51: {"info": "Three"},
    52: {"info": "Four"},
    53: {"info": "Five"},
    54: {"info": "Six"},
    55: {"info": "Seven"},
    56: {"info": "Eight"},
    57: {"info": "Nine"},
    58: {"info": "Colon"},
    59: {"info": "Semicolon"},
    60: {"html_name": "lt", "info": "Less than (or open angled bracket)"},
    61: {"info": "Equals"},
    62: {"html_name": "gt", "info": "Greater than (or close angled bracket)"},
    63: {"info": "Question mark"},
    64: {"info": "At symbol"},
    65: {"info": "Uppercase A"},
    66: {"info": "Uppercase B"},
    67: {"info": "Uppercase C"},
    68: {"info": "Uppercase D"},
    69: {"info": "Uppercase E"},
    70: {"info": "Uppercase F"},
    71: {"info": "Uppercase G"},
    72: {"info": "Uppercase H"},
    73: {"info": "Uppercase I"},
    74: {"info": "Uppercase J"},
    75: {"info": "Uppercase K"},
    76: {"info": "Uppercase L"},
    77: {"info": "Uppercase M"},
    78: {"info": "Uppercase N"},
    79: {"info": "Uppercase O"},
    80: {"info": "Uppercase P"},
    81: {"info": "Uppercase Q"},
    82: {"info": "Uppercase R"},
    83: {"info": "Uppercase S"},
    84: {"info": "Uppercase T"},
    85: {"info": "Uppercase U"},
    86: {"info": "Uppercase V"},
    87: {"info": "Uppercase W"},
    88: {"info": "Uppercase X"},
    89: {"info": "Uppercase Y"},
    90: {"info": "Uppercase Z"},
    91: {"info": "Opening bracket"},
    92: {"info": "Backslash"},
    93: {"info": "Closing bracket"},
    94: {"info": "Caret - circumflex"},
    95: {"info": "Underscore"},
    96: {"info": "Grave accent"},
    97: {"info": "Lowercase a"},
    98: {"info": "Lowercase b"},
    99: {"info": "Lowercase c"},
    100: {"info": "Lowercase d"},
    101: {"info": "Lowercase e"},
    102: {"info": "Lowercase f"},
    103: {"info": "Lowercase g"},
    104: {"info": "Lowercase h"},
    105: {"info": "Lowercase i"},
    106: {"info": "Lowercase j"},
    107: {"info": "Lowercase k"},
    108: {"info": "Lowercase l"},
    109: {"info": "Lowercase m"},
    110: {"info": "Lowercase n"},
    111: {"info": "Lowercase o"},
    112: {"info": "Lowercase p"},
    113: {"info": "Lowercase q"},
    114: {"info": "Lowercase r"},
    115: {"info": "Lowercase s"},
    116: {"info": "Lowercase t"},
    117: {"info": "Lowercase u"},
    118: {"info": "Lowercase v"},
    119: {"info": "Lowercase w"},
    120: {"info": "Lowercase x"},
    121: {"info": "Lowercase y"},
    122: {"info": "Lowercase z"},
    123: {"info": "Opening brace"},
    124: {"info": "Vertical bar"},
    125: {"info": "Closing brace"},
    126: {"info": "Equivalency sign - tilde"},
    127: {"char": "DEL", "info": "Delete"},
    128: {"char": "€", "html_name": "euro", "info": "Euro sign"},
    # 129: {"char": " ", "info": " "},
    130: {"char": "‚", "html_name": "sbquo", "info": "Single low-9 quotation mark"},
    131: {"char": "ƒ", "html_name": "fnof", "info": "Latin small letter f with hook"},
    132: {"char": "„", "html_name": "bdquo", "info": "Double low-9 quotation mark"},
    133: {"char": "…", "html_name": "hellip", "info": "Horizontal ellipsis"},
    134: {"char": "†", "html_name": "dagger", "info": "Dagger"},
    135: {"char": "‡", "html_name": "Dagger", "info": "Double dagger"},
    136: {"char": "ˆ", "html_name": "circ", "info": "Modifier letter circumflex accent"},
    137: {"char": "‰", "html_name": "permil", "info": "Per mille sign"},
    138: {"char": "Š", "html_name": "Scaron", "info": "Latin capital letter S with caron"},
    139: {"char": "‹", "html_name": "lsaquo", "info": "Single left-pointing angle quotation"},
    140: {"char": "Œ", "html_name": "OElig", "info": "Latin capital ligature OE"},
    # 141: {"char": " ", "info": " "},
    142: {"char": "Ž", "info": "Latin captial letter Z with caron"},
    # 143: {"char": " ", "info": " "},
    # 144: {"char": " ", "info": " "},
    145: {"char": "‘", "html_name": "lsquo", "info": "Left single quotation mark"},
    146: {"char": "’", "html_name": "rsquo", "info": "Right single quotation mark"},
    147: {"char": "“", "html_name": "ldquo", "info": "Left double quotation mark"},
    148: {"char": "”", "html_name": "rdquo", "info": "Right double quotation mark"},
    149: {"char": "•", "html_name": "bull", "info": "Bullet"},
    150: {"char": "–", "html_name": "ndash", "info": "En dash"},
    151: {"char": "—", "html_name": "mdash", "info": "Em dash"},
    152: {"char": "˜", "html_name": "tilde", "info": "Small tilde"},
    153: {"char": "™", "html_name": "trade", "info": "Trade mark sign"},
    154: {"char": "š", "html_name": "scaron", "info": "Latin small letter S with caron"},
    155: {"char": "›", "html_name": "rsaquo", "info": "Single right-pointing angle quotation mark"},
    156: {"char": "œ", "html_name": "oelig", "info": "Latin small ligature oe"},
    # 157: {"char": " ", "info": " "},
    158: {"char": "ž", "info": "Latin small letter z with caron"},
    159: {"char": "Ÿ", "html_name": "yuml", "info": "Latin capital letter Y with diaeresis"},
    160: {"char": " ", "html_name": "nbsp", "info": "Non-breaking space"},
    161: {"char": "¡", "html_name": "iexcl", "info": "Inverted exclamation mark"},
    162: {"char": "¢", "html_name": "cent", "info": "Cent sign"},
    163: {"char": "£", "html_name": "pound", "info": "Pound sign"},
    164: {"char": "¤", "html_name": "curren", "info": "Currency sign"},
    165: {"char": "¥", "html_name": "yen", "info": "Yen sign"},
    166: {"char": "¦", "html_name": "brvbar", "info": "Pipe, Broken vertical bar"},
    167: {"char": "§", "html_name": "sect", "info": "Section sign"},
    168: {"char": "¨", "html_name": "uml", "info": "Spacing diaeresis - umlaut"},
    169: {"char": "©", "html_name": "copy", "info": "Copyright sign"},
    170: {"char": "ª", "html_name": "ordf", "info": "Feminine ordinal indicator"},
    171: {"char": "«", "html_name": "laquo", "info": "Left double angle quotes"},
    172: {"char": "¬", "html_name": "not", "info": "Not sign"},
    173: {"char": "\xad", "html_name": "shy", "info": "Soft hyphen"},
    174: {"char": "®", "html_name": "reg", "info": "Registered trade mark sign"},
    175: {"char": "¯", "html_name": "macr", "info": "Spacing macron - overline"},
    176: {"char": "°", "html_name": "deg", "info": "Degree sign"},
    177: {"char": "±", "html_name": "plusmn", "info": "Plus-or-minus sign"},
    178: {"char": "²", "html_name": "sup2", "info": "Superscript two - squared"},
    179: {"char": "³", "html_name": "sup3", "info": "Superscript three - cubed"},
    180: {"char": "´", "html_name": "acute", "info": "Acute accent - spacing acute"},
    181: {"char": "µ", "html_name": "micro", "info": "Micro sign"},
    182: {"char": "¶", "html_name": "para", "info": "Pilcrow sign - paragraph sign"},
    183: {"char": "·", "html_name": "middot", "info": "Middle dot - Georgian comma"},
    184: {"char": "¸", "html_name": "cedil", "info": "Spacing cedilla"},
    185: {"char": "¹", "html_name": "sup1", "info": "Superscript one"},
    186: {"char": "º", "html_name": "ordm", "info": "Masculine ordinal indicator"},
    187: {"char": "»", "html_name": "raquo", "info": "Right double angle quotes"},
    188: {"char": "¼", "html_name": "frac14", "info": "Fraction one quarter"},
    189: {"char": "½", "html_name": "frac12", "info": "Fraction one half"},
    190: {"char": "¾", "html_name": "frac34", "info": "Fraction three quarters"},
    191: {"char": "¿", "html_name": "iquest", "info": "Inverted question mark"},
    192: {"char": "À", "html_name": "Agrave", "info": "Latin capital letter A with grave"},
    193: {"char": "Á", "html_name": "Aacute", "info": "Latin capital letter A with acute"},
    194: {"char": "Â", "html_name": "Acirc", "info": "Latin capital letter A with circumflex"},
    195: {"char": "Ã", "html_name": "Atilde", "info": "Latin capital letter A with tilde"},
    196: {"char": "Ä", "html_name": "Auml", "info": "Latin capital letter A with diaeresis"},
    197: {"char": "Å", "html_name": "Aring", "info": "Latin capital letter A with ring above"},
    198: {"char": "Æ", "html_name": "AElig", "info": "Latin capital letter AE"},
    199: {"char": "Ç", "html_name": "Ccedil", "info": "Latin capital letter C with cedilla"},
    200: {"char": "È", "html_name": "Egrave", "info": "Latin capital letter E with grave"},
    201: {"char": "É", "html_name": "Eacute", "info": "Latin capital letter E with acute"},
    202: {"char": "Ê", "html_name": "Ecirc", "info": "Latin capital letter E with circumflex"},
    203: {"char": "Ë", "html_name": "Euml", "info": "Latin capital letter E with diaeresis"},
    204: {"char": "Ì", "html_name": "Igrave", "info": "Latin capital letter I with grave"},
    205: {"char": "Í", "html_name": "Iacute", "info": "Latin capital letter I with acute"},
    206: {"char": "Î", "html_name": "Icirc", "info": "Latin capital letter I with circumflex"},
    207: {"char": "Ï", "html_name": "Iuml", "info": "Latin capital letter I with diaeresis"},
    208: {"char": "Ð", "html_name": "ETH", "info": "Latin capital letter ETH"},
    209: {"char": "Ñ", "html_name": "Ntilde", "info": "Latin capital letter N with tilde"},
    210: {"char": "Ò", "html_name": "Ograve", "info": "Latin capital letter O with grave"},
    211: {"char": "Ó", "html_name": "Oacute", "info": "Latin capital letter O with acute"},
    212: {"char": "Ô", "html_name": "Ocirc", "info": "Latin capital letter O with circumflex"},
    213: {"char": "Õ", "html_name": "Otilde", "info": "Latin capital letter O with tilde"},
    214: {"char": "Ö", "html_name": "Ouml", "info": "Latin capital letter O with diaeresis"},
    215: {"char": "×", "html_name": "times", "info": "Multiplication sign"},
    216: {"char": "Ø", "html_name": "Oslash", "info": "Latin capital letter O with slash"},
    217: {"char": "Ù", "html_name": "Ugrave", "info": "Latin capital letter U with grave"},
    218: {"char": "Ú", "html_name": "Uacute", "info": "Latin capital letter U with acute"},
    219: {"char": "Û", "html_name": "Ucirc", "info": "Latin capital letter U with circumflex"},
    220: {"char": "Ü", "html_name": "Uuml", "info": "Latin capital letter U with diaeresis"},
    221: {"char": "Ý", "html_name": "Yacute", "info": "Latin capital letter Y with acute"},
    222: {"char": "Þ", "html_name": "THORN", "info": "Latin capital letter THORN"},
    223: {"char": "ß", "html_name": "szlig", "info": "Latin small letter sharp s - ess-zed"},
    224: {"char": "à", "html_name": "agrave", "info": "Latin small letter a with grave"},
    225: {"char": "á", "html_name": "aacute", "info": "Latin small letter a with acute"},
    226: {"char": "â", "html_name": "acirc", "info": "Latin small letter a with circumflex"},
    227: {"char": "ã", "html_name": "atilde", "info": "Latin small letter a with tilde"},
    228: {"char": "ä", "html_name": "auml", "info": "Latin small letter a with diaeresis"},
    229: {"char": "å", "html_name": "aring", "info": "Latin small letter a with ring above"},
    230: {"char": "æ", "html_name": "aelig", "info": "Latin small letter ae"},
    231: {"char": "ç", "html_name": "ccedil", "info": "Latin small letter c with cedilla"},
    232: {"char": "è", "html_name": "egrave", "info": "Latin small letter e with grave"},
    233: {"char": "é", "html_name": "eacute", "info": "Latin small letter e with acute"},
    234: {"char": "ê", "html_name": "ecirc", "info": "Latin small letter e with circumflex"},
    235: {"char": "ë", "html_name": "euml", "info": "Latin small letter e with diaeresis"},
    236: {"char": "ì", "html_name": "igrave", "info": "Latin small letter i with grave"},
    237: {"char": "í", "html_name": "iacute", "info": "Latin small letter i with acute"},
    238: {"char": "î", "html_name": "icirc", "info": "Latin small letter i with circumflex"},
    239: {"char": "ï", "html_name": "iuml", "info": "Latin small letter i with diaeresis"},
    240: {"char": "ð", "html_name": "eth", "info": "Latin small letter eth"},
    241: {"char": "ñ", "html_name": "ntilde", "info": "Latin small letter n with tilde"},
    242: {"char": "ò", "html_name": "ograve", "info": "Latin small letter o with grave"},
    243: {"char": "ó", "html_name": "oacute", "info": "Latin small letter o with acute"},
    244: {"char": "ô", "html_name": "ocirc", "info": "Latin small letter o with circumflex"},
    245: {"char": "õ", "html_name": "otilde", "info": "Latin small letter o with tilde"},
    246: {"char": "ö", "html_name": "ouml", "info": "Latin small letter o with diaeresis"},
    247: {"char": "÷", "html_name": "divide", "info": "Division sign"},
    248: {"char": "ø", "html_name": "oslash", "info": "Latin small letter o with slash"},
    249: {"char": "ù", "html_name": "ugrave", "info": "Latin small letter u with grave"},
    250: {"char": "ú", "html_name": "uacute", "info": "Latin small letter u with acute"},
    251: {"char": "û", "html_name": "ucirc", "info": "Latin small letter u with circumflex"},
    252: {"char": "ü", "html_name": "uuml", "info": "Latin small letter u with diaeresis"},
    253: {"char": "ý", "html_name": "yacute", "info": "Latin small letter y with acute"},
    254: {"char": "þ", "html_name": "thorn", "info": "Latin small letter thorn"},
    255: {"char": "ÿ", "html_name": "yuml", "info": "Latin small letter y with diaeresis"},
}

ASCII_HEADER = "DEC    HEX     OCT      CHR      HTML        DESCRIPTION\n"
ASCII_LINE = "%-3d    0x%02x    0o%03o    %-5s%s    %-8s%s"


def display_ascii(code):
    """Format and return ascii line."""

    entry = ASCII_INFO[code]
    char = entry.get("char", chr(code))
    info = ("    (%s)" % entry.get("info", ""))
    html_name = entry.get("html_name", "")
    if html_name != "":
        html_name = "&%s;" % html_name

    spacer = " " if code == 173 else ""

    return (
        ASCII_LINE % (
            code,       # decimal
            code,       # hex
            code,       # octal
            char,       # char
            spacer,     # spacer
            html_name,  # html name
            info        # info
        )
    ).rstrip()


def get_ascii_info(code, info_type):
    value = None
    entry = ASCII_INFO[code]
    if info_type == DEC:
        value = str(code)
    elif info_type == HEX:
        value = hex(code)[2:]
    elif info_type == OCT:
        value = oct(code)[2:]
    elif info_type == CHR:
        value = entry.get("char", chr(code))
    elif info_type == HTM:
        value = entry.get("html_name", "")
        if value != "":
            value = "&%s;" % value
    elif info_type == INF:
        value = entry.get("info", "")
    return value


class AsciiTableSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit, info_type):
        """Find or launch an ascii table view and pop and then call actual search command."""

        if not self.view.settings().get("ascii_table_view", False):
            window = self.view.window()
            if window is not None:
                window.run_command('ascii_table')
        else:
            ascii_view = self.view

        ascii_view = window.active_view()
        if ascii_view is not None:
            ascii_view.run_command('ascii_table_view_search', {'info_type': info_type})


class AsciiTableViewSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit, info_type):
        """Show the palette search options based on info_type."""

        info_map = {
            "dec": DEC,
            "hex": HEX,
            "oct": OCT,
            "chr": CHR,
            "htm": HTM,
            "inf": INF
        }
        self.info_type = info_map.get(info_type)
        if self.info_type is not None:
            self.items = [get_ascii_info(x, self.info_type) for x in range(0, 256) if x in ASCII_INFO]
            if len(self.items):
                self.view.window().show_quick_panel(self.items, self.show)

    def show(self, value):
        """Focus the search result."""

        if value != -1:
            pt = self.view.text_point(value + 1, 0)
            self.view.sel().clear()
            self.view.sel().add(pt)
            self.view.show_at_center(pt)

    def is_enabled(self, info_type):
        """Enable only if we are in an ascii table view."""

        return self.view.settings().get("ascii_table_view", False)


class AsciiTableWriteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        """Insert table in ascii view."""

        self.view.insert(edit, 0, ASCII_HEADER + '\n'.join([display_ascii(x) for x in range(0, 256) if x in ASCII_INFO]))


class AsciiTableCommand(sublime_plugin.WindowCommand):
    def run(self):
        """Show the ascii table.  Only generate if one is not available."""

        for view in self.window.views():
            if view.settings().get("ascii_table_view", False):
                self.window.focus_view(view)
                return

        view = self.window.new_file()
        if view is not None:
            view.set_encoding("UTF-8")
            view.run_command("ascii_table_write")
            view.set_read_only(True)
            view.set_scratch(True)
            view.set_name(".ascii_table")
            view.settings().set("ascii_table_view", True)
            view.set_syntax_file("Packages/SublimeRandomCrap/ascii_table.%s" % ST_SYNTAX)
