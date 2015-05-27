#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Isaac Muse
# Copyright (c) 2015 Isaac Muse
#
# License: MIT
#

"""This module exports the Prospector plugin class."""

from SublimeLinter.lint import Linter, util, persist
import os
import re
from functools import lru_cache
import sublime

RE_ALIAS = re.compile(r'(?P<default>[\w\d\-._]+)@alias=(?P<alias>[\w\d\-._]*)')
RE_DOC = re.compile(r'D\d{3}$')
RE_PYLINT_CODES = re.compile(r'(?P<error>[FE]\d+)|(?P<warning>[CIWR]\d+)$')

# Pylint symbolic name <--> code mapping
pylint_codes = {
    "blacklisted-name": "C0102",
    "invalid-name": "C0103",
    "missing-docstring": "C0111",
    "empty-docstring": "C0112",
    "missing-module-attribute": "C0121",
    "bad-classmethod-argument": "C0202",
    "bad-mcs-method-argument": "C0203",
    "bad-mcs-classmethod-argument": "C0204",
    "line-too-long": "C0301",
    "too-many-lines": "C0302",
    "trailing-whitespace": "C0303",
    "missing-final-newline": "C0304",
    "multiple-statements": "C0321",
    "superfluous-parens": "C0325",
    "bad-whitespace": "C0326",
    "mixed-line-endings": "C0327",
    "unexpected-line-ending-format": "C0328",
    "bad-continuation": "C0330",
    "wrong-spelling-in-comment": "C0401",
    "wrong-spelling-in-docstring": "C0402",
    "invalid-characters-in-docstring": "C0403",
    "old-style-class": "C1001",
    "syntax-error": "E0001",
    "unrecognized-inline-option": "E0011",
    "bad-option-value": "E0012",
    "init-is-generator": "E0100",
    "return-in-init": "E0101",
    "function-redefined": "E0102",
    "not-in-loop": "E0103",
    "return-outside-function": "E0104",
    "yield-outside-function": "E0105",
    "return-arg-in-generator": "E0106",
    "nonexistent-operator": "E0107",
    "duplicate-argument-name": "E0108",
    "missing-reversed-argument": "E0109",
    "abstract-class-instantiated": "E0110",
    "bad-reversed-sequence": "E0111",
    "method-hidden": "E0202",
    "access-member-before-definition": "E0203",
    "no-method-argument": "E0211",
    "no-self-argument": "E0213",
    "interface-is-not-class": "E0221",
    "missing-interface-method": "E0222",
    "bad-context-manager": "E0235",
    "invalid-slots-object": "E0236",
    "assigning-non-slot": "E0237",
    "invalid-slots": "E0238",
    "inherit-non-class": "E0239",
    "used-before-assignment": "E0601",
    "undefined-variable": "E0602",
    "undefined-all-variable": "E0603",
    "invalid-all-object": "E0604",
    "no-name-in-module": "E0611",
    "bad-except-order": "E0701",
    "raising-bad-type": "E0702",
    "raising-non-exception": "E0710",
    "notimplemented-raised": "E0711",
    "catching-non-exception": "E0712",
    "slots-on-old-class": "E1001",
    "super-on-old-class": "E1002",
    "bad-super-call": "E1003",
    "missing-super-argument": "E1004",
    "no-member": "E1101",
    "not-callable": "E1102",
    "assignment-from-no-return": "E1111",
    "no-value-for-parameter": "E1120",
    "too-many-function-args": "E1121",
    "unexpected-keyword-arg": "E1123",
    "redundant-keyword-arg": "E1124",
    "invalid-sequence-index": "E1126",
    "invalid-slice-index": "E1127",
    "logging-unsupported-format": "E1200",
    "logging-format-truncated": "E1201",
    "logging-too-many-args": "E1205",
    "logging-too-few-args": "E1206",
    "bad-format-character": "E1300",
    "truncated-format-string": "E1301",
    "mixed-format-string": "E1302",
    "format-needs-mapping": "E1303",
    "missing-format-string-key": "E1304",
    "too-many-format-args": "E1305",
    "too-few-format-args": "E1306",
    "bad-str-strip-call": "E1310",
    "print-statement": "E1601",
    "parameter-unpacking": "E1602",
    "unpacking-in-except": "E1603",
    "old-raise-syntax": "E1604",
    "backtick": "E1605",
    "long-suffix": "E1606",
    "old-ne-operator": "E1607",
    "old-octal-literal": "E1608",
    "fatal": "F0001",
    "astroid-error": "F0002",
    "ignored-builtin-module": "F0003",
    "parse-error": "F0010",
    "method-check-failed": "F0202",
    "unresolved-interface": "F0220",
    "import-error": "F0401",
    "raw-checker-failed": "I0001",
    "bad-inline-option": "I0010",
    "locally-disabled": "I0011",
    "locally-enabled": "I0012",
    "file-ignored": "I0013",
    "suppressed-message": "I0020",
    "useless-suppression": "I0021",
    "deprecated-pragma": "I0022",
    "no-self-use": "R0201",
    "cyclic-import": "R0401",
    "duplicate-code": "R0801",
    "too-many-ancestors": "R0901",
    "too-many-instance-attributes": "R0902",
    "too-few-public-methods": "R0903",
    "too-many-public-methods": "R0904",
    "too-many-return-statements": "R0911",
    "too-many-branches": "R0912",
    "too-many-arguments": "R0913",
    "too-many-locals": "R0914",
    "too-many-statements": "R0915",
    "interface-not-implemented": "R0923",
    "unreachable": "W0101",
    "dangerous-default-value": "W0102",
    "pointless-statement": "W0104",
    "pointless-string-statement": "W0105",
    "expression-not-assigned": "W0106",
    "unnecessary-pass": "W0107",
    "unnecessary-lambda": "W0108",
    "duplicate-key": "W0109",
    "deprecated-lambda": "W0110",
    "useless-else-on-loop": "W0120",
    "exec-used": "W0122",
    "eval-used": "W0123",
    "bad-builtin": "W0141",
    "lost-exception": "W0150",
    "assert-on-tuple": "W0199",
    "attribute-defined-outside-init": "W0201",
    "bad-staticmethod-argument": "W0211",
    "protected-access": "W0212",
    "arguments-differ": "W0221",
    "signature-differs": "W0222",
    "abstract-method": "W0223",
    "super-init-not-called": "W0231",
    "no-init": "W0232",
    "non-parent-init-called": "W0233",
    "non-iterator-returned": "W0234",
    "unnecessary-semicolon": "W0301",
    "bad-indentation": "W0311",
    "mixed-indentation": "W0312",
    "lowercase-l-suffix": "W0332",
    "wildcard-import": "W0401",
    "deprecated-module": "W0402",
    "relative-import": "W0403",
    "reimported": "W0404",
    "import-self": "W0406",
    "misplaced-future": "W0410",
    "fixme": "W0511",
    "invalid-encoded-data": "W0512",
    "global-variable-undefined": "W0601",
    "global-variable-not-assigned": "W0602",
    "global-statement": "W0603",
    "global-at-module-level": "W0604",
    "unused-import": "W0611",
    "unused-variable": "W0612",
    "unused-argument": "W0613",
    "unused-wildcard-import": "W0614",
    "redefined-outer-name": "W0621",
    "redefined-builtin": "W0622",
    "redefine-in-handler": "W0623",
    "undefined-loop-variable": "W0631",
    "unbalanced-tuple-unpacking": "W0632",
    "unpacking-non-sequence": "W0633",
    "cell-var-from-loop": "W0640",
    "bare-except": "W0702",
    "broad-except": "W0703",
    "pointless-except": "W0704",
    "nonstandard-exception": "W0710",
    "binary-op-exception": "W0711",
    "property-on-old-class": "W1001",
    "assignment-from-none": "W1111",
    "logging-not-lazy": "W1201",
    "logging-format-interpolation": "W1202",
    "bad-format-string-key": "W1300",
    "unused-format-string-key": "W1301",
    "bad-format-string": "W1302",
    "missing-format-argument-key": "W1303",
    "unused-format-string-argument": "W1304",
    "format-combined-specification": "W1305",
    "missing-format-attribute": "W1306",
    "invalid-format-index": "W1307",
    "anomalous-backslash-in-string": "W1401",
    "anomalous-unicode-escape-in-string": "W1402",
    "bad-open-mode": "W1501",
    "boolean-datetime": "W1502",
    "redundant-unittest-assert": "W1503",
    "unidiomatic-typecheck": "W1504",
    "apply-builtin": "W1601",
    "basestring-builtin": "W1602",
    "buffer-builtin": "W1603",
    "cmp-builtin": "W1604",
    "coerce-builtin": "W1605",
    "execfile-builtin": "W1606",
    "file-builtin": "W1607",
    "long-builtin": "W1608",
    "raw_input-builtin": "W1609",
    "reduce-builtin": "W1610",
    "standarderror-builtin": "W1611",
    "unicode-builtin": "W1612",
    "xrange-builtin": "W1613",
    "coerce-method": "W1614",
    "delslice-method": "W1615",
    "getslice-method": "W1616",
    "setslice-method": "W1617",
    "no-absolute-import": "W1618",
    "old-division": "W1619",
    "dict-iter-method": "W1620",
    "dict-view-method": "W1621",
    "next-method-called": "W1622",
    "metaclass-assignment": "W1623",
    "indexing-exception": "W1624",
    "raising-string": "W1625",
    "reload-builtin": "W1626",
    "oct-method": "W1627",
    "hex-method": "W1628",
    "nonzero-method": "W1629",
    "cmp-method": "W1630",
    "input-builtin": "W1632",
    "round-builtin": "W1633",
    "intern-builtin": "W1634",
    "unichr-builtin": "W1635",
    "map-builtin-not-iterating": "W1636",
    "zip-builtin-not-iterating": "W1637",
    "range-builtin-not-iterating": "W1638",
    "filter-builtin-not-iterating": "W1639",
    "using-cmp-argument": "W1640"
}


