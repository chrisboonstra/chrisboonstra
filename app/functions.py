import streamlit as st
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import yaml
import os

def is_valid_email(email):
  email_pattern = r"'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z0-9.]+$"
  return re.match(email_pattern, email) is not None

def send_email(subject, text, html, sender, recipients, password):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    msg.attach(part1)
    msg.attach(part2)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def load_repositories(repo_file):
    if os.path.exists(repo_file):
        with open(repo_file, "r") as f:
            return yaml.safe_load(f) or []

