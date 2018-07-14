import hashlib
import random
import string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.shortcuts import render, redirect
from .forms import Auth_form, Reg_form
from .models import User
from DjangoSite import settings


def login_exist(login):
    return bool(User.objects.filter(login=login))


def email_exist(email):
    return bool(User.objects.filter(email=email))


def add_new_user(login, password, email):
    hash_fun = hashlib.md5()
    hash_fun.update(password.encode())
    hash_password = hash_fun.digest()
    user = User.objects.create(login=login, password=hash_password, email=email)
    user.save()


def create_secret_key(size=8, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def password_is_correct(login, password):
    model = User.objects.get(login=login)
    hash_fun = hashlib.md5()
    hash_fun.update(password.encode())
    hash_password = hash_fun.digest()
    return str(model.password) == str(hash_password)


def check_errors(login, password, password_confirm, email):
    errors = []
    if login_exist(login):
        errors.append('this login is already exist')
    if password != password_confirm:
        errors.append('password confirmation failed')
    if email_exist(email):
        errors.append('this email is already taken')
    return errors


def auth(request):
    if request.method == 'POST':
        form = Auth_form(request.POST)
        if form.is_valid():
            login = form.cleaned_data['user_login']
            password = form.cleaned_data['user_pass']
            if login_exist(login):
                if password_is_correct(login, password):
                    #print('вход выполнен')
                    return redirect('/user/')
            return render(request, 'start_page/auth.html', {'form': form, 'errors': 'password or login is invalid'})
    else:
        form = Auth_form()

    return render(request, 'start_page/auth.html', {'form': form})


def reg(request):
    if request.method == 'POST':
        form = Reg_form(request.POST)
        if form.is_valid():
            login = form.cleaned_data['user_login']
            password = form.cleaned_data['user_pass']
            password_confirm = form.cleaned_data['user_pass_confirm']
            email = form.cleaned_data['user_email']
            errors_list = check_errors(login, password, password_confirm, email)
            if errors_list:
                return render(request, 'start_page/reg.html', {'form': form, 'errors_list': errors_list})

            #  send_mail("your account verification", "test", settings.EMAIL_HOST_USER, ["dovvakkin@gmail.com"], [("static/justlikemaria.jpg", img_data, "image/jpg")])

            subject, from_email, to = 'your account verification', settings.EMAIL_HOST_USER, 'dovvakkin@gmail.com'
            text_content = 'This is an important message.'
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_file("start_page/image/justlikemaria.jpg")
            msg.send()


            #TODO
            add_new_user(login, password, email)
            return render(request, 'start_page/reg.html', {'form': form})  # регистрация успешна
    else:
        form = Reg_form()

    return render(request, 'start_page/reg.html', {'form': form})
