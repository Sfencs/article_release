from django.shortcuts import render,redirect,HttpResponse

from django.db.models import F
import json
import datetime
from article import models
from tools import email_send
from tools import forms
# Create your views here.



class baseResponse:
    def __init__(self):
        self.status=True
        self.error_message=None
        self.success_message=None

def main(request):
    if request.method=='GET':

        return render(request,'main.html')


def send_registe_identifying(request):

    if request.method=='GET':

        return redirect('/main/')
    elif request.method=='POST':
        ret = baseResponse()
        form=forms.send_email_form(request.POST)
        if form.is_valid():
            value_dict=form.clean()
            email=value_dict['registe_email']
            has_email=models.UserInfo.objects.filter(email=email).count()
            if has_email:
                ret.status = False
                ret.error_message='该邮箱已被注册'
            else:
                current_date = datetime.datetime.now()
                from tools import registe_code
                code=registe_code.random_code()
                count = models.SendMsg.objects.filter(email=email).count()
                if not count:
                    models.SendMsg.objects.create(code=code, email=email, ctime=current_date)
                    #发送邮件

                    email_send.Email([email,],code)

                else:
                    limit_time = current_date - datetime.timedelta(hours=1)
                    is_over_times = models.SendMsg.objects.filter(email=email, ctime__gt=limit_time, times__gt=9).count()
                    if is_over_times:
                        ret.status = False
                        ret.error_message = '已超最大次数(1小时后重试)'
                    else:
                        is_over_time=models.SendMsg.objects.filter(email=email,ctime__lt=limit_time).count()
                        if is_over_time:
                            models.SendMsg.objects.filter(email=email).update(times=0)

                        models.SendMsg.objects.filter(email=email).update(code=code,
                                                                          ctime=current_date,
                                                                          times=F('times') + 1)
                        #发送邮件

                        email_send.Email([email, ], code)
        else:
            ret.status=False
            ret.error_message=form.errors['registe_email'][0]


        return HttpResponse(json.dumps(ret.__dict__))


def registe(request):
    if request.method=='GET':
        return redirect('/main/')
    elif request.method=='POST':
        form=forms.registe_form(request.POST)
        ret=baseResponse()
        if form.is_valid():
            value_dict = form.clean()
            print(value_dict)
            current_date=datetime.datetime.now()
            limit = current_date - datetime.timedelta(minutes=2)
            is_valid_code = models.SendMsg.objects.filter(email=value_dict['registe_email'],
                                                          code=value_dict['registe_email_code'],
                                                          ctime__gt=limit).count()
            if not is_valid_code:
                ret.status = False
                ret.error_message='验证码错误或失效'
            else:
                has_exist_username=models.UserInfo.objects.filter(username=value_dict['registe_username']).count()
                if has_exist_username:
                    ret.status = False
                    ret.error_message = '用户名已经存在'
                else:
                    has_exist_email = models.UserInfo.objects.filter(email=value_dict['registe_email']).count()
                    if has_exist_email:
                        ret.status = False
                        ret.error_message='该邮箱已注册过'
                    else:
                        value_dict['ctime'] = current_date
                        value_dict.pop('registe_email_code')
                        user_dict={}
                        user_dict['username']=value_dict['registe_username']
                        user_dict['email'] = value_dict['registe_email']
                        user_dict['password'] = value_dict['registe_password']
                        user_dict['ctime'] = value_dict['ctime']
                        obj=models.UserInfo.objects.create(**user_dict)
                        models.SendMsg.objects.filter(email=value_dict['registe_email']).delete()
                        user_info_dict = {'nid': obj.nid, 'email': obj.email, 'username': obj.username}
                        request.session['is_login'] = True
                        request.session['user_info'] = user_info_dict

        else:
            ret.status = False
            error_msg = form.errors.as_json()
            error = json.loads(error_msg)

            key_list=error.keys()
            item=''
            for i in key_list:
                item=i

            message=error[item][0]['message']
            ret.error_message=message
        return HttpResponse(json.dumps(ret.__dict__))


