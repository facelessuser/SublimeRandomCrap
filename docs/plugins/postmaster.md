# Postmaster (EXPERIMENTAL) {: .doctitle}
Send emails from Sublime Text.

---

Allows for sending emails via SMTP.  New emails are created via a command:

Emails consist of the email content preceded by YAML frontmatter that defines
the subject, sender, recipients, attachments and SMTP servo info:

```
---
subject: Sending a file
from: Postmaster User <postmasteruser@example.com>
to: Someone <someone@example.com>
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

New emails can be configured with templates. If you have multiple templates, you will prompted for which template to use.

Currently, postmaster will store all the email address you write to in `User/Postmaster/Contacts.mail-contacts` (this will be optional in the future).  So when you are in the frontmatter, you can type <kbd>@</kbd> and then <kbd>Tab</kbd> and a panel will open from which you can pick a contact to insert.

When sending emails, you will be prompted for your password.

# Configuring
When creating an new email, postmaster looks in your Sublime User/Postmaster folder to find email templates.  These are used to create your new email
with its frontmatter and content:

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

| Name         | Type                       | Description                                                                                      |
|--------------|----------------------------|--------------------------------------------------------------------------------------------------|
| subject      | string                     | Email subject.                                                                                   |
| from         | string                     | Sender in the form `me@example.com` or `My Name <me@example.com>`.                               |
| to           | string or array of strings | Recipient in the form `to@example.com` or `Their Name <to@example.com>`.                         |
| cc           | string or array of strings | Carbon copy recipient in the form `to@example.com` or `Their Name <to@example.com>`.             |
| bcc          | string or array of strings | Blind carbon copy recipient in the form `to@example.com` or `Their Name <to@example.com>`.       |
| attachements | string or array of strings | Full file path for the attachment.                                                               |
| body         | string                     | Optional default body if desired.                                                                |
| smtp_server  | string                     | SMTP server used to send email.                                                                  |
| port         | int                        | SMTP server port used to send email.                                                             |
| tls          | bool                       | Should use tls via STARTTLS.                                                                     |
| user         | string                     | Optional user name for SMTP server. By default, your sender email will be used `me@example.com`. |

# Commands
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

# License
Licensed under MIT
Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
