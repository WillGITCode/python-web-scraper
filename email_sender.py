import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import gmail_sender
from config import email_reciever

def send_email(subject, body):
    email_text = MIMEMultipart()
    email_text['From'] = gmail_sender["user_name"]
    email_text['To'] = email_reciever["user_name"]
    email_text['Subject'] = subject
    email_text.attach(MIMEText(body))
    
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_sender["user_name"], gmail_sender["password"])
        smtp_server.sendmail(gmail_sender["user_name"], email_reciever["user_name"], email_text.as_string())
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)