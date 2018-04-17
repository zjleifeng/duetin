#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/10/28 10:00
# @Author  : eric
# @Site    :
# @File    : forms.py
# @Software: PyCharm

from django import forms
from django.contrib.auth import authenticate, login
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
import base64
from django.contrib.admin import widgets
from django.core.mail import send_mail
from django.utils.encoding import force_bytes


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,

        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': u"username",

            }
        ),
    )

    password = forms.CharField(
        required=True,

        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': u'password',
                'onfocus': "this.value = '';",
                'onblur': "if (this.value == '') {this.value = 'Password';}"
            }
        ),

    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'请输入正确的用户名和密码')
        else:
            cleaned_data = super(LoginForm, self).clean()


class ChangepwdForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u'原密码',
        error_messages={'required': u'请输入原始密码!'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"原密码",
            }
        ),
    )
    newpassword1 = forms.CharField(
        required=True,
        label=u'新密码',
        error_messages={'required': u'请输出新密码!'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'新密码',

            }
        ),
    )

    newpassword2 = forms.CharField(
        required=True,
        label=u'再次输入新密码',
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'确认新密码',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'所有项都必须填！')
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u'2次输入的密码不同！')
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class PasswordRestForm(forms.Form):
    # 错误信息
    error_messages = {
        'email_error': u"此用户不存在或者用户名与email不对应.",
    }

    # 错误信息 invalid 表示username不合法的错误信息,
    # required 表示没填的错误信息
    username = forms.CharField(
        required=True,

        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': '',
                'placeholder': u"用户名",
            }
        ),
    )

    email = forms.CharField(
        required=True,

        error_messages={'required': u'请输入邮箱'},
        widget=forms.EmailInput(
            attrs={
                'class': '',
                'placeholder': u'email',
            }
        ),

    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'所有都必须填')
        else:
            username = self.cleaned_data.get('username')
            email = self.cleaned_data.get('email')

            if username and email:
                try:
                    self.user = User.objects.get(
                        username=username, email=email, is_active=True
                    )
                except User.DoesNotExist:
                    raise forms.ValidationError(
                        self.error_messages["email_error"]
                    )

            return self.cleaned_data

    def save(self, from_email=None, request=None,
             token_generator=default_token_generator):
        email = self.cleaned_data['email']

        site_name = u'xmkt'
        domain = u'127.0.0.1:8000'
        uid = base64.urlsafe_b64encode(
            force_bytes(self.user.pk)
        ).rstrip(b'\n=')
        token = token_generator.make_token(self.user)
        protocol = 'http'

        title = u"重置 {} 的密码".format(site_name)
        message = "".join([
            u"你收到这封信是因为你请求重置你在网站 {} 上的账户密码\n\n".format(
                site_name
            ),
            u"请访问该页面并输入新密码:\n\n",
            "{}://{}/resetpassword/{}/{}/\n\n".format(
                protocol, domain, uid, token
            ),
            u"你的用户名，如果已经忘记的话:  {}\n\n".format(
                self.user.username
            ),
            u"感谢使用我们的站点!\n\n",
            u"{} 团队\n\n\n".format(site_name)
        ])

        try:
            send_mail(title, message, from_email, [self.user.email])
        except Exception as e:
            pass


class SetPasswordForm(forms.Form):
    newpassword1 = forms.CharField(
        required=True,
        label=u'新密码',
        error_messages={'required': u'请输入新密码!'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'新密码',
            }
        ),
    )

    newpassword2 = forms.CharField(
        required=True,
        label=u'再次输入新密码',
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u'确认新密码',
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'所有项都必须填！')
        elif self.cleaned_data['newpassword1'] <> self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u'2次输入的密码不同！')
        else:
            cleaned_data = super(SetPasswordForm, self).clean()
        return cleaned_data

