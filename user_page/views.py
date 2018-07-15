import logging
import socket

from django.shortcuts import render, redirect
from .forms import User_form
from DjangoSite import settings
import start_page.models


def reply_correction(data):
    data = str(data)
    if data[0] == 'b':
        return data[2:len(data) - 1]
    else:
        return data


def index(request):
    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(filename="", format=log_format, level=logging.DEBUG)

    if "id" in request.session:
        id_cookie = request.session.get("id")
        users = start_page.models.User.objects.filter(user_id=id_cookie)
        if users:  # вошло
            form = User_form(request.GET)
            answer_list = []
            if form.is_valid():
                link = form.cleaned_data['link']
                expression = form.cleaned_data['expression']
                answer_list.append('received link:' + link)

                parse_result = "-1"

                try:
                    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client_sock.connect(('127.0.0.1', settings.PARSER_PORT))
                    client_sock.sendall(link.encode())
                    parse_result = reply_correction(client_sock.recv(1024))
                    client_sock.close()

                    answer_list.append('number of posts:' + parse_result)
                    logging.debug("server_parser_reply:" + str(parse_result))
                except Exception:
                    logging.error("Сервер 'parser' устал и прилёг отдохнуть")

                if parse_result != "-1":
                    expression += ('+' + parse_result)

                    try:
                        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client_sock.connect(('127.0.0.1', settings.CALCULATOR_PORT))
                        client_sock.sendall(expression.encode())
                        expression_result = reply_correction(client_sock.recv(1024))
                        client_sock.close()

                        answer_list.append('answer:' + expression_result)
                        logging.debug("expression:" + expression)
                        logging.debug("server_calculator_reply:" + expression_result)
                    except Exception:
                        logging.error("Сервер 'calculator' устал и прилёг отдохнуть")

                    return render(request, 'user_page/user_page.html', {'form': form, 'answer_list': answer_list})

                answer_list.append('link is invalid')
            return render(request, 'user_page/user_page.html', {'form': form, 'answer_list': answer_list})
    return redirect("/")
