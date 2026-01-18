import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email: str, subject: str, html_content: str):
    message = Mail(
        from_email=(
            os.getenv("EMAIL_FROM"),
            os.getenv("EMAIL_FROM_NAME")
        ),
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    sg = SendGridAPIClient(os.getenv("EMAIL_API_KEY"))
    response = sg.send(message)
    return response.status_code


    
