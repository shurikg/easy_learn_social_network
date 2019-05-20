from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from sys import argv

mail_password = os.environ.get('PASS_ONLY')


def send_mail(from_user, to_user, subject, body, cc=None):
    msg = MIMEMultipart()
    msg['From'] = from_user
    msg['To'] = to_user
    msg['Subject'] = subject
    rcpt = to_user
    if cc:
        msg['Cc'] = cc
        rcpt = [to_user] + cc.split(',')
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('des.sce.il19@gmail.com', mail_password)
    server.sendmail(msg['From'], rcpt, msg.as_string())
    server.quit()


if __name__ == '__main__':
    try:
        arg_to = 'jonbir2@gmail.com'
        arg_cc = 'shlomitofahi@gmail.com,mayhagbi@gmail.com,elishalmon111@gmail.com'
        arg_subject = argv[1]
        arg_body = argv[2]
        send_mail('des.sce.il19@gmail.com', arg_to, arg_subject, arg_body, arg_cc)
    except Exception as e:
        print(e)
