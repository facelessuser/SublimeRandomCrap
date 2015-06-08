"""
Postmaster Sublime Plugin.

Allows for sending emails via SMTP.  New emails are created via a command:


Emails consist of the email content preceeded by YAML frontmatter that defines
the subject, sender, recipients, attachments and smtp servo info:

```
---
subject: Sending a file
from: Postmaster User <postmasteruser@example.com>
to: ''
cc: ''
bcc: ''
attachments:
- /Somepath/somefile.txt
smtp_server: smtp.gmail.com
port: 587
tls: true
---
Jeff,

Hey what's up. Here's a file.

~Postmaster
```

When creating an new email, postmaster looks in your Sublime User/Postmaster folder to find email templates.
These are used to create your new email with its frontmatter and content:

```js
{
    "from": "Postmaster User <postmasteruser@example.com>",
    "signature": "~Postmaster",
    "smtp_server": "smtp.gmail.com",
    "port": 587,
    "tls": true
}
```

Available template variables are:

| Name         | Type                       | Description                                                             |
|--------------|----------------------------|-------------------------------------------------------------------------|
| subject      | string                     | Email subject.                                                          |
| from         | string                     | Sender in the form `me@example.com` or `My Name <me@example.com>`.      |
| to           | string or array of strings | Recipient in the form `to@example.com` or `Their Name <to@example.com>`.|
| cc           | string or array of strings | Carbon copy recipient in the form `to@example.com` or `Their Name       |
|              |                            | <to@example.com>`.                                                      |
| bcc          | string or array of strings | Blind carbon copy recipient in the form `to@example.com` or `Their Name |
|              |                            | <to@example.com>`.                                                      |
| attachements | string or array of strings | Full file path for the attachment.                                      |
| body         | string                     | Optional default body if desired.                                       |
| smtp_server  | string                     | SMTP server used to send email.                                         |
| port         | int                        | SMTP server port used to send email.                                    |
| tls          | bool                       | Should use tls via STARTTLS.                                            |
| user         | string                     | Optional user name for SMTP server. By your default sender email will be|
|              |                            | used `me@example.com`.                                                  |

If you have multiple templates, you will prompted for which template to use.

When sending emails, you will be prompted for your password.

Just add the following commands to create and send emails:

```js
    //////////////////////////////////
    // Postmaster
    //////////////////////////////////
    {
        "caption": "Postmaster: Send Mail",
        "command": "postmaster_send"
    },
    {
        "caption": "Postmaster: New Mail",
        "command": "postmaster_new"
    },
```

If you want to right click an email in a view and send an email to it, add the following to your context menu:

```js
    {"command": "postmaster_mail_to"}
```

Licensed under MIT
Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import sublime
import sublime_plugin
import codecs
import os
import re
import yaml
import SublimeRandomCrap.postmaster as postmaster
from collections import OrderedDict

NEW_MAIL = '''---
%(header)s---
%(body)s%(signature)s
'''

SETTINGS = 'postmaster.sublime-settings'
GLOBAL_CONTACTS = 'Contacts.mail-contacts'

DEFAULT_VARS = {
    "subject": "",
    "from": "",
    "to": "",
    "cc": "",
    "bcc": "",
    "attachments": "",
    "body": "",
    "smtp_server": " smtp.gmail.com",
    "port": " 587",
    "tls": " true",
    "user": "",
    "contacts": GLOBAL_CONTACTS
}


########################
# Helper methods
########################
def get_mail_settings_dir():
    """Get mail settings dir."""

    return os.path.join(sublime.packages_path(), "User", 'Postmaster')


def yaml_dump(data, stream=None, dumper=yaml.Dumper, object_pairs_hook=OrderedDict, **kwargs):
    """Force dictionaries to be ordered on YAML dump."""

    class OrderedDumper(dumper):

        """A custom ordered dumper object."""

    OrderedDumper.add_representer(
        object_pairs_hook,
        lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
    )

    return yaml.dump(data, stream, OrderedDumper, **kwargs)


def get_mail_contacts(contact_file_path):
    """Get mail contacts."""

    contacts = {}
    if not os.path.exists(contact_file_path):
        contact_file_path = os.path.join(get_mail_settings_dir(), GLOBAL_CONTACTS)
    else:
        contact_file = contact_file_path
    if os.path.exists(contact_file):
        try:
            with codecs.open(contact_file, 'r', encoding='utf-8') as f:
                obj = yaml.load(f.read())
            for k, v in obj.items():
                contacts[k.lower()] = v
        except Exception:
            pass
    return contacts


def save_contacts(contacts, contact_file_path):
    """Save contacts."""

    if not os.path.exists(contact_file_path):
        contact_file_path = os.path.join(get_mail_settings_dir(), GLOBAL_CONTACTS)
    else:
        contact_file = contact_file_path
    try:
        with codecs.open(contact_file, 'w', encoding='utf-8') as f:
            f.write(
                yaml_dump(
                    contacts,
                    width=None, indent=4,
                    allow_unicode=True, default_flow_style=False
                )
            )
    except Exception:
        pass


def get_mail_settings():
    """Get mail settings."""

    base = get_mail_settings_dir()
    for f in os.listdir(base):
        file_path = os.path.join(base, f)
        if os.path.isfile(file_path) and file_path.lower().endswith('.mail-settings'):
            yield file_path


########################
# Compose Mail
########################
class PostmasterInsertContactCommand(sublime_plugin.TextCommand):

    """Quick insert of contacts from contact file into mail frontmatter."""

    def insert_contact(self, value):
        """Call insert with the selected contact."""
        if value >= 0:
            self.view.run_command(
                'postmaster_insert_contact',
                {"contact": self.options[value]}
            )

    def get_contact_file(self):
        """Get contact file."""

        frontmatter = postmaster.strip_frontmatter(
            self.view.substr(sublime.Region(0, self.view.size()))
        )[0]
        contacts = frontmatter.get('contacts', GLOBAL_CONTACTS)
        contact_file = os.path.join(get_mail_settings_dir(), contacts)
        if not os.path.exists(contact_file):
            contact_file = os.path.join(get_mail_settings_dir(), GLOBAL_CONTACTS)
        return contact_file

    def run(self, edit, contact=None):
        """Insert contact if provided. If not, prompt user for contact."""

        pt = self.view.sel()[0].begin()
        if contact is None and pt > 0 and self.view.substr(pt - 1) == '@':
            self.options = []
            self.view.erase(edit, sublime.Region(pt - 1, pt))
            contacts = get_mail_contacts(self.get_contact_file())
            for email, name in contacts.items():
                if not name:
                    self.options.append(email)
                else:
                    self.options.append("%s <%s>" % (name, email))
            if len(self.options):
                self.view.window().show_quick_panel(self.options, self.insert_contact)
        elif contact:
            self.view.insert(edit, pt, contact)


class PostmasterFormatMailCommand(sublime_plugin.TextCommand):

    """When creating a new mail, use a template and format desired content."""

    def format_subject(self, template_variables):
        """Format subject."""

        subject = template_variables.get('subject', None)
        if not subject or not isinstance(subject, str):
            self.template_variables['subject'] = ''
        else:
            self.template_variables['subject'] = subject

    def format_sender(self, template_variables):
        """Format sender."""

        sender = template_variables.get('from', None)
        if not sender or not isinstance(sender, str):
            self.template_variables['from'] = ''
        else:
            self.template_variables['from'] = sender

    def format_recipients(self, template_variables):
        """Format recipients."""

        for recipient in ('to', 'cc', 'bcc'):
            to = template_variables.get(recipient, None)
            if not to or not isinstance(to, (str, list, tuple, set)):
                if recipient == 'to' and self.address is not None:
                    self.template_variables[recipient] = self.address
                else:
                    self.template_variables[recipient] = ''
            elif isinstance(to, (list, tuple, set)):
                value = [r for r in to if r and isinstance(r, str)]
                if recipient == 'to' and self.address:
                    value.insert(0, self.address)
                self.template_variables[recipient] = '' if len(value) == 0 else value
            elif isinstance(to, str):
                if recipient == 'to' and self.address:
                    value = [r for r in (self.address, to) if r and isinstance(r, str)]
                    self.template_variables[recipient] = '' if len(value) == 0 else value
                else:
                    self.template_variables[recipient] = ' %s' % to

    def format_attachments(self, template_variables):
        """Format attachments."""

        attachments = template_variables.get('attachments', None)
        if not attachments or not isinstance(attachments, (str, list, tuple, set)):
            self.template_variables['attachments'] = ''
        elif isinstance(attachments, (list, tuple, set)):
            value = [a for a in attachments if a and isinstance(a, str)]
            self.template_variables['attachments'] = '' if len(value) == 0 else value
        elif isinstance(attachments, str):
            self.template_variables['attachments'] = attachments

    def format_body(self, template_variables):
        """Format body."""

        body = template_variables.get('body', None)
        if not body or not isinstance(body, str):
            self.body = ''
        else:
            self.body = ' %s' % body

    def format_signature(self, template_variables):
        """Format signature."""

        signature = template_variables.get('signature', None)
        if not signature or not isinstance(signature, str):
            self.signature = ''
        else:
            self.signature = '\n\n%s' % signature

    def format_smtp_server(self, template_variables):
        """Format smtp server."""

        server = template_variables.get('smtp_server', "smtp.gmail.com")
        if not server or not isinstance(server, str):
            self.template_variables['smtp_server'] = "smtp.gmail.com"
        else:
            self.template_variables['smtp_server'] = server

    def format_port(self, template_variables):
        """Format port."""

        port = template_variables.get('port', 587)
        if not port or not isinstance(port, int):
            self.template_variables['port'] = 587
        else:
            self.template_variables['port'] = port

    def format_tls(self, template_variables):
        """Format tls."""

        tls = template_variables.get('tls', 587)
        if not tls or not isinstance(tls, bool):
            self.template_variables['tls'] = True
        else:
            self.template_variables['tls'] = tls

    def format_user(self, template_variables):
        """Format user."""

        user = template_variables.get('user', None)
        if user and isinstance(user, str):
            self.template_variables['user'] = user

    def format_contacts(self, template_variables):
        """Format contacts."""

        contacts = template_variables.get('contacts', None)
        if contacts and isinstance(contacts, str):
            self.template_variables['contacts'] = contacts

    def run(self, edit, address=None, template_variables=DEFAULT_VARS):
        """Insert template into new mail view."""

        self.address = address if address and isinstance(address, str) else None
        self.template_variables = OrderedDict()

        # Format template values
        self.format_subject(template_variables)
        self.format_sender(template_variables)
        self.format_recipients(template_variables)
        self.format_attachments(template_variables)
        self.format_body(template_variables)
        self.format_signature(template_variables)
        self.format_smtp_server(template_variables)
        self.format_port(template_variables)
        self.format_tls(template_variables)
        self.format_user(template_variables)
        self.format_contacts(template_variables)

        self.view.insert(
            edit, 0,
            NEW_MAIL % {
                "header": yaml_dump(
                    self.template_variables,
                    width=None, indent=4,
                    allow_unicode=True, default_flow_style=False
                ),
                "body": self.body,
                "signature": self.signature
            }
        )


class PostmasterNewCommand(sublime_plugin.WindowCommand):

    """Create a new mail view to send."""

    def new_mail(self, value):
        """Open the new view with the template."""

        variables = None
        if value >= 0:
            mail_setting = self.mail_settings[value]
            try:
                with codecs.open(mail_setting, 'r', encoding='utf-8') as f:
                    variables = yaml.load(f.read())
            except Exception:
                pass

        view = self.window.new_file()
        view.run_command(
            'postmaster_format_mail',
            {
                'template_variables': variables if variables else DEFAULT_VARS,
                'address': self.address if self.address else None
            }
        )
        view.set_syntax_file("Packages/SublimeRandomCrap/PostmasterEmail.tmLanguage")

    def run(self, address=None, mail_settings=None):
        """Initiate opening new view with mail template."""

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


class PostmasterMailTo(sublime_plugin.TextCommand):

    """Context menu command to create mail from address under cursor."""

    def is_visible(self, event):
        """Don't show in context menu unless there is an address."""

        return self.find_address(event) is not None

    def find_address(self, event):
        """Retrieve the address from the view."""

        address = None
        pt = self.view.window_to_text((event["x"], event["y"]))
        line = self.view.line(pt)

        line.a = max(line.a, pt - 1024)
        line.b = min(line.b, pt + 1024)

        text = self.view.substr(line)

        it = postmaster.RE_MAIL.finditer(text)

        for match in it:
            if match.start() <= (pt - line.a) and match.end() >= (pt - line.a):
                address = text[match.start():match.end()]
                break

        return address

    def description(self, event):
        """Display address to mail to in context menu."""

        address = self.find_address(event)
        if len(address) > 64:
            address = address[0:64] + "..."
        return "Mail To: " + address

    def want_event(self):
        """Receive event."""

        return True

    def run(self, edit, event):
        """Create new email to the given address."""

        address = self.find_address(event)
        if address:
            self.view.window().run_command('postmaster_new', {"address": address})


