import logging
import urllib.request
import socket
import re

PORT = 53210


def config():
    try:
        from DjangoSite import settings
        global PORT
        PORT = settings.PARSER_PORT
        logging.info("port successfully configured for: " + str(PORT))
    except Exception:
        logging.info("configuration failed, port set by default for: " + str(PORT))


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def reply_correction(data):
    data = str(data)
    if data[0] == 'b':
        return data[2:len(data) - 1]
    else:
        return data


def address_correction(link):
    if link.startswith("https"):
        return link
    else:
        return "https://" + link


def posts(link, iterator):
    link = link + "?offset={}"
    html_code = str(get_html(link.format(str(iterator))))
    return re.findall(r'wall\d{1,}_\d{1,}', html_code)


def parser_itself(link):
    link = link.replace("https://vk.com", "https://m.vk.com")
    posts_iterator = 0
    while posts(link, posts_iterator):
        posts_iterator += 1
    return posts_iterator



log_format = '%(levelname)s: %(message)s'
logging.basicConfig(filename="", format=log_format, level=logging.DEBUG)
config()
log_format = '%(levelname)s: %(message)s'
logging.basicConfig(filename="", format=log_format, level=logging.DEBUG)
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', PORT))
serv_sock.listen(10)
try:
    while serv_sock:
        client_sock, client_addr = serv_sock.accept()
        logging.debug('connected by ' + str(client_addr))
        data = client_sock.recv(1024)
        logging.debug('Received: ' + str(data))

        page_link = address_correction(reply_correction(data))

        posts_amount = parser_itself(page_link)

        logging.debug("Sent:" + str(posts_amount))
        client_sock.sendall((str(posts_amount)).encode())
        client_sock.close()
except Exception:
    logging.error("КОЗЛЫ СКОРМИЛИ СЕРВЕРУ-ПАРСЕРY КАКУЮ-ТО ДРЯНЬ")



