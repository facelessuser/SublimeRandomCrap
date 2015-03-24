import requests
import yaml
import json
import os
import re


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


class MailGunException(Exception):
    pass


class MailGun(object):
    def __init__(self, api_url, api_key):
        """ Initialize mail variables """
        self.sender = None
        self.reply = None
        self.to = []
        self.cc = []
        self.bcc = []
        self.subject = None
        self.text = None
        self.attachments = []
        self.api_url = api_url
        self.api_key = api_key

    def get_email_size(self):
        """ Get size of email in bytes """
        size = len(self.text.encode('utf-8'))
        for attachment in self.attachments:
            try:
                size += os.path.getsize(attachment)
            except:
                pass
        return size

    def send(self):
        """ Send email via MailGun's API """

        if convert_file_size('bytes', 'mega', self.get_email_size()) > 25:
            raise MailGunException('Message exceeds 25MB!')

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
            "to": self.to,
            "cc": self.cc,
            "bcc": self.bcc,
            "subject": self.subject,
            "text": self.text
        }

        # Add reply if provided
        if self.reply:
            data["h:Reply-To"] = self.reply

        # Attempt to physically send email
        response = requests.post(
            self.api_url + '/messages',
            auth=("api", self.api_key),
            files=files,
            data=data,
            timeout=5
        )

        return str(response)

    def set_sender(self, sender, reply):
        """ Set sender and reply email """
        if sender and isinstance(sender, str):
            self.sender = sender

        if reply and isinstance(reply, str):
            self.reply = reply

        # Use reply as sender name if reply is specified
        # and sender (from) is not
        if not self.sender and self.reply:
            self.sender = self.reply

    def set_recipients(self, recipient_type, recipients):
        """ Set recipient """
        to = getattr(self, recipient_type)
        if recipients:
            if isinstance(recipients, str):
                to.append(recipients)
            elif isinstance(recipients, list):
                for recipient in recipients:
                    if recipient and isinstance(recipient, str):
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
        response = "Mail Fail"

        #  Strip mail frontmatter from mail text
        frontmatter, body = strip_frontmatter(string)

        self.set_sender(
            frontmatter.get('from', None),
            frontmatter.get('reply', None)
        )
        for x in ('to', 'cc', 'bcc'):
            self.set_recipients(x, frontmatter.get(x, []))
        self.set_subject(frontmatter.get('subject', None))
        self.set_attachments(frontmatter.get('attachment', []))
        self.set_body(body)

        # Send message if we have enough info
        if self.reply and self.to and (self.text or len(self.attachments)):
            # If text is empty, make sure it is at least a string.
            response = self.send()
        else:
            raise MailGunException('Message configuration did not meet the minimum requirements!')

        return response
