import smtplib
from email.mime.text import MIMEText
from email.header import Header
from test.ConfigSetup import Reader

#SendEmail类用来指定邮箱发送邮件
class SendEmail:
    def __init__(self):
        self.reader = Reader()
        self.EmailHost = self.reader.GetInfo("SendEmailInfo", "EmailHost")  # 设置smtp服务器
        self.EmailUser = self.reader.GetInfo("SendEmailInfo", "EmailUser")  # 发邮件地址
        self.EmailCode = self.reader.GetInfo("SendEmailInfo", "EmailCode")  # 第三方客户端登录需要的口令
        self.EmailTo = self.reader.GetInfo("GetEmailInfo", "EmailUser") # 收邮件地址

    def Send(self):
        message = MIMEText(self.reader.GetInfo("SendEmailInfo", "EmailText"), 'plain', 'utf-8')
        message['From'] = Header(self.EmailUser)
        message['To'] = Header(self.EmailTo)
        subject = self.reader.GetInfo("SendEmailInfo", "EmailTitle")
        message['Subject'] = Header(subject, 'utf-8')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.EmailHost, 25)  # 25 为 SMTP 端口号
            smtpObj.login( self.EmailUser, self.EmailCode)
            smtpObj.sendmail(self.EmailUser, self.EmailTo, message.as_string()) # 第二个参数可以改为list形式，sendmail会向list中所有的对象发送邮件
            print("邮件发送成功")
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
