import sublime_plugin
from datetime import datetime
import time


class InsertDateTimeCommand(sublime_plugin.TextCommand):
    def run(self, edit, format="%Y-%m-%d", utc=False):
        if utc:
            date_time = time.strftime(format, time.gmtime())
        else:
            date_time = datetime.now().strftime(format)
        for sel in self.view.sel():
             self.view.replace(edit, sel, date_time)
