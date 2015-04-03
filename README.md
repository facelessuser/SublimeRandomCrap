SublimeRandomCrap
=================
Random Sublime plugin scripts (some experimental).  This is a personal repo of plugins that aren't worth creating a repo for, or are experimental plugins.  There may not be documentation on all scripts in this repo (maybe an idea is incomplete or abandoned; therefore, not worth mentioning).  I will not be actively give support to anyone who stumbles on this, so use at your own risk.  Usually, if I am willing to start supporting a plugin here, you will see it moved to its own repo and appear on Package Control.  If a plugin becomes to complicated, I may move it to its own repo and still keep it off Package Control. 

### Table of Contents

- [ToggleWhiteSpace (STABLE)](#togglewhitespace-stable)
    - [Commands](#commands)
    - [License](#license)
- [HighlightWord (STABLE)](#highlightword-stable)
    - [Configuring](#configuring)
    - [License](#license-1)
- [SublimeApiDoc (STABLE)](#sublimeapidoc-stable)
    - [Commands](#commands-1)
    - [License](#license-2)
- [SublimeInfo (STABLE)](#sublimeinfo-stable)
    - [Commands](#commands-2)
    - [License](#license-3)
- [InsertDate (STABLE)](#insertdate-stable)
    - [Commands](#commands-3)
    - [License](#license-4)
- [ShortcutPlus (STABLE)](#shortcutplus-stable)
    - [Commands](#commands-4)
    - [License](#license-5)
- [GrepHere (STABLE)](#grephere-stable)
    - [Configuring](#configuring-1)
    - [Commands](#commands-5)
    - [License](#license-6)
- [AsciiTable (STABLE)](#asciitable-stable)
    - [Commands](#commands-6)
    - [License](#license-7)
- [Postmaster (EXPERIMENTAL)](#postmaster-experimental)
    - [Configuring](#configuring-2)
    - [Commands](#commands-7)
    - [License](#license-8)

## ToggleWhiteSpace (STABLE)
Simple plugin that toggles showing white space.

### Commands
```js
    //////////////////////////////////
    // Toggle White Space Command
    //////////////////////////////////
    {
        "caption": "Toggle White Space",
        "command": "toggle_white_space"
    },
```

### License

Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## HighlightWord (STABLE)
Originally a mod of ajpalkovic's plugin https://github.com/ajpalkovic, though it doesn't appear to be available anymore.


### Configuring
Highlights all other instances of the selected word (or optionally word under cursor):

```js
    // Require the word to be selected.
    // Disable to highlight word with no selection.
    "require_word_select": true,
```

Can be configured to highlight multiple word sets simultaneously with multiple cursors.
When doing multiple cursors, you can highlight each in their own color
(limited by available theme colors):

```js
    // Define scopes for highlights
    // The more you define, the more selections you can do
    "highlight_scopes": ["string", "keyword", "constant.language"],
```

Style of highlights can also be controlled:

```js
    // Highlight style (solid|outline|underline|thin_underline|squiggly|stippled)
    "highlight_style": "outline",
```

Optionally can disable highlight if number of selections in view are greater than a certain value:

```js
    // If selection threshold is greater than
    // the specified setting, don't highlight words.
    // -1 means no threshold.
    "selection_threshold": -1
```

### License
Unknown at the present.  It used to be publicly available, but has since been removed.  I had forked it for personal modifications.  There was no license mentioned at the time.

## SublimeApiDoc (STABLE)
Show Sublime's API Doc webpage:

### Commands
```js
    //////////////////////////////////
    // Doc Commands
    //////////////////////////////////
    {
        "caption": "Sublime API Docs",
        "command": "show_sublime_api"
    },
```

### License
Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## SublimeInfo (STABLE)
Show info about the system and the current Sublime Text instance.

### Commands
```js
    //////////////////////////////////
    // Info Commands
    //////////////////////////////////
    {
        "caption": "Sublime Info",
        "command": "sublime_info"
    },
```

### License
Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## InsertDate (STABLE)
Very simple plugin that inserts the date.  You can create multiple variants of the commands
in the command palette to format the date in different ways via the `format` and `utc` option.

There are more comprehensive insert date plugins available, but this is really all I need at the present.

### Commands

Example Commands:

```js
    //////////////////////////////////
    // Insertion Commands
    //////////////////////////////////
    {
        "caption": "Insert: Date",
        "command": "insert_date_time"
    },
    {
        "caption": "Insert: UTC Date Time",
        "command": "insert_date_time",
        "args": { "format": "%Y-%m-%d %H:%M:%S", "utc": true }
    },
```

### License
Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## ShortcutPlus (STABLE)
Plugin for creating shortcuts that are context sensitive to profiles, platforms, OS, etc.

### Commands
This shows how to define two shortcut profiles bound to shortcuts:

```js
    // Shortcut Plus Toggle
    {
        "keys": ["alt+`"],
        "command": "toggle_shortcut_plus",
        "args": {"profile": "MyProfile1"}
    },
    // Shortcut Plus Toggle
    {
        "keys": ["ctrl+alt+`"],
        "command": "toggle_shortcut_plus",
        "args": {"profile": "MyProfile2"}
    },
```


This shows how to create shortcuts that execute only in a given shortcut profile. The first is bound to `Myprofile1` and shows a dialog when all selections are empty and the escape key is pressed.  `shortcut_plus_test` is command only for testing; you can use any command you want.

```js
    // Shortcut Plus Test
    {
        "keys": ["escape"],
        "command": "shortcut_plus_test",
        "context":
        [
            {"key": "shortcut_plus(profile):MyProfile1"},
            {"key": "selection_empty", "operator": "equal", "operand": true, "match_all": true}
        ],
        "args": {
            "msg": "All selection are empty!"
        }
    },
```

The next example is bound to MyProfile2 and shows the inverse when escape is pressed.
```js
    // Shortcut Plus Test
    {
        "keys": ["escape"],
        "command": "shortcut_plus_test",
        "context":
        [
            {"key": "shortcut_plus(profile):MyProfile2"},
            {"key": "selection_empty", "operator": "equal", "operand": false, "match_all": true}
        ],
        "args": {
            "msg": "All selections are not empty!"
        }
    }
```

### License
Licensed under MIT
Copyright (c) 2012-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## GrepHere (STABLE)
Sends a sidebar path or current view path to your favorite grep program.

### Configuring
Multiple entries can be defined and you can limit them to a specific platform:

```js
    "grep_call": {
        "win": {
            "caption": "Grep Here…",
            "cmd": ["C:\\Program Files\\grepWin\\grepWin.exe", "/searchpath:${PATH}"],
            "platform": ["windows"]
        },
        "win_rummage": {
            "caption": "Rummage Here…",
            "cmd": ["C:\\Program Files (x86)\\Rummage\\Rummage.exe", "-s", ":${PATH}"],
            "platform": ["windows"]
        },
        "osx": {
            "caption": "Rummage Here…",
            "cmd": ["/Applications/Rummage.app/Contents/MacOS/Rummage", "-s", "${PATH}"],
            "platform": ["osx"]
        }
    }
```

### Commands
You can then define actual commands for the context menu or sidebar context menu:

Context menu:
```js
    {"command": "grep_here_file", "args": {"key": "osx"}},
    {"command": "grep_here_file", "args": {"key": "win"}},
    {"command": "grep_here_file", "args": {"key": "win_rummage"}},
```

Sidebar menu:

```js
    {"command": "grep_here_folder", "args": {"paths": [], "key": "osx"}},
    {"command": "grep_here_folder", "args": {"paths": [], "key": "win"}},
    {"command": "grep_here_folder", "args": {"paths": [], "key": "win_rummage"}}
```

### License
Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## AsciiTable (STABLE)
Displays an extended ASCII table in Sublime for reference.  Allows searching the table for specific info.

### Commands
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

### License
Licensed under MIT
Copyright (c) 2014-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Postmaster (EXPERIMENTAL)
Allows for sending emails via SMTP.  New emails are created via a command:

Emails consist of the email content preceded by YAML frontmatter that defines
the subject, sender, recipients, attachments and SMTP servo info:

```
---
subject: Sending a file
from: Postmaster User <postmasteruser@example.com>
to: ''
cc: ''
bcc: ''
attachments:
- /Somepath/somefile.txt
smtp_server: smtp.gmail.com
port: 587
tls: true
---
Jeff,

Hey what's up. Here's a file.

~Postmaster
```

New emails can be configured with templates. If you have multiple templates, you will prompted for which template to use.

When sending emails, you will be prompted for your password.

### Configuring
When creating an new email, postmaster looks in your Sublime User/Postmaster folder to find email templates.  These are used to create your new email
with its frontmatter and content:

```js
{
    "from": "Postmaster User <postmasteruser@example.com>",
    "signature": "~Postmaster",
    "smtp_server": "smtp.gmail.com",
    "port": 587,
    "tls": true
}
```

Available template variables are:

| Name         | Type                       | Description                                                                                     |
|--------------|----------------------------|-------------------------------------------------------------------------------------------------|
| subject      | string                     | Email subject.                                                                                  |
| from         | string                     | Sender in the form `me@example.com` or `My Name <me@example.com>`.                              |
| to           | string or array of strings | Recipient in the form `to@example.com` or `Their Name <to@example.com>`.                        |
| cc           | string or array of strings | Carbon copy recipient in the form `to@example.com` or `Their Name <to@example.com>`.            |
| bcc          | string or array of strings | Blind carbon copy recipient in the form `to@example.com` or `Their Name <to@example.com>`.      |
| attachements | string or array of strings | Full file path for the attachment.                                                              |
| body         | string                     | Optional default body if desired.                                                               |
| smtp_server  | string                     | SMTP server used to send email.                                                                 |
| port         | int                        | SMTP server port used to send email.                                                            |
| tls          | bool                       | Should use tls via STARTTLS.                                                                    |
| user         | string                     | Optional user name for SMTP server. By your default sender email will be used `me@example.com`. |


### Commands
Just add the following commands to create and send emails:

```js
    //////////////////////////////////
    // Postmaster
    //////////////////////////////////
    {
        "caption": "Postmaster: Send Mail",
        "command": "postmaster_send"
    },
    {
        "caption": "Postmaster: New Mail",
        "command": "postmaster_new"
    },
```

If you want to right click an email in a view and send an email to it, add the following to your context menu:

```js
    {"command": "postmaster_mail_to"}
```

### License
Licensed under MIT
Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
