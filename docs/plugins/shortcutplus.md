# ShortcutPlus (STABLE) {: .doctitle}
Shortcut profile manager for Sublime Text.

---

Plugin for creating shortcuts that are context sensitive to profiles, platforms, OS, etc.

# Commands
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

# License
Licensed under MIT
Copyright (c) 2012-2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