# Predictable code <--> near token mapping
near_token = {
    # Pylint
    'C1001': 'class',  # adequately reported at column 0, converted to None
    'E0100': '__init__',
    'E0101': '__init__',
    'E0106': 'return',
    'E0235': '__exit__',
    'E0711': 'NotImplemented',
    'E1111': '=',
    'I0014': 'disable',
    'I0022': '-msg',  # 'disable-msg' or 'enable-msg'. TODO find a way to highlight both
    'W0122': 'exec',
    'W0142': '*',
    'W0231': '__init__',
    'W0234': '__iter__',  # or 'next'. TODO find a way to handle both
    'W0301': ';',
    'W0331': '<>',
    'W0401': 'import *',
    'W0410': '__future__',  # reported at column 0, converted to None
    'W0603': 'global',
    'W0604': 'global',
    'W0614': 'import *',
    'W1111': '=',
    'W1201': '%',

    # Pylint: no meaningful columns
    'C0111': None,  # mssing docstring for modules, classes and methods
    'C0112': None,  # empty docstring for modules, classes and methods
    'C0301': None,
    'C0302': None,
    'C0303': None,
    'C0304': None,
    # 'C0326',  # special case TODO find a way to use the next 2 lines on
    # the report, which shows the position of the error.
    'E0001': None,
    'E0102': None,
    'E0202': None,
    'E0211': None,
    'E0213': None,
    'E0221': None,
    'E0222': None,
    'E1001': None,
    'E1002': None,
    'E1120': None,
    'E1121': None,
    'E1125': None,
    'E1200': None,
    'E1201': None,
    'E1205': None,
    'E1206': None,
    'E1300': None,
    'E1301': None,
    'E1302': None,
    'E1303': None,
    'E1304': None,
    'E1305': None,
    'E1306': None,
    'I0013': None,
    'R0902': None,
    'R0903': None,
    'R0911': None,
    'R0912': None,
    'R0914': None,
    'W0101': None,
    'W0104': None,
    'W0105': None,
    'W0109': None,  # on a multiline dict, it is reported on the assignment line
    'W0120': None,
    'W0121': None,
    'W0199': None,
    'W0221': None,
    'W0222': None,
    'W0223': None,
    'W0232': None,
    'W0311': None,
    'W0312': None,
    'W0406': None,
    'W0632': None,
    'W0633': None,
    'W0712': None,
    'W1300': None,
    'W1301': None
}


