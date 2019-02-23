#__author:"sfencs"
#date:2018/11/25
from django import forms


class send_email_form(forms.Form):
    registe_email=forms.EmailField()

class registe_form(forms.Form):
    registe_username = forms.CharField()
    registe_email = forms.EmailField()
    registe_password = forms.CharField()
    registe_email_code = forms.CharField()
class login_form(forms.Form):
    login_username_or_email=forms.CharField()
    login_password = forms.CharField()