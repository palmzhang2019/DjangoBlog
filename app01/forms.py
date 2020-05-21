from django import forms
from django.core.exceptions import ValidationError
from app01 import models


class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label="Username",
        error_messages={
            "max_length": "username cannot too long, max length: 16",
            "required": "username cannot be empty"
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"}
        )
    )

    password = forms.CharField(
        min_length=6,
        label='Password',
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True
        ),
        error_messages={
            "min_length": "passowrd cannot too short min length: 6",
            "required": "password cannot be empty"
        }
    )

    re_password = forms.CharField(
        min_length=6,
        label="Password Confirm",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True
        ),
        error_messages={
            "min_length": "passowrd confirm cannot too short min length: 6",
            "required": "password confirm cannot be empty"
        }
    )

    email = forms.EmailField(
        label="Email",
        widget=forms.widgets.EmailInput(
            attrs={"class":"form-control"}
        ),
        error_messages={
            "invalud":"E-mail format is incorrect",
            "required": "E-mail cannot be empty"
        }
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error("username", ValidationError("User existed"))
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = models.UserInfo.objects.filter(email=email)
        if is_exist:
            self.add_error("email", ValidationError("Email existed"))
        else:
            return  email

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("Two passwords are inconsistent"))
        else:
            return self.cleaned_data