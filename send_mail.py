from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from sys import argv


def send_mail(from_user, to_user, subject, body):
    msg = MIMEMultipart()
    msg['From'] = from_user
    msg['To'] = to_user
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('des.sce.il19@gmail.com', mail_password)
    server.sendmail(msg['From'], msg['to'], msg.as_string())
    server.quit()


if __name__ == '__main__':
    mail_password = os.environ.get('PASS_ONLY')
    try:
        send_mail('des.sce.il19@gmail.com', argv[1], argv[2], argv[3])
    except Exception as e:
        print(e)
