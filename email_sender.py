'''
Author: Derry
Date: 2022-12-05 20:37:24
LastEditors: Derry
Email: drlv@mail.ustc.edu.cn
LastEditTime: 2022-12-06 17:39:28
Description: None
'''

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class EmailSender:
    """
    邮件发送模块
    """

    def __init__(self, msg_to='derrylv@qq.com', msg_from='derrylv@qq.com', pwd="lcbejwsmaajeheeh"):
        self.smtp = "smtp.qq.com"
        self.msg_to = msg_to
        self.msg_from = msg_from
        self.pwd = pwd

    def send(self, content, subject="程序出错啦 /(ㄒoㄒ)/~~", attachment=None):
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"] = self.msg_from
        msg["To"] = self.msg_to
        text = MIMEText(content, "html", "utf-8")
        msg.attach(text)
        if attachment:
            att = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment; filename="{}"'.format(
                attachment)
            msg.attach(att)
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.smtp)
            smtp.login(self.msg_from, self.pwd)
            smtp.sendmail(self.msg_from, self.msg_to, msg.as_string())
            print("Successfully sending email to", self.msg_to)
        except:
            print("Failed to send email to", self.msg_to)
        finally:
            smtp.quit()

if __name__ == "__main__":
    email_sender = EmailSender()
    email_sender.send("test", "test","test.docx")