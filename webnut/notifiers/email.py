import smtplib
from email.mime.text import MIMEText
from .notifier import NotificationBuilder

class EmailBuilder(NotificationBuilder):
    def __init__(self, smtp_server, smtp_port, sender_email, receiver_email, password, protocol='ssl'):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password
        self.message = None
        self.protocol = protocol

    def is_valid(self):
        return self.smtp_server and self.smtp_port and self.sender_email and self.receiver_email and self.password

    def set_message(self, message):
        self.message = message

    def send(self):
        if self.message:
            try:
                msg = MIMEText(self.message)
                msg['Subject'] = "UPS Notification"
                msg['From'] = self.sender_email
                msg['To'] = self.receiver_email

                if self.protocol.lower() == 'ssl':
                    with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                        server.login(self.sender_email, self.password)
                        server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
                elif self.protocol.lower() == 'tls':
                    with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                        server.starttls()
                        server.login(self.sender_email, self.password)
                        server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
                else:
                    raise ValueError("Invalid protocol specified. Use 'ssl' or 'tls'.")
                print("Email notification sent successfully")
            except Exception as e:
                print(f"Failed to send email notification: {e}")

