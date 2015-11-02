"""
Originally a mod of ajpalkovic's plugin https://github.com/ajpalkovic, though it doesn't appear to be available anymore.

Highlights all other instances of the selected word (or optional word under cursor):

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
"""
import sublime
import sublime_plugin
from time import time, sleep
import threading

KEY = "HighlightCurrentWord"
SCOPE = 'comment'

reload_flag = False
highlight_word = None
settings = None

if 'hw_thread' not in globals():
    hw_thread = None


def debug(s):
    """Debug logging."""

    print("HighlightWord: " + s)


def highlight_style(option):
    """Configure style of region based on option."""

    style = 0
    if option == "outline":
        style |= sublime.DRAW_NO_FILL
    elif option == "none":
        style |= sublime.HIDDEN
    elif option == "underline":
        style |= sublime.DRAW_EMPTY_AS_OVERWRITE
    elif option == "thin_underline":
        style |= sublime.DRAW_NO_FILL
        style |= sublime.DRAW_NO_OUTLINE
        style |= sublime.DRAW_SOLID_UNDERLINE
    elif option == "squiggly":
        style |= sublime.DRAW_NO_FILL
        style |= sublime.DRAW_NO_OUTLINE
        style |= sublime.DRAW_SQUIGGLY_UNDERLINE
    elif option == "stippled":
        style |= sublime.DRAW_NO_FILL
        style |= sublime.DRAW_NO_OUTLINE
        style |= sublime.DRAW_STIPPLED_UNDERLINE
    return style


def clear_regions(view=None):
    """Clear regions."""

    if view is None:
        win = sublime.active_window()
        if win is not None:
            view = win.active_view()
    if view is not None:
        regions = view.settings().get('highlight_word_regions', 0)
        if highlight_word is not None:
            for count in range(0, regions):
                view.erase_regions(KEY + str(count))
                view.settings().set('highlight_word_regions', 0)


def underline(regions):
    """Convert to empty regions."""

    new_regions = []
    for region in regions:
        start = region.begin()
        end = region.end()
        while start < end:
            new_regions.append(sublime.Region(start))
            start += 1
    return new_regions


