from django import forms


class User_form(forms.Form):
    link = forms.URLField(max_length=64, label='link to vk profile')
    expression = forms.CharField(max_length=64, label='any expression (only "+" and "-")')
