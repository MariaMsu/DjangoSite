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
        print("port successfully configured for:", PORT)
    except Exception:
        print("configuration failed, port set by default for:", PORT)


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def main():
    config()
    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(filename="", format=log_format, level=logging.DEBUG)
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.bind(('127.0.0.1', PORT))
    serv_sock.listen(10)
    try:
        while serv_sock:
            client_sock, client_addr = serv_sock.accept()
            logging.debug('connected by ', client_addr)
            page_link = ""
            data = client_sock.recv(1024)
            logging.debug('Received: ', data)
            page_link += str(data)

            if page_link[0] == 'b':  # b'' reducing Y
                page_link = page_link[2:(len(page_link) - 1)]
            page_link = page_link.replace("https://vk.com", "https://m.vk.com")
            page_link = page_link + "?offset={}"
            posts = 0

            html_code = str(get_html(page_link.format(str(posts))))
            posts_list = re.findall(r'wall\d{1,}_\d{1,}', html_code)

            while posts_list:
                posts += 1

                html_code = str(get_html(page_link.format(str(posts))))
                posts_list = re.findall(r'wall\d{1,}_\d{1,}', html_code)

            logging.debug("Sent:", str(posts).encode())
            client_sock.sendall((str(posts)).encode())
            client_sock.close()
    except Exception:
        logging.error("КОЗЛЫ СКОРМИЛИ СЕРВЕРУ-ПАРСЕР КАКУЮ-ТО ДРЯНЬ")


if __name__ == '__main__':
    main()
