# AsciiTable (STABLE)

## Overview

Displays an extended ASCII table in Sublime for reference.  Allows searching the table for specific info.

## Commands

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

## License

Licensed under MIT
Copyright (c) 2014-2019 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
