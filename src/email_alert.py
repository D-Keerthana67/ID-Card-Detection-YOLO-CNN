import smtplib
from email.message import EmailMessage


class EmailAlert:
    def __init__(self, sender, password, receiver, smtp_server, smtp_port):
        self.sender = sender
        self.password = password
        self.receiver = receiver
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_warning(self, student_id, warning_number):
        message = EmailMessage()
        message["Subject"] = f"ID Card Compliance Warning {warning_number}"
        message["From"] = self.sender
        message["To"] = self.receiver
        message.set_content(
            f"Student ID: {student_id}\n"
            f"Warning number: {warning_number}\n\n"
            "The computer vision system detected a confirmed ID-card compliance violation."
        )
        with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=20) as server:
            server.starttls()
            server.login(self.sender, self.password)
            server.send_message(message)
