"""
InsertDate Sublime Plugin.

Very simple plugin that inserts the date.  You can create multiple variants of the commands
in the command palette to format the date in different ways via the `format` and `utc` option.

There are more comprehensive insert date plugins available, but this is really all I need at the present.

Example commands:

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

Licensed under MIT
Copyright (c) 2013-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import sublime_plugin
from datetime import datetime
import time


class InsertDateTimeCommand(sublime_plugin.TextCommand):
    """Insert date into view."""

    def run(self, edit, time_format="%Y-%m-%d", utc=False):
        """Run command."""

        if utc:
            date_time = time.strftime(time_format, time.gmtime())
        else:
            date_time = datetime.now().strftime(time_format)
        for sel in self.view.sel():
            self.view.replace(edit, sel, date_time)