# The search is performed half a second after the most recent event
# in order to prevent the search hapenning on every keypress.
# Each of the event handlers simply marks the time of the most recent
# event and a timer periodically executes do_search
class HighlightWord(object):
    """HighlightWord."""

    def __init__(self):
        """Setup."""

        self.previous_region = sublime.Region(0, 0)
        self.theme_selectors = tuple(settings.get('highlight_scopes', [SCOPE]))
        self.word_select = settings.get('require_word_select', False)
        style = settings.get('highlight_style', 'outline')
        self.style = highlight_style(style)
        self.underline = style == 'underline'
        self.max_selections = len(self.theme_selectors)
        self.sel_threshold = int(settings.get('selection_threshold', -1))

    def do_search(self, view, force=True):
        """Perform the search for the highlighted word."""

        global reload_flag
        if view is None:
            return

        if reload_flag:
            reload_flag = False
            self.theme_selectors = tuple(settings.get('highlight_scopes', [SCOPE]))
            self.max_selections = len(self.theme_selectors)
            self.word_select = settings.get('require_word_select', False)
            style = settings.get('highlight_style', 'outline')
            self.style = highlight_style(style)
            self.underline = style == 'underline'
            self.sel_threshold = int(settings.get('selection_threshold', -1))
            force = True

        visible_region = view.visible_region()
        if not force and self.previous_region == visible_region:
            return

        clear_regions()

        # The default separator does not include whitespace, so I add that here no matter what
        separator_string = view.settings().get('word_separators', "") + " \n\r\t"

        current_words = []
        current_regions = []
        good_words = set()
        words = []

        selections = view.sel()
        sel_len = len(selections)
        if sel_len > 0 and (self.sel_threshold == -1 or self.sel_threshold >= sel_len):
            self.previous_region = visible_region

            # Reduce m*n search to just n by mapping each word
            # separator character into a dictionary
            self.separators = {}
            for c in separator_string:
                self.separators[c] = True

            for selection in selections:
                current_regions.append(view.word(selection))
                current_words.append(
                    view.substr(current_regions[-1]).strip(separator_string)
                )

            count = 0
            for word in current_words:
                if word not in good_words:
                    if count != self.max_selections:
                        good_words.add(word)
                        words.append((word, current_regions[count]))
                        count += 1
                    else:
                        return

        count = 0
        for word in words:
            key = KEY + str(count)
            selector = self.theme_selectors[count]

            # See if a word is selected or if you are just in a word
            if self.word_select and word[1].size() != selections[count].size():
                continue

            # remove leading/trailing separator characters just in case
            # print u"|%s|" % currentWord
            if len(word[0]) == 0:
                continue

            # ignore the selection if it spans multiple words
            abort = False
            for c in word[0]:
                if c in self.separators:
                    abort = True
                    break
            if abort:
                continue

            self.highlight_word(view, key, selector, word[1], word[0])
            count += 1

    def highlight_word(self, view, key, selector, current_region, current_word):
        """Find and highlight word."""

        size = view.size() - 1
        search_start = max(0, self.previous_region.begin() - len(current_word))
        search_end = min(size, self.previous_region.end() + len(current_word))

        valid_regions = []
        while True:
            found_region = view.find(current_word, search_start, sublime.LITERAL)
            if found_region is None:
                break

            # regions can have reversed start/ends so normalize them
            start = max(0, found_region.begin())
            end = min(size, found_region.end())
            if search_start == end:
                search_start += 1
                continue
            search_start = end

            if search_start >= size:
                break

            if found_region.empty():
                break

            if found_region.intersects(current_region):
                continue

            # check if the character before and after the region is a separator character
            # if it is not, then the region is part of a larger word and shouldn't match
            # this can't be done in a regex because we would be unable to use the word_separators setting string
            if start == 0 or view.substr(sublime.Region(start - 1, start)) in self.separators:
                if end == size or view.substr(sublime.Region(end, end + 1)) in self.separators:
                    valid_regions.append(found_region)

            if search_start > search_end:
                break

        view.add_regions(
            key,
            valid_regions if not self.underline else underline(valid_regions),
            selector,
            "",
            self.style
        )

        view.settings().set('highlight_word_regions', self.max_selections)


class HighlightWordListenerCommand(sublime_plugin.EventListener):
    """Handle listener events."""

    def on_selection_modified(self, view):
        """Handle selection events for highlighting."""

        if hw_thread.ignore_all:
            return
        now = time()
        hw_thread.modified = True
        hw_thread.time = now


class HwThread(threading.Thread):
    """Load up defaults."""

    def __init__(self):
        """Setup the thread."""
        self.reset()
        threading.Thread.__init__(self)

    def reset(self):
        """Reset the thread variables."""
        self.wait_time = 0.12
        self.time = time()
        self.modified = False
        self.ignore_all = False
        self.abort = False

    def payload(self, force=False):
        """Code to run."""

        self.modified = False
        # Ignore selection and edit events inside the routine
        self.ignore_all = True
        if highlight_word is not None:
            highlight_word.do_search(sublime.active_window().active_view(), force)
        self.ignore_all = False
        self.time = time()

    def kill(self):
        """Kill thread."""

        self.abort = True
        while self.is_alive():
            pass
        self.reset()

    def run(self):
        """Thread loop."""

        while not self.abort:
            if self.modified is True and time() - self.time > self.wait_time:
                sublime.set_timeout(lambda: self.payload(force=True), 0)
            elif not self.modified:
                sublime.set_timeout(self.payload, 0)
            sleep(0.5)


def set_reload():
    """Set reload events."""

    global reload_flag
    global settings
    reload_flag = True
    settings = sublime.load_settings("highlight_word.sublime-settings")
    settings.clear_on_change('reload')
    settings.add_on_change('reload', set_reload)


def plugin_loaded():
    """Setup plugin."""

    global highlight_word
    global hw_thread
    set_reload()
    highlight_word = HighlightWord()

    if hw_thread is not None:
        hw_thread.kill()
    hw_thread = HwThread()
    hw_thread.start()


def plugin_unloaded():
    """Kill thread."""

    hw_thread.kill()
    clear_regions()
