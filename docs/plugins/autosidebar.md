# AutoSideBar (EXPERIMENTAL) {: .doctitle}
Auto hide and show the sidebar.
{: .doctitle-info}

---

# Overview
Provides a listener that will hide the sidebar when mousing over a text view and triggering a hover event.  Shows the sidebar when the cursor mouses over the gutter and triggers a hover event.

# Commands
AutoSideBar contains only one command that is used to enable and disable the feature.  The toggle command also has only one optional argument that is used to set the sidebar state on feature disable.  `show_sidebar` can be set either to `true` or `false` to show or hide the sidebar on feature disable.  If nothing is specified, the sidebar will be left in its current state (shown or hidden) on feature disable. 

```js
    //////////////////////////////////
    // AutoSideBar Commands
    //////////////////////////////////
    {
        "caption": "AutoSideBar: Toggle",
        "command": "auto_side_bar_toggle",
        "args": {"show_sidebar": true}
    },
```

# License
Licensed under MIT
Copyright (c) 2016 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
