# GrepHere (STABLE) {: .doctitle}
Launch your favorite grep tool from Sublime text.
{: .doctitle-info}

---

# Overview
Sends a sidebar path or current view path to your favorite grep program.

# Configuring
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

Keep in mind that on windows, passing quoted paths to some applications in Python can turn out poorly (it all depends on the application receiving the paths). For example, I use [grepWin](http://stefanstools.sourceforge.net/grepWin.html) on windows, and passing quoted paths to it via Python just doesn't work well due to the way it parses its command line arguments.  So in this case, using a batch file is probably preferable as shown below:

Batch file:

```batch
"C:\Program Files\grepWin\grepWin.exe" /searchpath:%1
```

GrepHere configuration:

```js
    "win": {
        "caption": "Grep Here…",
        "cmd": ["C:\\MyPath\\grepwin.bat", "${PATH}"],
        "platform": ["windows"]
    },
```

# Commands
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