# Code <--> near regex mapping
near_regex = {
    # McCabe Prospector
    'MC0001': r'(?:[\w\d_]+\.)*?(?P<near>[\w\d_]+) is too complex \(\d+\)',

    # Pyflakes
    'F401': r'(?P<near>\'.+\') imported but unused',

    # Pylint
    'C0102': r'Black listed name "(?P<near>.*)"',
    'C0103': r'Invalid \S+ name "(?P<near>.*)"',
    'C0202': r"Class method (?P<near>.*) should have",
    'C0203': r"Metaclass method (?P<near>.*) should have",
    'C0204': r"Metaclass class method (?P<near>.*) should have",
    'C0325': r"Unnecessary parens after '(?P<near>.*)' keyword",
    'C1001': r"Old-style (?P<near>class) defined",
    'E0001': r'unknown encoding: (?P<near>.*)',  # can also be 'invalid syntax', 'EOF in multi-line statement'
    'E0011': r"Unrecognized file option '(?P<near>.*)'",
    'E0012': r"Bad option value '(?P<near>.*)'",
    'E0100': r"(?P<near>__init__) method is a generator",
    'E0107': r'Use of the non-existent (?P<near>.*) operator',
    'E0108': r"Duplicate argument name (?P<near>.*) in function definition",
    'E0203': r"Access to member '(?P<near>.*)' before its definition",
    'E0603': r"Undefined variable name '(?P<near>.*)' in",
    'E0604': r"Invalid object '(?P<near>.*)' in",
    'E0611': r"No name '(?P<near>.*)' in module",
    # may also be: Bad except clauses order (empty except clause should always appear last)
    # which is reported on the 'try'  -> keep the column info !
    'E0701': r'Bad except clauses order \(.* is an ancestor class of (?P<near>.*)\)',
    'E0712': r"Catching an exception which doesn't inherit from BaseException: (?P<near>.*)",
    'E1003': r"Bad first argument '(?P<near>.*)' given to super()",
    'E1101': r"has no '(?P<near>.*)' member",
    'E1102': r"(?P<near>.*) is not callable",
    'E1103': r"has no '(?P<near>.*)' member",
    'E1123': r"Passing unexpected keyword argument '(?P<near>.*)' in function call",
    'E1124': r"Parameter '(?P<near>.*)' passed as both positional and keyword argument",
    'E1310': r"Suspicious argument in \S+\.(?P<near>.*) call",
    'F0220': r"failed to resolve interfaces implemented by \S+ \((?P<near>.*)\)",
    'F0401': r"Unable to import '(?P<near>.*)'",
    'I0010': r"Unable to consider inline option '(?P<near>.*)'",
    'I0011': r"Locally disabling (?P<near>.*)",
    'I0012': r"Locally enabling (?P<near>.*)",
    'W0102': r'Dangerous default value (?P<near>\S*) (\(.*\) )?as argument',
    'W0106': r'Expression "\((?P<near>.*)\)" is assigned to nothing',  # FIXME regex too greedy ?
    'W0201': r"Attribute '(?P<near>.*)' defined outside __init__",
    'W0211': r"Static method with '(?P<near>.*)' as first argument",
    'W0212': r"Access to a protected member (?P<near>.*) of a client class",
    'W0402': r"Uses of a deprecated module '(?P<near>.*)'",
    'W0403': r"Relative import '(?P<near>.*)', should be",
    'W0404': r"Reimport '(?P<near>.*)'",
    'W0511': r"(?P<near>.*)",
    'W0512': r'Cannot decode using encoding ".*", unexpected byte at position (?P<col>\d+)',
    'W0601': r"Global variable '(?P<near>.*)' undefined",
    'W0602': r"Using global for '(?P<near>.*)' but",
    'W0611': r"Unused import (?P<near>.*)",
    'W0621': r"Redefining name '(?P<near>.*)' from outer scope",
    'W0622': r"Redefining built-in '(?P<near>.*)'",
    'W0623': r"Redefining name '(?P<near>.*)' from object '.*' in exception handler",
    'W0711': r'Exception to catch is the result of a binary "(?P<near>.*)" operation',
    'W1401': r"Anomalous backslash in string: '(?P<near>.*)'",  # does not work with \o, ...
    'W1402': r"Anomalous Unicode escape in byte string: '(?P<near>.*)'",  # does not work with \u, \U
    'W1501': r'"(?P<near>.*)" is not a valid mode for open'
}


