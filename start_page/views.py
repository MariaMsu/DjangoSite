import hashlib
import random
import string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from .forms import Auth_form, Reg_form
from .models import User
from DjangoSite import settings


def login_exist(login):
    return bool(User.objects.filter(login=login))


def email_exist(email):
    return bool(User.objects.filter(email=email))


def add_new_user(login, password, email, token):
    hash_fun = hashlib.md5()
    hash_fun.update(password.encode())
    hash_password = hash_fun.digest()
    user = User.objects.create(login=login, password=hash_password, email=email, token=token)
    user.save()


def create_secret_key(size=16, chars=string.ascii_letters + string.digits):
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


def verification_link(login, token):
    return settings.DOMAIN_NAME + "verification/?login=" + login + "&token=" + token


def html_creation(user_verification_link):
    f = open('email.html', 'r')
    #TODO!!!!! здесь не работатет регистрация

    string_html = f.read()
    string_html = string_html.format(user_verification_link)
    print(string_html)
    return string_html


def send_confirm_email(user_email, user_login):
    subject, from_email, to = 'your account verification', settings.EMAIL_HOST_USER, user_email
    user_token = create_secret_key()
    user_verification_link = verification_link(user_login, user_token)
    text_content = user_verification_link
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_creation(user_verification_link), "text/html")
    print (html_creation(user_verification_link))
    msg.send()
    return user_token


def accordance_login_and_token(login, token):
    token_is_correct = False
    user = User.objects.filter(login=login)
    if user:
        if str(user[0].token) == token:
            user[0].token = 0
            user[0].save()
            token_is_correct = True
    return token_is_correct


def verify(request):
    if request.method == 'GET':
        login = request.GET['login']
        token = request.GET['token']
        if accordance_login_and_token(login, token):
            return render(request, "start_page/verification_is_successfully.html", {'status': True})
    return render(request, "start_page/verification_is_successfully.html", {'status': False})


def auth(request):
    if request.method == 'POST':
        form = Auth_form(request.POST)
        if form.is_valid():
            login = form.cleaned_data['user_login']
            password = form.cleaned_data['user_pass']
            if login_exist(login):
                if password_is_correct(login, password):
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
            user_token = send_confirm_email(email, login)
            add_new_user(login, password, email, user_token)
            return render(request, 'start_page/confirm_email.html')  # регистрация успешна
    else:
        form = Reg_form()

    return render(request, 'start_page/reg.html', {'form': form})