class PostmasterListener(sublime_plugin.EventListener):

    """Postmaster listener."""

    def on_selection_modified(self, view):
        """
        Try to force the selection in an password panel to be at end.

        Milage may vary.
        """

        if view is not None and view.settings().get('postmaster_password_panel', False):
            view.sel().clear()
            view.sel().add(sublime.Region(view.size()))


########################
# Send Mail
########################
class PostmasterSendCommand(sublime_plugin.TextCommand):

    """Send the mail from the current view buffer."""

    def send_with_auth(self, value):
        """Send with the settings."""

        if value:
            value = self.auth
            self.auth = ''
            self.send(value)
        else:
            self.auth = ''

    def hide_auth(self, password):
        """Hide auth input."""

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
        """Clear auth value."""

        self.auth = ''

    def store_contacts(self, mg):
        """Store contacts."""

        settings = sublime.load_settings(SETTINGS)
        if settings.get('save_contacts'):
            contacts = []
            for contact in (mg.to + mg.cc + mg.bcc):
                record = postmaster.parse_contact(contact)
                if record is not None:
                    contacts.append(record)
            contact_list = get_mail_contacts(self.contacts)
            for c in contacts:
                contact_list[c[0]] = c[1].strip()
            save_contacts(contact_list, self.contacts)

    def send(self, auth):
        """Using the settings file to send the mail."""

        if auth:
            pm = postmaster.SendSmtp(self.smtp_server, self.port, self.tls)
            try:
                response = pm.sendmail(self.bfr, auth, self.user)

                # Parse response
                m = re.match(r'<Response \[(\d+)\]>', response)
                if m and m.group(1) == '200':
                    # Mail sent
                    self.store_contacts(pm)
                    sublime.status_message('Mail successfully sent!')
                elif m:
                    # Mail sending failed with the following response
                    sublime.error_message('Mail failed with code %s!' % m.group(1))
                else:
                    # Something else got returned
                    sublime.error_message('Mail failed with unknown error!\nSee console for more info.')
                    print(str(response))

            except Exception as e:
                sublime.error_message('Mail failed with unknown error!\nSee console for more info.')
                sublime.error_message(str(e))
        else:
            sublime.error_message('Auth was not provided!')

    def run(self, edit):
        """Initiate mail sending."""

        self.auth = ''
        self.window = self.view.window()
        self.user = None

        self.bfr = self.view.substr(sublime.Region(0, self.view.size()))
        frontmatter = postmaster.strip_frontmatter(self.bfr)[0]

        smtp_server = frontmatter.get('smtp_server', None)
        if smtp_server and isinstance(smtp_server, str):
            self.smtp_server = smtp_server
        else:
            self.smtp_server = None

        port = frontmatter.get('port', None)
        if port and isinstance(port, int):
            self.port = port
        else:
            self.port = None

        tls = frontmatter.get('tls', None)
        if tls and isinstance(tls, bool):
            self.tls = tls
        else:
            self.tls = None

        user = frontmatter.get('user', None)
        if user and isinstance(user, str):
            self.user = user
        else:
            self.user = None

        contacts = frontmatter.get('contacts', GLOBAL_CONTACTS)
        if contacts and isinstance(contacts, str):
            full_path = os.path.join(get_mail_settings_dir(), contacts)
            if os.path.exists(full_path):
                self.contacts = full_path
            else:
                self.contacts = os.path.join(get_mail_settings_dir(), GLOBAL_CONTACTS)
        else:
            self.contacts = os.path.join(get_mail_settings_dir(), GLOBAL_CONTACTS)

        self.port = frontmatter.get('port', None)
        self.tls = frontmatter.get('tls', None)
        if self.smtp_server and self.port is not None and self.tls is not None:
            view = self.window.show_input_panel('Password:', '', self.send_with_auth, self.hide_auth, self.clear_auth)
            view.settings().set('postmaster_password_panel', True)


def plugin_loaded():
    """Make sure mail setting folder exists."""

    mail_folder = get_mail_settings_dir()
    if not os.path.exists(mail_folder):
        os.makedirs(mail_folder)
