import smtplib, os
from email.mime.text import MIMEText

def format_posts_for_email(posts):
    """
    Formats a list of posts (documents) into a single string for email body.

    Parameters:
    - posts: A list of documents where each document contains 'link' and 'content'.

    Returns:
    - A formatted string that can be used as the body of an email.
    """
    formatted_message = ""
    formatted_message = "<div style='direction: rtl; text-align: right;'>\n"

    for post in posts:
        formatted_message += f"קישור - {post['link']}<br>\n"
        formatted_message += f"{post['content']}<br>\n"
        formatted_message += "----------------<br>\n"

    formatted_message += "</div>\n"
    return formatted_message

def send_email(subject, body, sender, recipients):
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients.join(",")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, os.getenv("GOOGLE_APP_PASSWORD"))
        smtp_server.sendmail(from_addr=sender, to_addrs=recipients, msg=msg.as_string())
        print("Message sent")
