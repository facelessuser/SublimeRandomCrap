import sublime_plugin

DEC = 0
HEX = 1
OCT = 2
CHR = 3
INF = 4


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
    34: {"info": "Double quotes (or speech marks)"},
    35: {"info": "Number"},
    36: {"info": "Dollar"},
    37: {"info": "Procenttecken"},
    38: {"info": "Ampersand"},
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
    60: {"info": "Less than (or open angled bracket)"},
    61: {"info": "Equals"},
    62: {"info": "Greater than (or close angled bracket)"},
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
    128: {"char": "€", "info": "Euro sign"},
    # 129: {"char": " ", "info": " "},
    130: {"char": "‚", "info": "Single low-9 quotation mark"},
    131: {"char": "ƒ", "info": "Latin small letter f with hook"},
    132: {"char": "„", "info": "Double low-9 quotation mark"},
    133: {"char": "…", "info": "Horizontal ellipsis"},
    134: {"char": "†", "info": "Dagger"},
    135: {"char": "‡", "info": "Double dagger"},
    136: {"char": "ˆ", "info": "Modifier letter circumflex accent"},
    137: {"char": "‰", "info": "Per mille sign"},
    138: {"char": "Š", "info": "Latin capital letter S with caron"},
    139: {"char": "‹", "info": "Single left-pointing angle quotation"},
    140: {"char": "Œ", "info": "Latin capital ligature OE"},
    # 141: {"char": " ", "info": " "},
    142: {"char": "Ž", "info": "Latin captial letter Z with caron"},
    # 143: {"char": " ", "info": " "},
    # 144: {"char": " ", "info": " "},
    145: {"char": "‘", "info": "Left single quotation mark"},
    146: {"char": "’", "info": "Right single quotation mark"},
    147: {"char": "“", "info": "Left double quotation mark"},
    148: {"char": "”", "info": "Right double quotation mark"},
    149: {"char": "•", "info": "Bullet"},
    150: {"char": "–", "info": "En dash"},
    151: {"char": "—", "info": "Em dash"},
    152: {"char": "˜", "info": "Small tilde"},
    153: {"char": "™", "info": "Trade mark sign"},
    154: {"char": "š", "info": "Latin small letter S with caron"},
    155: {"char": "›", "info": "Single right-pointing angle quotation mark"},
    156: {"char": "œ", "info": "Latin small ligature oe"},
    # 157: {"char": " ", "info": " "},
    158: {"char": "ž", "info": "Latin small letter z with caron"},
    159: {"char": "Ÿ", "info": "Latin capital letter Y with diaeresis"},
    160: {"char": " ", "info": "Non-breaking space"},
    161: {"char": "¡", "info": "Inverted exclamation mark"},
    162: {"char": "¢", "info": "Cent sign"},
    163: {"char": "£", "info": "Pound sign"},
    164: {"char": "¤", "info": "Currency sign"},
    165: {"char": "¥", "info": "Yen sign"},
    166: {"char": "¦", "info": "Pipe, Broken vertical bar"},
    167: {"char": "§", "info": "Section sign"},
    168: {"char": "¨", "info": "Spacing diaeresis - umlaut"},
    169: {"char": "©", "info": "Copyright sign"},
    170: {"char": "ª", "info": "Feminine ordinal indicator"},
    171: {"char": "«", "info": "Left double angle quotes"},
    172: {"char": "¬", "info": "Not sign"},
    173: {"char": "\xad", "info": "Soft hyphen"},
    174: {"char": "®", "info": "Registered trade mark sign"},
    175: {"char": "¯", "info": "Spacing macron - overline"},
    176: {"char": "°", "info": "Degree sign"},
    177: {"char": "±", "info": "Plus-or-minus sign"},
    178: {"char": "²", "info": "Superscript two - squared"},
    179: {"char": "³", "info": "Superscript three - cubed"},
    180: {"char": "´", "info": "Acute accent - spacing acute"},
    181: {"char": "µ", "info": "Micro sign"},
    182: {"char": "¶", "info": "Pilcrow sign - paragraph sign"},
    183: {"char": "·", "info": "Middle dot - Georgian comma"},
    184: {"char": "¸", "info": "Spacing cedilla"},
    185: {"char": "¹", "info": "Superscript one"},
    186: {"char": "º", "info": "Masculine ordinal indicator"},
    187: {"char": "»", "info": "Right double angle quotes"},
    188: {"char": "¼", "info": "Fraction one quarter"},
    189: {"char": "½", "info": "Fraction one half"},
    190: {"char": "¾", "info": "Fraction three quarters"},
    191: {"char": "¿", "info": "Inverted question mark"},
    192: {"char": "À", "info": "Latin capital letter A with grave"},
    193: {"char": "Á", "info": "Latin capital letter A with acute"},
    194: {"char": "Â", "info": "Latin capital letter A with circumflex"},
    195: {"char": "Ã", "info": "Latin capital letter A with tilde"},
    196: {"char": "Ä", "info": "Latin capital letter A with diaeresis"},
    197: {"char": "Å", "info": "Latin capital letter A with ring above"},
    198: {"char": "Æ", "info": "Latin capital letter AE"},
    199: {"char": "Ç", "info": "Latin capital letter C with cedilla"},
    200: {"char": "È", "info": "Latin capital letter E with grave"},
    201: {"char": "É", "info": "Latin capital letter E with acute"},
    202: {"char": "Ê", "info": "Latin capital letter E with circumflex"},
    203: {"char": "Ë", "info": "Latin capital letter E with diaeresis"},
    204: {"char": "Ì", "info": "Latin capital letter I with grave"},
    205: {"char": "Í", "info": "Latin capital letter I with acute"},
    206: {"char": "Î", "info": "Latin capital letter I with circumflex"},
    207: {"char": "Ï", "info": "Latin capital letter I with diaeresis"},
    208: {"char": "Ð", "info": "Latin capital letter ETH"},
    209: {"char": "Ñ", "info": "Latin capital letter N with tilde"},
    210: {"char": "Ò", "info": "Latin capital letter O with grave"},
    211: {"char": "Ó", "info": "Latin capital letter O with acute"},
    212: {"char": "Ô", "info": "Latin capital letter O with circumflex"},
    213: {"char": "Õ", "info": "Latin capital letter O with tilde"},
    214: {"char": "Ö", "info": "Latin capital letter O with diaeresis"},
    215: {"char": "×", "info": "Multiplication sign"},
    216: {"char": "Ø", "info": "Latin capital letter O with slash"},
    217: {"char": "Ù", "info": "Latin capital letter U with grave"},
    218: {"char": "Ú", "info": "Latin capital letter U with acute"},
    219: {"char": "Û", "info": "Latin capital letter U with circumflex"},
    220: {"char": "Ü", "info": "Latin capital letter U with diaeresis"},
    221: {"char": "Ý", "info": "Latin capital letter Y with acute"},
    222: {"char": "Þ", "info": "Latin capital letter THORN"},
    223: {"char": "ß", "info": "Latin small letter sharp s - ess-zed"},
    224: {"char": "à", "info": "Latin small letter a with grave"},
    225: {"char": "á", "info": "Latin small letter a with acute"},
    226: {"char": "â", "info": "Latin small letter a with circumflex"},
    227: {"char": "ã", "info": "Latin small letter a with tilde"},
    228: {"char": "ä", "info": "Latin small letter a with diaeresis"},
    229: {"char": "å", "info": "Latin small letter a with ring above"},
    230: {"char": "æ", "info": "Latin small letter ae"},
    231: {"char": "ç", "info": "Latin small letter c with cedilla"},
    232: {"char": "è", "info": "Latin small letter e with grave"},
    233: {"char": "é", "info": "Latin small letter e with acute"},
    234: {"char": "ê", "info": "Latin small letter e with circumflex"},
    235: {"char": "ë", "info": "Latin small letter e with diaeresis"},
    236: {"char": "ì", "info": "Latin small letter i with grave"},
    237: {"char": "í", "info": "Latin small letter i with acute"},
    238: {"char": "î", "info": "Latin small letter i with circumflex"},
    239: {"char": "ï", "info": "Latin small letter i with diaeresis"},
    240: {"char": "ð", "info": "Latin small letter eth"},
    241: {"char": "ñ", "info": "Latin small letter n with tilde"},
    242: {"char": "ò", "info": "Latin small letter o with grave"},
    243: {"char": "ó", "info": "Latin small letter o with acute"},
    244: {"char": "ô", "info": "Latin small letter o with circumflex"},
    245: {"char": "õ", "info": "Latin small letter o with tilde"},
    246: {"char": "ö", "info": "Latin small letter o with diaeresis"},
    247: {"char": "÷", "info": "Division sign"},
    248: {"char": "ø", "info": "Latin small letter o with slash"},
    249: {"char": "ù", "info": "Latin small letter u with grave"},
    250: {"char": "ú", "info": "Latin small letter u with acute"},
    251: {"char": "û", "info": "Latin small letter u with circumflex"},
    252: {"char": "ü", "info": "Latin small letter u with diaeresis"},
    253: {"char": "ý", "info": "Latin small letter y with acute"},
    254: {"char": "þ", "info": "Latin small letter thorn"},
    255: {"char": "ÿ", "info": "Latin small letter y with diaeresis"},
}

