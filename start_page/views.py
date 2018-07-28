from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from .forms import Auth_form, Reg_form
from .models import *
from DjangoSite import settings


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
    try:
        f = open('email.html', 'r')
        string_html = f.read()
        string_html = string_html.format(user_verification_link, user_verification_link)
    except:
        settings.logging.info("email.html потерян в пути")
        string_html = "click here to confirm your email" + str(user_verification_link)
    return string_html


def send_confirm_email(user_email, user_login):
    subject, from_email, to = 'your account verification', settings.EMAIL_HOST_USER, user_email
    user_token = create_secret_key()
    user_verification_link = verification_link(user_login, user_token)
    text_content = user_verification_link
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_creation(user_verification_link), "text/html")
    msg.send()
    return user_token


def verify(request):
    if request.method == 'GET':
        login = request.GET['login']
        token = request.GET['token']
        if accordance_login_and_token(login, token):
            return render(request, "start_page/verification_is_successfully.html", {'status': True})
    return render(request, "start_page/verification_is_successfully.html", {'status': False})


def set_id_into_cookies(login):
    response = redirect("/user/")
    response.set_cookie("id", get_id(login), 60 * 60 * 24)
    return response


def auth(request):
    if is_logged_in(request):
        return redirect("/user/")
    if request.method == 'POST':
        form = Auth_form(request.POST)
        if form.is_valid():
            login = form.cleaned_data['user_login']
            password = form.cleaned_data['user_pass']
            if login_exist(login):
                if password_is_correct(login, password):
                    if token_is_null(login):
                        response = set_id_into_cookies(login)
                        return response
                    return render(request,
                                  'start_page/auth.html',
                                  {'form': form, 'errors': "your account doesn't seem to be activated"})
            return render(request,
                          'start_page/auth.html',
                          {'form': form, 'errors': 'password or login is invalid'})
    else:
        form = Auth_form()
    return render(request,
                  'start_page/auth.html',
                  {'form': form})


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
