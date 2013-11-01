import sublime
import sublime_plugin
from time import time, sleep
import _thread as thread

KEY = "HighlightCurrentWord"
STYLE = "solid"
SCOPE = 'comment'


def debug(s):
    print("HighlightWord: " + s)


# The search is performed half a second after the most recent event in order to prevent the search hapenning on every keypress.
# Each of the event handlers simply marks the time of the most recent event and a timer periodically executes doSearch
class HighlightWord(object):
    def __init__(self):
        self.previousRegion = sublime.Region(0, 0)
        self.highlighting = False

    def doSearch(self, view, force=True):
        self.highlighting = True

        if view == None:
            self.highlighting = False
            return

        selections = view.sel()
        if len(selections) == 0:
            view.erase_regions(KEY)
            self.highlighting = False
            return

        visibleRegion = view.visible_region()
        if force or (self.previousRegion != visibleRegion):
            self.previousRegion = visibleRegion
            view.erase_regions(KEY)
        else:
            self.highlighting = False
            return

        # The default separator does not include whitespace, so I add that here no matter what
        separatorString = view.settings().get('word_separators', "") + " \n\r\t"
        themeSelector = view.settings().get('highlight_word_theme_selector', SCOPE)

        currentRegion = view.word(selections[0])

        # See if a word is selected or if you are just in a word
        if view.settings().get('highlight_word_require_word_select', False) and currentRegion.size() != selections[0].size():
            view.erase_regions(KEY)
            self.highlighting = False
            return

        # remove leading/trailing separator characters just in case
        currentWord = view.substr(currentRegion).strip(separatorString)

        #print u"|%s|" % currentWord
        if len(currentWord) == 0:
            view.erase_regions(KEY)
            self.highlighting = False
            return

        size = view.size() - 1
        searchStart = max(0, self.previousRegion.begin() - len(currentWord))
        searchEnd = min(size, self.previousRegion.end() + len(currentWord))

        # Reduce m*n search to just n by mapping each word separator character into a dictionary
        separators = {}
        for c in separatorString:
            separators[c] = True

        # ignore the selection if it spans multiple words
        for c in currentWord:
            if c in separators:
                self.highlighting = False
                return

        # If we are multi-selecting and all the words are the same, then we should still highlight
        if len(selections) > 1:
            for region in selections:
                word = view.substr(region).strip(separatorString)
                if word != currentWord:
                    self.highlighting = False
                    return

        validRegions = []
        while True:
            foundRegion = view.find(currentWord, searchStart, sublime.LITERAL)
            if foundRegion == None:
                break

            # regions can have reversed start/ends so normalize them
            start = max(0, foundRegion.begin())
            end = min(size, foundRegion.end())
            if searchStart == end:
                searchStart += 1
                continue
            searchStart = end

            if searchStart >= size:
                break

            if foundRegion.empty():
                break

            if foundRegion.intersects(currentRegion):
                continue

            # check if the character before and after the region is a separator character
            # if it is not, then the region is part of a larger word and shouldn't match
            # this can't be done in a regex because we would be unable to use the word_separators setting string
            if start == 0 or view.substr(sublime.Region(start - 1, start)) in separators:
                if end == size or view.substr(sublime.Region(end, end + 1)) in separators:
                    validRegions.append(foundRegion)

            if searchStart > searchEnd:
                break

        # Pick highlight style "outline" or the default "solid"
        style = sublime.DRAW_OUTLINED if view.settings().get('highlight_word_outline_style', False) == True else 0

        view.add_regions(
            KEY,
            validRegions,
            themeSelector,
            "",
            style
        )

        self.highlighting = False


class HwEventManager(object):
    @classmethod
    def load(cls):
        cls.wait_time = 0.12
        cls.time = time()
        cls.modified = False
        cls.ignore_all = False

HwEventManager.load()


class HwThreadMgr(object):
    restart = False


class HighlightWordListenerCommand(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        if HwEventManager.ignore_all:
            return
        now = time()
        if now - HwEventManager.time > HwEventManager.wait_time:
            sublime.set_timeout(lambda: hw_run(), 0)
        else:
            HwEventManager.modified = True
            HwEventManager.time = now


# Kick off hex highlighting
def hw_run():
    HwEventManager.modified = False
    # Ignore selection and edit events inside the routine
    HwEventManager.ignore_all = True
    highlight_word(sublime.active_window().active_view())
    HwEventManager.ignore_all = False
    HwEventManager.time = time()


# Start thread that will ensure highlighting happens after a barage of events
# Initial highlight is instant, but subsequent events in close succession will
# be ignored and then accounted for with one match by this thread
def hw_loop():
    while not HwThreadMgr.restart:
        if HwEventManager.modified == True and time() - HwEventManager.time > HwEventManager.wait_time:
            sublime.set_timeout(lambda: hw_run(), 0)
        elif not HwEventManager.modified:
            sublime.set_timeout(lambda: hw_run(), 0)
        sleep(0.5)

    if HwThreadMgr.restart:
        HwThreadMgr.restart = False
        sublime.set_timeout(lambda: thread.start_new_thread(hw_loop, ()), 0)


def plugin_loaded():
    global highlight_word
    highlight_word = HighlightWord().doSearch

    if not 'running_hw_loop' in globals():
        global running_hw_loop
        running_hw_loop = True
        debug("Start Thread")
        thread.start_new_thread(hw_loop, ())
    else:
        HwThreadMgr.restart = True
        debug("Restart Thread")
