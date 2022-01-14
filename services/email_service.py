import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:

    def __init__(self, config):
        self.config = config

    def format_email_subject(self, keywords):
        return ", ".join(keywords)

    def format_email_paragraph(self, article):
        return """\
            Article Title: %s
            Article URL: %s
            Article Keywoards: %s
            Article NLP summary: %s
            """ % (article.title, article.url, self.format_email_subject(article.keywords), article.summary)
    
    def format_email_body(self, articles):
        return """\
            Article Title: %s
            Article URL: %s
            Article NLP summary: %s
            """ % (article.title, article.url, article.summary)

    def send_email(self, subject, body):
        email_text = MIMEMultipart()
        email_text['From'] = self.config.gmail_sender["user_name"]
        email_text['To'] = self.config.email_reciever["user_name"]
        email_text['Subject'] = subject
        email_text.attach(MIMEText(body))
        
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(self.config.gmail_sender["user_name"], self.config.gmail_sender["password"])
            smtp_server.sendmail(self.config.gmail_sender["user_name"], self.config.email_reciever["user_name"], email_text.as_string())
            smtp_server.close()
            print ("Email sent successfully!")
        except Exception as ex:
            print ("Something went wrong….",ex)