import hashlib
import random
import string

from django.db import models


class User(models.Model):
    login = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email = models.EmailField()
    token = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)


def login_exist(login):
    return bool(User.objects.filter(login=login))


def email_exist(email):
    return bool(User.objects.filter(email=email))


def token_is_null(login):
    return User.objects.get(login=login).token == "0"


def create_secret_key(size=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_id(login):  # login must exist
    return User.objects.get(login=login).user_id


def add_new_user(login, password, email, token):
    hash_fun = hashlib.md5()
    hash_fun.update(password.encode())
    hash_password = hash_fun.digest()
    user_id = login + create_secret_key()
    user = User.objects.create(login=login, password=hash_password, email=email, token=token, user_id=user_id)
    user.save()


def password_is_correct(login, password):
    model = User.objects.get(login=login)
    hash_fun = hashlib.md5()
    hash_fun.update(password.encode())
    hash_password = hash_fun.digest()
    return str(model.password) == str(hash_password)


def accordance_login_and_token(login, token):
    token_is_correct = False
    user = User.objects.filter(login=login)
    if user:
        if str(user[0].token) == token:
            user[0].token = 0
            user[0].save()
            token_is_correct = True
    return token_is_correct


def is_logged_in(request):
    if "id" in request.COOKIES:
        if User.objects.filter(user_id=request.COOKIES["id"]):
            return True
    return False
