#__author:"sfencs"
#date:2018/11/25
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
def Email(email_list,content,subject='article-release--用户注册'):
    msg = MIMEText(content,'plain','utf-8')
    msg['From']=formataddr(['article-release','article_release@163.com'])
    msg['To']=email_list[0]
    msg['Subject']=subject
    server=smtplib.SMTP('smtp.163.com',25)
    server.login('article_release@163.com','article259863')
    server.sendmail('article_release@163.com',email_list,msg.as_string())
    server.quit()