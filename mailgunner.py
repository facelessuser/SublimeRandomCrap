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


def get_mail_settings_dir():
    return os.path.join(sublime.packages_path(), "User", 'MailGunner')


def get_mail_settings():
    base = get_mail_settings_dir()
    for f in os.listdir(base):
        file_path = os.path.join(base, f)
        if os.path.isfile(file_path) and file_path.lower().endswith('.mail-settings'):
            yield os.path.basename(file_path)


class MailGunnerFormatMailCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, NEW_MAIL)


class MailGunnerNewCommand(sublime_plugin.WindowCommand):
    def run(self):
        view = self.window.new_file()
        view.run_command('mail_gun_format_mail')


class MailGunnerCommand(sublime_plugin.TextCommand):
    def send_with_settings(self, value):
        if value >= 0:
            mail_setting = self.mail_settings[value]
            settings = {}
            setting_file = os.path.join(get_mail_settings_dir(), mail_setting)
            if os.path.exists(setting_file):
                try:
                    with codecs.open(setting_file, "r", encoding='utf8') as f:
                        settings = json.loads(f.read())
                except:
                    pass
            self.send(settings)

    def send(self, mail_settings):
        """ Using the settings file to send the mail """
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

    def run(self, edit, mail_setting=None):
        """ Initiate mail sending """
        if mail_setting is not None:
            settings = os.path.join(get_mail_settings_dir(), mail_setting)
            if not os.path.exists(settings):
                mail_setting = None

        if mail_setting:
            self.mail_settings = [mail_setting]
            entries = 1
        else:
            self.mail_settings = []
            for setting in get_mail_settings():
                self.mail_settings.append(setting)
            entries = len(self.mail_settings)

        if entries:
            if entries == 1:
                self.send_with_settings(0)
            else:
                self.view.window().show_quick_panel(
                    self.mail_settings,
                    self.send_with_settings
                )
        else:
            sublime.error_message('No mail configurations available!')


def plugin_loaded():
    # Make sure mail setting folder exists
    mail_folder = get_mail_settings_dir()
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)
