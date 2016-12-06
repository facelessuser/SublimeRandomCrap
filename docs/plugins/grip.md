# Grip (EXPERIMENTAL) {: .doctitle}
Github Readme GitHub Readme Instant Preview.

---

# Overview
This is buggy. Uses [grip](https://github.com/joeyespo/grip) (installed on machine) to preview a Github readme.  Can only have one grip instance running a one time.  When a new grip instance is created, the last one is killed.

# Commands
```js
    //////////////////////////////////
    // Grip Commands
    //////////////////////////////////
    {
        "caption": "Grip: Preview",
        "command": "grip"
    },
    {
        "caption": "Grip: Live Preview",
        "command": "grip",
        "args": {"livereload": true}
    },
    {
        "caption": "Grip: Kill Last Instance",
        "command": "grip_kill"
    }
```

# Settings
Settings are found in `sublime-grip.sublime-settings`.

## python_cmd
Specify the python command to be used.  In general, grip will be called in the following way `python -m grip`, but on some systems, you may have to give the absolute path or something different.

If python found on path:

```js
    "python_cmd": ["python"]
```

If using a specific python version on a Unix/Linux system:

```js
    "python_cmd": ["python3"]
```

If python requires an absolute path:

```js
    "python_cmd": ["/some/path/python"]
```

If using python launcher on windows:

```js
    "python_cmd": ["py", "-3.5"]
```

Or anything else you require.

# License
Licensed under MIT
Copyright (c) 2016 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