@lru_cache(maxsize=None)
def which(cmd):
    """
    Return the full path to the given command, or None if not found.

    Adjust for alias name.  This is good for selecting maybe a symlink to
    a different version from the default one.
    """

    match = RE_ALIAS.match(cmd)

    if match:
        path = None
        args = match.groupdict()
        if args.get('alias'):
            path = util.find_executable(args.get('alias'))
        if not path:
            path = util.find_executable(args.get('default'))
        return path
    else:
        return util.find_executable(cmd)


@lru_cache(maxsize=None)
def find_files(start_dir, names, parent=False, limit=None, aux_dirs=None):
    """
    Take SublimeLinters 'find_file' and augment it to find one of a list of file names.

    Any match in the list, we quit and return the path.
    """

    if aux_dirs is None:
        aux_dirs = []

    for d in util.climb(start_dir, limit=limit):
        for name in names:
            target = os.path.join(d, name)

            if os.path.exists(target):
                if parent:
                    return d

                return target

    for d in aux_dirs:
        d = os.path.expanduser(d)
        for name in names:
            target = os.path.join(d, name)

            if os.path.exists(target):
                if parent:
                    return d

                return target

class Prospector(Linter):

    """Provides an interface to prospector."""

    syntax = ('python', )
    version_args = '--version'
    executable = "prospector@alias="
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.10.2'
    regex = r'''(?x)
        # Line:Column Class.function Tool
        ^\s+L(?P<line>\d+):(?P<col>\-|\d+)[ ](?P<method>.*?):[ ](?P<tool>[\w\d\-_]+)[ ]-[ ]
        # Codes
        (?P<code>
            # Sort pep8, pep257, pep8-naming, MCabe and pyflakes error codes
            (?P<error>(?:F(?:40[24]|8(?:12|2[123]|31))|E(?:11[23]|90[12])))|
            (?P<warning>(?:[DFEWCN]|MC)\d+)|
            # Pylint errors will drop into unsorted as they are symbolic names
            # and will be sorted later.
            (?P<unsorted>.+?)
        )\r?\n
        # The related message.
        ^\s+(?P<message>.+?)\r?\n
    '''
    multiline = True
    tempfile_suffix = "-"
    check_version = True
    prospector_config = ('.prospector.yml', 'landscape.yml')
    prospector_cwd = None
    prospector_target = None
    prospector_project_profile = False

    defaults = {
        '--profile:,+': [],
        '--strictness': 'medium',
        '--max-line-length': 160,
        '--profile-path': '',
        '--uses:,+': [],
        '--tools:,+': [],
        '--with-tool:,+': [],
        '--without-tool:,+': [],
        '--ignore-patterns:,+': [],
        '--ignore-paths:,+': []
    }

    meta_defaults = {
        '@only-project-profile': False,
        '@alias': 'prospector',
        '@project-profiles': ['.prospector.yml', '.landscape.yml'],
        '@project-root-files': ['tox.ini', 'setup.cfg', '.git', '.gitignore']
    }

    disallowed_args = {
        '-S', '--summary-only',
        '-M', '--messages-only',
        '-X', '--die-on-tool-error',
        '--absolute-paths',
        '-0', '--zero-exit',
        '-h', '--help',
        '-v', '--version'
    }

    disallowed_kwargs = {
        '-o', '--output-format',
        '-p', '--path'
    }

    profile_path = {
        '--profile', '-P'
    }

    def context_sensitive_executable_path(self, cmd):
        """
        Find the alias requested, else return the default.

        If none are found, return None.
        """

        match = RE_ALIAS.match(cmd[0])
        if match:
            settings = self.get_view_settings()
            default_script = match.group('default')
            alias_script = settings.get('@alias', '')
            which = '{}@alias={}'.format(default_script, alias_script)
            path = self.which(which)

            if path:
                return True, path

        return False, None

    @classmethod
    def settings(cls):
        """Return the default settings for this linter, merged with the user settings."""

        if cls.lint_settings is None:
            linters = persist.settings.get('linters', {})
            cls.lint_settings = (cls.defaults or {}).copy()
            cls.lint_settings.update((cls.meta_defaults or {}).copy())
            cls.lint_settings.update(linters.get(cls.name, {}))

        return cls.lint_settings

    @classmethod
    def which(cls, cmd):
        """Find which cmd binary to use."""

        return which(cmd)

    def replace_sublime_profile(self, a):
        """Replace sublime profile."""

        m = re.match(r'\$\{sublime=(?P<profile>.+?)\}', a)
        if m:
            if os.path.exists(filename):
                a = filename
        return a

    def insert_args(self, cmd):
        """Insert user arguments into cmd and return the result."""

        # Get build args, but strip out anything that would
        # interfere with are needed settings.
        args = []

        if not self.prospector_project_profile:
            skip_next = False
            replace_variables = False
            count = 0
            for a in self.build_args(self.get_view_settings(inline=True)):
                if replace_variables:
                    args.append('%s' % self.replace_sublime_profile(a))
                elif skip_next:
                    skip_next = False
                elif a in self.disallowed_args:
                    pass
                elif a in self.disallowed_kwargs:
                    skip_next = True
                elif a in self.profile_path:
                    args.append(a)
                    replace_variables = True
                else:
                    args.append(a)
                count += 1

        cmd = list(cmd)

        if '*' in cmd:
            i = cmd.index('*')

            if args:
                cmd[i:i + 1] = args
            else:
                cmd.pop(i)
        else:
            cmd += args

        return cmd

    def cmd(self):
        """Return the command line to execute."""

        # self.executable_path = None
        self.prospector_project_profile = False
        self.prospector_cwd = None
        self.prospector_target = self.filename
        self.only_project_profile = False

        settings = self.get_view_settings()
        alias = settings['@alias']
        root_check = tuple(settings['@project-root-files'])
        project_profiles = tuple(settings['@project-profiles'])
        self.only_project_profile = settings['@only-project-profile']

        alias = '@alias=%s' % ('' if not isinstance(alias, str) else alias)

        # This is the base command
        #    - Prospector call.
        #    - Emacs output for easy parsing result parsing.
        #    - Messages only; no summary.
        cmd = ['prospector' + alias, '-o', 'emacs', '-M']

        # Try and find prospector default config file
        # and, if found count, the parent directory as project root.
        prospector_config = None
        if '-p' not in cmd and '--path' not in cmd and self.filename:
            prospector_config = find_files(
                os.path.dirname(self.filename),
                project_profiles,
            )

        # If no config found, try and find the root of the project
        # by searching for a file that indicates the root.
        root = None
        if not prospector_config:
            root = find_files(
                os.path.dirname(self.filename),
                root_check
            )

        # Set the CWD directory if project root found.
        # Add project profile if found and make relative to CWD.
        # Set target file path as relative to project root (if found).
        if prospector_config:
            self.prospector_project_profile = True
            self.prospector_cwd = os.path.dirname(prospector_config)
            self.prospector_target = os.path.relpath(self.filename, self.prospector_cwd)
            cmd += ['--profile-path', os.path.basename(prospector_config)]
        elif root is not None:
            self.prospector_cwd = os.path.dirname(root)
            self.prospector_target = os.path.relpath(self.filename, self.prospector_cwd)

        # Add insertion tokes for other arguments and file name.
        cmd += ['*', '@']

        if persist.debug_mode():
            persist.printf('------- Prospector Lint -------')
            persist.printf('Settings: {}'.format(self.get_view_settings()))
            persist.printf('Bin: {}'.format(cmd[0]))

        # Adjust for context sensitive settings
        have_path, path = self.context_sensitive_executable_path(cmd)
        if have_path:
            cmd[0] = path

        return cmd

    def split_match(self, match):
        """Split match."""

        # Get the match parts.
        error = bool(match.group('error')) or bool(match.group('unsorted'))
        warning = bool(match.group('warning'))
        message = match.group('message').strip()
        tool = match.group('tool')
        code = match.group('code')
        unsorted = match.group('unsorted')
        line = int(match.group('line')) - 1
        col = match.group('col')
        # method = match.group('method')
        near = None

        # '-' and '0' should not have a col highlighted without 'near'
        # Anything else should adjust column by '-1' as columns are '1' based.
        if col == '-' or (tool != 'pylint' and col == '0'):
            col = None
        else:
            col = int(col) - (1 if tool != 'pylint' else 0)

        # Pylint uses symbolic names in prospector.
        # Search the mappings to find actual code.
        if unsorted:
            error = True
            code = pylint_codes.get(unsorted)
            if code is not None:
                m = RE_PYLINT_CODES.match(code)
                if m:
                    error = bool(match.group('error'))
                    warning = bool(match.group('warning'))

        # See if this code has a predefined 'near' token.
        if code in near_token:
            col = None
            near = near_token[code]

        # See if this code has a regex to find the 'near' token.
        elif code in near_regex:
            col = None
            m = re.match(near_regex[code], message)
            if m:
                if 'near' in m.groupdict():
                    # 'near' will be more precise than 'col'
                    near = m.group('near')
                elif 'col' in m.groupdict():
                    col = int(m.group('col'))

        # Return the parsed match parts.
        return match, line, col, error, warning, "%s: %s" % (code, message), near

    def run(self, cmd, code):
        """Run."""

        # Prospector works best if you can run it from a path
        # relative to the config. So we adjust the CWD if found
        # the project root.

        if self.prospector_cwd is not None:
            os.chdir(self.prospector_cwd)

        if self.only_project_profile and not self.prospector_project_profile:
            return ''

        if persist.debug_mode():
            persist.printf('{}: {} {}'.format(
                self.name,
                os.path.basename(self.filename or '<unsaved>'),
                cmd or '<builtin>')
            )

        # Add in the adjusted file target
        if '@' in cmd:
            cmd[cmd.index('@')] = self.prospector_target
        elif not code:
            cmd.append(self.prospector_target)

        if persist.debug_mode():
            persist.printf('Final CMD: {}'.format(str(cmd)))

        # We never run live, only on save, so no need to deal with view code.
        return util.communicate(
            cmd,
            None,
            output_stream=self.error_stream,
            env=self.env
        )
