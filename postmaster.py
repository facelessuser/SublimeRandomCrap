"""
Postmaster

Licensed under MIT
Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import requests
import yaml
import json
import os
import re
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


EMAIL = r'''
(?:[\-+\w]([\w\-+]|\.(?!\.))+)        # Local part
@(?:[\w\-]+\.)                        # @domain part start
(?:(?:[\w\-]|(?<!\.)\.(?!\.))*)[a-z]  # @domain.end (allow multiple dot names)
(?![\d\-_@])                          # Don't allow last char to be followed by these
'''

RE_MAIL = re.compile(r'''(?x)(?i)(?P<email>%s)''' % EMAIL)

RE_CONTACT = re.compile(
    r'''(?x)(?i)\s*(?:(?P<name>.*?)<(?P<email>%s)>|(?P<email2>%s))\s*''' % (EMAIL, EMAIL)
)


def is_contact(contact):
    """ Is string a contact? """
    return RE_CONTACT.match(contact) is not None


def parse_contact(contact):
    """ Parse contact """
    m = RE_CONTACT.match(contact)
    contact_record = None
    if m:
        if m.group('name'):
            contact_record = (m.group('email').lower(), m.group('name'))
        else:
            contact_record = (m.group('email2').lower(), '')
    return contact_record


def convert_file_size(from_size, to_size, value):
    """ Convert byte sizes """
    file_sizes = ('bytes', 'kilo', 'mega', 'giga', 'tera', 'peta')
    if from_size != 'bytes':
        value = value * (1024.0 ** file_sizes.index(from_size))
    return float(value) / (1024.0 ** file_sizes.index(to_size))


def strip_frontmatter(string):
    """ Get frontmatter from string """
    frontmatter = {}

    if string.startswith("---"):
        m = re.search(r'^(---(.*?)---[ \t]*\r?\n)', string, re.DOTALL)
        if m:
            try:
                frontmatter = json.loads(m.group(2))
            except:
                try:
                    frontmatter = yaml.load(m.group(2))
                except:
                    pass
            string = string[m.end(1):]

    return frontmatter, string


class PostmasterException(Exception):
    pass


class SendMailGunApi(object):
    def __init__(self):
        """ Initialize mail variables """
        self.sender = None
        self.reply = None
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = None
        self.text = None
        self.attachments = []

    def get_email_size(self):
        """ Get size of email in bytes """
        size = len(self.text.encode('utf-8'))
        for attachment in self.attachments:
            try:
                size += os.path.getsize(attachment)
            except:
                pass
        return size

    def send(self, api_url, api_key):
        """ Send email via MailGun's API """

        if convert_file_size('bytes', 'mega', self.get_email_size()) > 25:
            raise PostmasterException('Message exceeds 25MB!')

        # Prepare attachments
        files = []
        for attachment in self.attachments:
            try:
                f = ("attachment", open(attachment))
                files.append(f)
            except:
                pass

        # Prepare data structure
        data = {
            "from": self.sender,
            "h:Reply-To": self.reply,
            "to": self.to,
            "cc": self.cc,
            "bcc": self.bcc,
            "subject": self.subject,
            "text": self.text
        }

        # Attempt to physically send email
        response = requests.post(
            api_url + '/messages',
            auth=("api", api_key),
            files=files,
            data=data,
            timeout=5
        )

        return str(response)

    def set_sender(self, sender):
        """ Set sender """
        if sender and isinstance(sender, str):
            contact = parse_contact(sender)
            if contact is not None:
                self.sender = '%s <%s>' % (contact[1], contact[0]) if contact[1] else contact[0]
                self.reply = contact[0]

    def set_recipients(self, recipient_type, recipients):
        """ Set recipient """
        to = getattr(self, recipient_type)
        if recipients:
            if isinstance(recipients, str) and is_contact(recipients):
                to.append(recipients)
            elif isinstance(recipients, list):
                for recipient in recipients:
                    if recipient and isinstance(recipient, str) and is_contact(recipient):
                        to.append(recipient)

    def set_subject(self, subject):
        """ Set subject """
        self.subject = subject if subject and isinstance(subject, str) else "No Subject"

    def set_attachments(self, attachments):
        """ Populate attachment list """
        if attachments:
            if isinstance(attachments, str):
                if os.path.exists(attachments):
                    self.attachments.append(attachments)
            elif isinstance(attachments, list):
                for attachment in attachments:
                    if os.path.exists(attachment):
                        self.attachments.append(attachment)

    def set_body(self, body):
        """ Set body """
        self.text = body if body else ''

    def sendmail(self, string):
        """ Parse mail buffer and send it """
        response = None

        #  Strip mail frontmatter from mail text
        frontmatter, body = strip_frontmatter(string)

        self.set_sender(frontmatter.get('from', None))
        for x in ('to', 'cc', 'bcc'):
            self.set_recipients(x, frontmatter.get(x, []))
        self.set_subject(frontmatter.get('subject', None))
        self.set_attachments(frontmatter.get('attachment', []))
        self.set_body(body)

        # Send message if we have enough info
        if self.sender and self.to and (self.text or len(self.attachments)):
            # If text is empty, make sure it is at least a string.
            response = self.send()
        else:
            raise PostmasterException('Message configuration did not meet the minimum requirements!')

        return response


