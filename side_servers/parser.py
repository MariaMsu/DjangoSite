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


def main():
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
            page_link = str(data)

            if page_link[0] == 'b':  # b'' reducing Y
                page_link = page_link[2:(len(page_link) - 1)]
            page_link = page_link.replace("https://vk.com", "https://m.vk.com")
            page_link = page_link + "?offset={}"
            posts = 0

            html_code = str(get_html(page_link.format(str(posts))))
            #print(1)
            posts_list = re.findall(r'wall\d{1,}_\d{1,}', html_code)

            while posts_list:
                posts += 1
                html_code = str(get_html(page_link.format(str(posts))))
                #print(2)
                posts_list = re.findall(r'wall\d{1,}_\d{1,}', html_code)

            logging.debug("Sent:" + str(posts))
            client_sock.sendall((str(posts)).encode())
            client_sock.close()
    except Exception:
        logging.error("КОЗЛЫ СКОРМИЛИ СЕРВЕРУ-ПАРСЕРY КАКУЮ-ТО ДРЯНЬ")


if __name__ == '__main__':
    main()
