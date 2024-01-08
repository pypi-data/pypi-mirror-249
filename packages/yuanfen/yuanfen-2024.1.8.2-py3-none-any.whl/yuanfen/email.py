import email
import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import chardet


class Email:
    def __init__(self, address, password, smtp_host, smtp_port, imap_host, imap_port, sender_name=None, timeout=10):
        self.address = address
        self.password = password
        self.smtp_server = smtp_host
        self.smtp_port = smtp_port
        self.imap_server = imap_host
        self.imap_port = imap_port
        self.sender_name = sender_name
        self.timeout = timeout

    def send_text(self, to, subject, text):
        msg = MIMEMultipart()
        msg["From"] = f"{self.sender_name or self.address} <{self.address}>"
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(text, "html", "utf-8"))

        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, timeout=self.timeout) as connection:
            connection.login(self.address, self.password)
            connection.sendmail(self.address, to, msg.as_string())

    def receive_emails(self, subject, count=1):
        emails = []
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port, timeout=self.timeout) as connection:
            connection.login(self.address, self.password)
            connection.select()

            _, [ids] = connection.search(None, "SUBJECT", subject.encode("utf-8"))
            email_ids = ids.split()[-count:]
            for msg_id in email_ids:
                _, msg_data = connection.fetch(msg_id, "(RFC822)")
                raw = email.message_from_bytes(msg_data[0][1])
                for part in raw.walk():
                    if part.get_content_type() == "text/html":
                        payload = part.get_payload(decode=True)
                        charset = chardet.detect(payload)["encoding"]
                        if charset == "GB2312":
                            charset = "GBK"
                        emails.append(payload.decode(charset))
        return emails
