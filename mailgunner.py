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
attachments:%(attachments)s
---
%(body)s%(signature)s
'''

DEFAULT_VARS = {
    "subject": "",
    "from": "",
    "to": "",
    "cc": "",
    "bcc": "",
    "attachments": "",
    "body": ""
}


########################
# Helper methods
########################
def get_mail_settings_dir():
    """ Get mail settings dir """
    return os.path.join(sublime.packages_path(), "User", 'MailGunner')


def get_mail_contacts():
    """ Get mail contacts """
    contacts = {}
    base = get_mail_settings_dir()
    contact_file = os.path.join(base, 'Contacts.mail-contacts')
    if os.path.exists(contact_file):
        try:
            with codecs.open(contact_file, 'r', encoding='utf-8') as f:
                obj = json.loads(f.read())
            for k, v in obj.items():
                contacts[k.lower()] = v
        except:
            pass
    return contacts


def save_contacts(contacts):
    """ Save contacts """
    base = get_mail_settings_dir()
    contact_file = os.path.join(base, 'Contacts.mail-contacts')
    try:
        with codecs.open(contact_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(contacts, sort_keys=True, indent=4, separators=(',', ': ')))
    except:
        pass


def get_mail_settings():
    """ Get mail settings """
    base = get_mail_settings_dir()
    for f in os.listdir(base):
        file_path = os.path.join(base, f)
        if os.path.isfile(file_path) and file_path.lower().endswith('.mail-settings'):
            yield file_path


########################
# Compose Mail
########################
class MailGunnerInsertContactCommand(sublime_plugin.TextCommand):
    """ Quick insert of contacts from contact file into mail frontmatter """
    def insert_contact(self, value):
        """ Call insert with the selected contact """
        if value >= 0:
            self.view.run_command(
                'mail_gunner_insert_contact',
                {"contact": self.options[value]}
            )

    def run(self, edit, contact=None):
        """ Insert contact if provided. If not, prompt user for contact. """
        pt = self.view.sel()[0].begin()
        if contact is None and pt > 0 and self.view.substr(pt - 1) == '@':
            self.options = []
            self.view.erase(edit, sublime.Region(pt - 1, pt))
            contacts = get_mail_contacts()
            for email, name in contacts.items():
                if not name:
                    self.options.append(email)
                else:
                    self.options.append("%s <%s>" % (name, email))
            if len(self.options):
                self.view.window().show_quick_panel(self.options, self.insert_contact)
        elif contact:
            self.view.insert(edit, pt, contact)


class MailGunnerFormatMailCommand(sublime_plugin.TextCommand):
    """ When creating a new mail, use a template and format desired content. """
    def format_subject(self):
        """ Format subject """
        subject = self.template_variables.get('subject', None)
        if not subject or not isinstance(subject, str):
            self.template_variables['subject'] = ''
        else:
            self.template_variables['subject'] = ' %s' % subject

    def format_sender(self):
        """ Format sender """
        sender = self.template_variables.get('from', None)
        if not sender or not isinstance(sender, str):
            self.template_variables['from'] = ''
        else:
            self.template_variables['from'] = ' %s' % sender

    def format_recipients(self):
        """ Format recipients """
        for recipient in ('to', 'cc', 'bcc'):
            to = self.template_variables.get(recipient, None)
            if not to or not isinstance(to, (str, list, tuple, set)):
                self.template_variables[recipient] = ' %s' % self.address if recipient == 'to' and self.address is not None else ''
            elif isinstance(to, (list, tuple, set)):
                value = ['\n- %s' % r for r in to if r and isinstance(r, str)]
                if recipient == 'to' and self.address:
                    value.insert(0, self.address)
                self.template_variables[recipient] = '' if len(value) == 0 else ''.join(value)
            elif isinstance(to, str):
                if recipient == 'to' and self.address:
                    value = ['\n- %s' % r for r in (self.address, to) if r and isinstance(r, str)]
                    self.template_variables[recipient] = '' if len(value) == 0 else ''.join(value)
                else:
                    self.template_variables[recipient] = ' %s' % to

    def format_attachments(self):
        """ Format attachments """
        attachments = self.template_variables.get('attachments', None)
        if not attachments or not isinstance(attachments, (str, list, tuple, set)):
            self.template_variables['attachments'] = ''
        elif isinstance(attachments, (list, tuple, set)):
            value = ['\n- %s' % a for a in attachments if a and isinstance(a, str)]
            self.template_variables['attachments'] = '' if len(value) == 0 else ''.join(value)
        elif isinstance(attachments, str):
            self.template_variables['attachments'] = ' %s' % attachments

    def format_body(self):
        """ Format body """
        body = self.template_variables.get('body', None)
        if not body or not isinstance(body, str):
            self.template_variables['body'] = ''
        else:
            self.template_variables['body'] = ' %s' % body

    def format_signature(self):
        """ Format signature """
        signature = self.template_variables.get('signature', None)
        if not signature or not isinstance(signature, str):
            self.template_variables['signature'] = ''
        else:
            self.template_variables['signature'] = '\n\n%s' % signature

    def run(self, edit, address=None, template_variables=DEFAULT_VARS):
        """ Insert template into new mail view """
        self.address = address if address and isinstance(address, str) else None
        self.template_variables = template_variables

        # Format template values
        self.format_subject()
        self.format_sender()
        self.format_recipients()
        self.format_attachments()
        self.format_body()
        self.format_signature()

        self.view.insert(edit, 0, NEW_MAIL % template_variables)


class MailGunnerNewCommand(sublime_plugin.WindowCommand):
    """ Create a new mail view to send """
    def new_mail(self, value):
        """ Open the new view with the template """
        vars = None
        if value >= 0:
            mail_setting = self.mail_settings[value]
            try:
                with codecs.open(mail_setting, 'r', encoding='utf-8') as f:
                    vars = json.loads(f.read())
            except:
                pass

        view = self.window.new_file()
        view.run_command(
            'mail_gunner_format_mail',
            {
                'template_variables': vars if vars else DEFAULT_VARS,
                'address': self.address if self.address else None
            }
        )
        view.set_syntax_file("Packages/SublimeRandomCrap/Email.tmLanguage")

    def run(self, address=None, mail_settings=None):
        """ Initiate opening new view with mail template """
        self.address = address if address and isinstance(address, str) else None
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
                self.window.show_quick_panel(
                    mail_menu,
                    self.new_mail
                )
        else:
            # No config provided
            self.new_mail(-1)


class MailGunnerMailTo(sublime_plugin.TextCommand):
    """ Context menu command to create mail from address under cursor """
    def is_visible(self, event):
        """ Don't show in context menu unless there is an address """
        return self.find_address(event) is not None

    def find_address(self, event):
        """ Retrieve the address from the view """
        address = None
        pt = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(pt)

        line.a = max(line.a, pt - 1024)
        line.b = min(line.b, pt + 1024)

        text = self.view.substr(line)

        it = mailgun.RE_MAIL.finditer(text)

        for match in it:
            if match.start() <= (pt - line.a) and match.end() >= (pt - line.a):
                address = text[match.start():match.end()]
                break

        return address

    def description(self, event):
        """ Display address to mail to in context menu """
        address = self.find_address(event)
        if len(address) > 64:
            address = address[0:64] + "..."
        return "Mail To: " + address

    def want_event(self):
        """ Receive event """
        return True

    def run(self, edit, event):
        """ Create new email to the given address """
        address = self.find_address(event)
        if address:
            self.view.window().run_command('mail_gunner_new', {"address": address})


class MailGunnerListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        if view is not None and view.settings().get('mail_gunner_password', False):
            view.sel().clear()
            view.sel().add(sublime.Region(view.size()))


########################
# Send Mail
########################
class MailGunnerSendCommand(sublime_plugin.TextCommand):
    """ Send the mail from the current view buffer """
    def send_with_auth(self, value):
        """ Send with the settings """
        if value:
            value = self.auth
            self.auth = ''
            self.send(value)
        else:
            self.auth = ''

    def hide_auth(self, password):
        if len(password) > len(self.auth):
            self.auth += password[len(self.auth):]
            password = '*' * len(self.auth)
        elif len(password) < len(self.auth):
            self.auth = self.auth[:len(password)]
            password = '*' * len(self.auth)
        else:
            return
        view = self.window.show_input_panel("Password", password, self.send_with_auth, self.hide_auth, self.clear_auth)
        view.sel().clear()
        view.sel().add(sublime.Region(view.size()))

    def clear_auth(self):
        self.auth = ''

    def store_contacts(self, mg):
        """ Store contacts """
        contacts = []
        for contact in (mg.to + mg.cc + mg.bcc):
            record = mailgun.parse_contact(contact)
            if record is not None:
                contacts.append(record)
        contact_list = get_mail_contacts()
        for c in contacts:
            contact_list[c[0]] = c[1]
        save_contacts(contact_list)

    def send(self, auth):
        """ Using the settings file to send the mail """

        if auth:
            mg = mailgun.MailGunSmtp(auth)
            try:
                response = mg.sendmail(
                    self.view.substr(sublime.Region(0, self.view.size()))
                )

                # Parse response
                m = re.match(r'<Response \[(\d+)\]>', response)
                if m and m.group(1) == '200':
                    # Mail sent
                    self.store_contacts(mg)
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
        self.auth = ''
        self.window = self.view.window()
        view = self.window.show_input_panel('Password:', '', self.send_with_auth, self.hide_auth, self.clear_auth)
        view.settings().set('mail_gunner_password', True)


def plugin_loaded():
    # Make sure mail setting folder exists
    mail_folder = get_mail_settings_dir()
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)