class SendSmtp(object):
    def __init__(self, smtp_server, port, tls=True):
        """ Initialize mail variables """
        # Server settings
        self.server = smtp_server
        self.port = port
        self.tls = tls

        # Mail header settings
        self.sender = None
        self.reply = None
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = None
        self.text = None
        self.attachments = []

    def get_email_size(self):
        """ Get size of email in bytes """
        size = len(self.text.encode('utf-8'))
        for attachment in self.attachments:
            try:
                size += os.path.getsize(attachment)
            except:
                pass
        return size

    def send(self, auth, user=None):
        """ Send email via smtp """

        if convert_file_size('bytes', 'mega', self.get_email_size()) > 25:
            raise PostmasterException('Message exceeds 25MB!')

        # create the message
        msg = MIMEMultipart()
        msg["From"] = self.sender
        msg["Reply-To"] = self.reply
        msg["Subject"] = self.subject
        msg["Date"] = formatdate(localtime=True)
        msg["To"] = ', '.join(self.to)
        msg["Cc"] = ', '.join(self.cc)
        msg["Bcc"] = ', '.join(self.bcc)

        # Prepare attachments
        for a in self.attachments:
            try:
                with open(a, "rb") as f:
                    part = MIMEBase('application', "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(a))
                    msg.attach(part)
            except:
                pass

        msg.attach(MIMEText(self.text))
        server = smtplib.SMTP(self.server, self.port)
        if self.tls:
            # identify ourselves to smtp client
            server.ehlo()
            # secure our email with tls encryption
            server.starttls()
            # re-identify ourselves as an encrypted connection
            server.ehlo()
        server.login(self.reply if user is None else user, auth)
        try:
            server.sendmail(self.reply, self.to + self.cc + self.bcc, msg.as_string())
            server.quit()
        except:
            server.quit()
            raise PostmasterException('SMTP mail sending failed!')

        return str('<Response [200]>')

    def set_sender(self, sender):
        """ Set sender """
        if sender and isinstance(sender, str):
            contact = parse_contact(sender)
            if contact is not None:
                self.sender = '%s <%s>' % (contact[1], contact[0]) if contact[1] else contact[0]
                self.reply = contact[0]

    def set_recipients(self, recipient_type, recipients):
        """ Set recipient """
        to = getattr(self, recipient_type)
        if recipients:
            if isinstance(recipients, str) and is_contact(recipients):
                to.append(recipients)
            elif isinstance(recipients, list):
                for recipient in recipients:
                    if recipient and isinstance(recipient, str) and is_contact(recipient):
                        to.append(recipient)

    def set_subject(self, subject):
        """ Set subject """
        self.subject = subject if subject and isinstance(subject, str) else "No Subject"

    def set_attachments(self, attachments):
        """ Populate attachment list """
        if attachments:
            if isinstance(attachments, str):
                if os.path.exists(attachments):
                    self.attachments.append(attachments)
            elif isinstance(attachments, list):
                for attachment in attachments:
                    if attachment and isinstance(attachment, str) and os.path.exists(attachment):
                        self.attachments.append(attachment)

    def set_body(self, body):
        """ Set body """
        self.text = body if body else ''

    def sendmail(self, string, auth, user=None):
        """ Parse mail buffer and send it """
        response = None

        #  Strip mail frontmatter from mail text
        frontmatter, body = strip_frontmatter(string)

        self.set_sender(frontmatter.get('from', None))
        for x in ('to', 'cc', 'bcc'):
            self.set_recipients(x, frontmatter.get(x, []))
        self.set_subject(frontmatter.get('subject', None))
        self.set_attachments(frontmatter.get('attachments', []))
        self.set_body(body)

        # Send message if we have enough info
        if self.sender and self.to and (self.text or len(self.attachments)):
            # If text is empty, make sure it is at least a string.
            response = self.send(auth, user=user)
        else:
            raise PostmasterException('Message configuration did not meet the minimum requirements!')

        return response
