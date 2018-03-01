from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    user_name = forms.CharField(label='用户名', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_password = forms.CharField(label='密码', max_length=20, min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', error_messages={"invalid": u"验证码错误"})
