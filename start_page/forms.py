from django import forms


class Auth_form(forms.Form):
    user_login = forms.CharField(max_length=30, label='login')
    user_pass = forms.CharField(max_length=30, label='pass', widget=forms.PasswordInput)


class Reg_form(forms.Form):
    user_login = forms.CharField(max_length=30, label='your login')
    user_pass = forms.CharField(max_length=30, label='your password', widget=forms.PasswordInput)
    user_pass_confirm = forms.CharField(max_length=30, label='confirm password', widget=forms.PasswordInput)
    user_email = forms.EmailField(label='your email')
