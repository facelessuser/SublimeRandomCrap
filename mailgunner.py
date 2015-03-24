import sublime
import sublime_plugin
import codecs
import os
import re
import json
import SublimeRandomCrap.mailgun as mailgun

NEW_MAIL = '''---
subject:
from:
reply:
to: []
cc: []
bcc: []
attachements: []
---
Message here!
'''


class MailGunnerFormatMailCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, NEW_MAIL)


class MailGunnerNewCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file()
        view.run_command('mail_gun_format_mail')


class MailGunnerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        mail_settings = None
        api_key = None
        api_url = None
        settings = sublime.load_settings('mailgun.sublime-settings')
        mail_info = settings.get('mail_settings', {})
        if os.path.exists(mail_info):
            with codecs.open(mail_info, "r", encoding='utf8') as f:
                mail_settings = json.loads(f.read())
        if mail_settings:
            api_key = mail_settings.get('api_key', None)
            api_url = mail_settings.get('api_url', None)

        if api_key and api_url:
            mg = mailgun.MailGun(api_url, api_key)
            try:
                response = mg.sendmail(
                    self.view.substr(sublime.Region(0, self.view.size()))
                )

                # Parse response
                m = re.match(r'<Response \[(\d+)\]>', response)
                if m and m.group(1) == '200':
                    # Mail sent
                    sublime.status_message('Mail successfully sent!')
                elif m:
                    # Mail sending failed with the following response
                    sublime.error_message('Mail failed with code %s!' % m.group(1))
                else:
                    # Something else got returned
                    sublime.error_message('Mail failed with unknown error: %s!' % response)

            except mailgun.MailGunException as e:
                sublime.error_message(str(e))
        else:
            sublime.error_message('Could not find MailGun API setup info!')
