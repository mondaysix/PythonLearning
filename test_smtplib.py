import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
sender = "1293880978@qq.com"
sender_pass = "jfuerykopwjgfedj"
receiver = "1293880978@qq.com"

def mail():
    ret = True
    try:
        msg = MIMEText('填写邮件内容','plain','utf-8')
        msg['From'] = formataddr(["发件人昵称",sender])
        msg['To'] = formataddr(["收件人昵称",receiver])
        msg['Subject'] = "邮件主题-测试"
        server = smtplib.SMTP_SSL('smtp.qq.com',465)
        server.login(sender, sender_pass)
        server.sendmail(sender,[receiver,],msg.as_string())
        server.quit()
    except Exception as e:
        print(e)
        ret = False
    return ret

ret = mail()
if ret:
    print("send email success")
else :
    print("send email fail")
# from smtplib import SMTP_SSL
# from email.header import Header
# from email.mime.text import MIMEText
#
# mail_info = {
#     "from": "1293880978@qq.com",
#     "to": "1293880978@qq.com",
#     "hostname": "smtp.qq.com",
#     "username": "1293880978@qq.com",
#     "password": "jfuerykopwjgfedj",
#     "mail_subject": "test",
#     "mail_text": "hello, this is a test email, sended by py",
#     "mail_encoding": "utf-8"
# }
#
# if __name__ == '__main__':
#     # 这里使用SMTP_SSL就是默认使用465端口
#     smtp = SMTP_SSL(mail_info["hostname"])
#     smtp.set_debuglevel(1)
#
#     smtp.ehlo(mail_info["hostname"])
#     smtp.login(mail_info["username"], mail_info["password"])
#
#     msg = MIMEText(mail_info["mail_text"], "plain", mail_info["mail_encoding"])
#     msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
#     msg["from"] = mail_info["from"]
#     msg["to"] = mail_info["to"]
#
#     smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
#
#     smtp.quit()