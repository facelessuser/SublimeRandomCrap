import sublime
import sublime_plugin
import codecs
import os
import re
import json
import SublimeRandomCrap.mailgun as mailgun

NEW_MAIL = '''---
subject:%(subject)s
from:%(from)s
to:%(to)s
cc:%(cc)s
bcc:%(bcc)s
attachements:%(attachements)s
keyfile:%(keyfile)s
---
%(body)s%(signature)s
'''

DEFAULT_VARS = {
    "subject": "",
    "from": "",
    "to": "",
    "cc": "",
    "bcc": "",
    "attachements": "",
    "body": "",
    "keyfile": ""
}


def get_mail_settings_dir():
    """ Get mail settings dir """
    return os.path.join(sublime.packages_path(), "User", 'MailGunner')


def get_mail_settings():
    """ Get mail settings """
    base = get_mail_settings_dir()
    for f in os.listdir(base):
        file_path = os.path.join(base, f)
        if os.path.isfile(file_path) and file_path.lower().endswith('.mail-settings'):
            yield file_path


class MailGunnerFormatMailCommand(sublime_plugin.TextCommand):
    def run(self, edit, template_variables=DEFAULT_VARS):
        """ Insert template into new mail view """
        subject = template_variables.get('subject', None)
        if not subject or not isinstance(subject, str):
            template_variables['subject'] = ''
        else:
            template_variables['subject'] = ' %s' % subject

        sender = template_variables.get('from', None)
        if not sender or not isinstance(sender, str):
            template_variables['from'] = ''
        else:
            template_variables['from'] = ' %s' % sender

        for recipient in ('to', 'cc', 'bcc'):
            to = template_variables.get(recipient, None)
            if not to or not isinstance(to, (str, list, tuple, set)):
                template_variables[recipient] = ''
            elif isinstance(to, (list, tuple, set)):
                value = ['\n- %s' % r for r in to if r and isinstance(r, str)]
                template_variables[recipient] = '' if len(value) == 0 else ''.join(value)
            elif isinstance(to, str):
                template_variables[recipient] = ' %s' % to

        attachements = template_variables.get('attachements', None)
        if not attachements or not isinstance(attachements, (str, list, tuple, set)):
            template_variables['attachements'] = ''
        elif isinstance(attachements, (list, tuple, set)):
            value = ['\n- %s' % a for a in attachements if a and isinstance(a, str)]
            template_variables['attachements'] = '' if len(value) == 0 else ''.join(value)
        elif isinstance(attachements, str):
            template_variables['attachements'] = ' %s' % attachements

        keyfile = template_variables.get('keyfile', None)
        if not keyfile or not isinstance(keyfile, str):
            template_variables['keyfile'] = ''
        else:
            template_variables['keyfile'] = ' %s' % keyfile

        body = template_variables.get('body', None)
        if not body or not isinstance(body, str):
            template_variables['body'] = ''
        else:
            template_variables['body'] = ' %s' % body

        signature = template_variables.get('signature', None)
        if not signature or not isinstance(signature, str):
            template_variables['signature'] = ''
        else:
            template_variables['signature'] = '\n\n%s' % signature

        self.view.insert(edit, 0, NEW_MAIL % template_variables)


class MailGunnerNewCommand(sublime_plugin.WindowCommand):
    def new_mail(self, value):
        """ Open the new view with the template """
        vars = None
        if value >= 0:
            mail_setting = self.mail_settings[value]
            try:
                with codecs.open(mail_setting, 'r', encoding='utf-8') as f:
                    vars = json.loads(f.read())
                keyfile = vars.get('keyfile', None)
                print(keyfile)
                if not keyfile or not isinstance(keyfile, str):
                    vars['keyfile'] = os.path.basename(mail_setting)
                if 'api_key' in vars:
                    del vars['api_key']
                if 'api_url' in vars:
                    del vars['api_url']
            except:
                pass

        view = self.window.new_file()
        view.run_command(
            'mail_gunner_format_mail',
            {'template_variables': vars if vars else DEFAULT_VARS}
        )

    def run(self, mail_settings=None):
        """ Initiate opening new view with mail template """
        mail_menu = []
        if mail_settings is not None:
            # Mail config file provided
            settings = os.path.join(get_mail_settings_dir(), mail_settings)
            if not os.path.exists(settings):
                mail_settings = None
            else:
                mail_settings = settings

        if mail_settings:
            # Use mail conifig to populate new mail template
            mail_menu = [os.path.splitext(os.path.basename(mail_settings))[0]]
            self.mail_settings = [mail_settings]
            entries = 1
        else:
            # Find all configs that can populate new mail template
            self.mail_settings = []
            for setting in get_mail_settings():
                mail_menu.append(os.path.splitext(os.path.basename(setting))[0])
                self.mail_settings.append(setting)
            entries = len(self.mail_settings)

        if entries:
            if entries == 1:
                # Only one config available; use it
                self.new_mail(0)
            else:
                # Prompt user to pick config to populate template
                self.view.window().show_quick_panel(
                    mail_menu,
                    self.new_mail
                )
        else:
            # No config provided
            self.new_mail(-1)


class MailGunnerCommand(sublime_plugin.TextCommand):
    def send_with_settings(self, value):
        """ Send with the settings """
        if value >= 0:
            mail_setting = self.mail_settings[value]
            settings = {}
            if os.path.exists(mail_setting):
                try:
                    with codecs.open(mail_setting, "r", encoding='utf8') as f:
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

    def run(self, edit, mail_settings=None):
        """ Initiate mail sending """
        mail_menu = []
        if mail_settings is not None:
            # Keyfile fed in via argument
            settings = os.path.join(get_mail_settings_dir(), mail_settings)
            if not os.path.exists(settings):
                mail_settings = None
            else:
                mail_settings = settings
        else:
            # Keyfile found in frontmatter
            bfr = self.view.substr(sublime.Region(0, self.view.size()))
            frontmatter = mailgun.strip_frontmatter(bfr)[0]
            if frontmatter is not None:
                keyfile = frontmatter.get('keyfile', None)
                if keyfile and isinstance(keyfile, str):
                    settings = os.path.join(get_mail_settings_dir(), keyfile)
                    if os.path.exists(settings):
                        mail_settings = settings

        if mail_settings:
            # Mail setting to use already provided
            mail_menu = [os.path.splitext(os.path.basename(mail_settings))[0]]
            self.mail_settings = [mail_settings]
            entries = 1
        else:
            # Search for available mail settings
            self.mail_settings = []
            for setting in get_mail_settings():
                mail_menu.append(os.path.splitext(os.path.basename(setting))[0])
                self.mail_settings.append(setting)
            entries = len(self.mail_settings)

        if entries:
            if entries == 1:
                # Send with the only option
                self.send_with_settings(0)
            else:
                # Prompt user to pick which send config to use
                self.view.window().show_quick_panel(
                    mail_menu,
                    self.send_with_settings
                )
        else:
            sublime.error_message('No mail configurations available!')


def plugin_loaded():
    # Make sure mail setting folder exists
    mail_folder = get_mail_settings_dir()
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)
