import os
from email.message import EmailMessage
# Add security
import ssl
import smtplib

email_sender = "weeqichew0316@gmail.com"
email_password = "wogwjgkvzgliubck"
email_reciver = "weeqichew0316@gmail.com"


subject = "Check out my new video"
body = "chewlucy987@gmail.com"

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_reciver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_reciver, em.as_string())