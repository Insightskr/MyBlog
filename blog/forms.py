from django import forms
from .models import Victor
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    user_name = forms.CharField(label='用户名', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_password = forms.CharField(label='密码', max_length=256, min_length=6,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码', error_messages={"invalid": u"验证码错误"})


# 以用户类为基础创建注册类
class RegisterForm(forms.ModelForm):
    captcha = CaptchaField(label='验证码', error_messages={"invalid": u"验证码错误"})

    class Meta:
        model = Victor
        fields = ['user_name', 'user_password', 'user_email', 'sex']
        widgets = {
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        # 用于错误信息调用
        error_messages = {
            "user_name": {"unique": "用户名不能重复", },
            "user_email": {"unique": "邮箱不能重复", },
        }

    # 定义钩子，编写自定义的清洗内容和 自定义的返回信息
    def clean_user_email(self):
        user_email = self.cleaned_data['user_email']
        obj = Victor.objects.filter(user_email=user_email)

        if obj:
            # 抛出异常错误
            raise ValidationError('该邮箱已注册')
        return user_email