ASCII_HEADER = "DEC    HEX     OCT      CHR      INFO\n"
ASCII_LINE = "%-3d    0x%02x    0o%03o    %-5s%s"


def display_ascii(code):
    """
    Format and return ascii line
    """

    entry = ASCII_INFO[code]
    char = entry.get("char", chr(code))
    info = ("    (%s)" % entry.get("info", ""))
    if code == 173:
        # Soft Hyphen takes no space
        # So indent further
        info = " " + info
    return (
        ASCII_LINE % (
            code,  # decimal
            code,  # hex
            code,  # octal
            char,  # char
            info   # info
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
    elif info_type == INF:
        value = entry.get("info", "")
    return value


class AsciiTableSearchCommand(sublime_plugin.TextCommand):
    def run(self, edit, info_type):
        info_map = {
            "dec": DEC,
            "hex": HEX,
            "oct": OCT,
            "chr": CHR,
            "inf": INF
        }
        self.info_type = info_map.get(info_type)
        if self.info_type is not None:
            self.items = [get_ascii_info(x, self.info_type) for x in range(0, 256) if x in ASCII_INFO]
            if len(self.items):
                self.view.window().show_quick_panel(self.items, self.show)

    def show(self, value):
        if value != -1:
            pt = self.view.text_point(value + 1, 0)
            self.view.sel().clear()
            self.view.sel().add(pt)
            self.view.show_at_center(pt)

    def is_visible(self, info_type):
        return self.view.settings().get("ascii_table_view", False)


class AsciiTableWriteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, ASCII_HEADER + '\n'.join([display_ascii(x) for x in range(0, 256) if x in ASCII_INFO]))


class AsciiTableCommand(sublime_plugin.WindowCommand):
    def run(self):
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
            view.set_syntax_file("Packages/SublimeRandomCrap/ascii_table.hidden-tmLanguage")
