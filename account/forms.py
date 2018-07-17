from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

from .models import Account

class AccountForm(forms.ModelForm):
    password = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, label=u"密码*")
    password2 = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, label=u"再次输入密码*")
    phone     = forms.CharField(max_length=128, min_length=11, label=u"手机号*")
    email = forms.EmailField(label="邮箱(稍后进行激活验证)")
    birth = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}), label=u"出生日期*")
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'}, output_format=u'%(text_field)s %(image)s %(hidden_field)s')
    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError(u"两次密码必须一致")

    class Meta:
        model = Account
        db_table = 'AccountForm'
        fields = ("name", "phone", "password", "password2", "email", "sex", "picture", "birth", "personalized_signature")

class AccountModifyForm(forms.ModelForm):

    class Meta:
        model = Account
        db_table = 'AccountModifyForm'
        fields = ("id", "name", "phone", "email", "sex", "birth", "personalized_signature")

class LoginForm(forms.ModelForm):
    password = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, label=u"密码*")
    class Meta:
        model = Account
        fields = ("phone", "password")

class LoginwithcaptchaForm(forms.ModelForm):
    password = forms.CharField(max_length=128, min_length=8, widget=forms.PasswordInput, label=u"密码*")
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'},
                           output_format=u'%(text_field)s %(image)s %(hidden_field)s')
    class Meta:
        model = Account
        fields = ("phone", "password")

class ForgetForm(forms.Form):
    email=forms.EmailField(required=True)
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'}, output_format=u'%(text_field)s %(image)s %(hidden_field)s')
 
#reset.html中，用于验证新设的密码长度是否达标
class ResetForm(forms.Form):
    newpwd1=forms.CharField(required=True,min_length=8,error_messages={'required': '密码不能为空.', 'min_length': "至少8位"})
    newpwd2 = forms.CharField(required=True, min_length=8, error_messages={'required': '密码不能为空.', 'min_length': "至少8位"})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "last_name", "first_name", "password")

