import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(transcript_id: str, app_password: str = GMAIL_APP_PASSWORD) -> None:
    with st.spinner("Sending email..."):
        # --- Configuration ---
        sender_email = "parisaparker2001@gmail.com"
        receiver_email = "parisaparker2001@gmail.com" 

        subject = "Test Email with Attachment"
        body = "Hi, here is the file you wanted."

        # --- Create the email ---
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Email body
        msg.attach(MIMEText(body, "plain"))

        # --- Attach a file ---
        file_path = Path(__file__).resolve().parents[1] / f'outputs/quizzes/{transcript_id}.pdf'  # change to your file path
        with open(file_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
            
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file_path)}")
        msg.attach(part)

        # --- Send via Gmail’s SMTP ---
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

    st.success("Email sent successfully!")