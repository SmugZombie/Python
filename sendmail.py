#! /usr/bin/python
# sendmail.py - Utilizes Authenticated SMTP Relay to send mail
# Ron Egli - github.com/smugzombie
# Version 1.0

import smtplib
import argparse
import HTMLParser
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

arguments = argparse.ArgumentParser()
arguments.add_argument('--to','-t', help="Recipient of the email", required=True)
arguments.add_argument('--subject','-s', help="Subject of the email", required=True)
arguments.add_argument('--body','-b', help="Body of the email", required=True)
arguments.add_argument('--frm', '-f', help="From", required=True)
args = arguments.parse_args()

to = args.to
subject = args.subject
body = args.body
frm = args.frm

html_parser = HTMLParser.HTMLParser()
body = html_parser.unescape(body)

msg_from = frm + " <noreply@bouncerelay.com>"
msg_to = to

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

# Create the body of the message (a plain-text and an HTML version).
text = body
html = body

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)
# Send the message via local SMTP server.
# mail = smtplib.SMTP('smtp.gmail.com', 587)
mail = smtplib.SMTP('email-smtp.us-west-2.amazonaws.com', 587)

mail.ehlo()
mail.starttls()

mail.login('MAILUSER', 'MAILPASS')

response = {}

try:
        mail.sendmail(msg_from, msg_to, msg.as_string())
        mail.quit()
except smtplib.SMTPDataError as e:
#       print "SMTP Error: "+str(e)
        response['status'] = 0
        response['message'] = str(e)
except:
        e = sys.exc_info()[0]
        ressponse['status'] = 0
        response['message'] = "Unknown Error"
else:
        response['status'] = 1
        response['message'] = "Message Sent Succesfully!"

print json.dumps(response)
