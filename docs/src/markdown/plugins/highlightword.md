# HighlightWord (STABLE)

## Overview

An advanced highlight word plugin. Originally a mod of [ajpalkovic's plugin](https://github.com/ajpalkovic), though it
doesn't appear to be available anymore.


## Configuring

All settings are found in `highlight_word.sublime-settings`.

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

## Selecting All Instances of Word

HighlightWord also provides a command to highlight all instances of selected word(s). Just add the following command to
your `Default.sublime-commands` file:

```js
    //////////////////////////////////
    // Highlight Word
    //////////////////////////////////
    {
        "caption": "HighlightWord: Select Word(s)",
        "command": "highlight_word_select"
    },
```

## License

Unknown at the present.  It used to be publicly available, but has since been removed.  I had forked it for personal
modifications.  There was no license mentioned at the time.
