import logging
import socket

PORT = 53211


def config():
    try:
        from DjangoSite import settings
        global PORT
        PORT = settings.CALCULATOR_PORT
        logging.info("port successfully configured for: " + str(PORT))
    except Exception:
        logging.info("configuration failed, port set by default for: " + str(PORT))


def reply_correction(data):
    data = str(data)
    if data[0] == 'b':
        return data[2:len(data) - 1]
    else:
        return data


def sum(s):
    s += "+"  # Y just for lulz
    ful_sum = 0
    length = len(s)
    i = 0
    separate_digit = "+"
    while i < length:
        if s[i] == '-':
            if (separate_digit != "+") and (separate_digit != "-"):
                ful_sum += int(separate_digit)
            separate_digit = "-"
        elif s[i] == '+':
            if (separate_digit != "+") and (separate_digit != "-"):
                ful_sum += int(separate_digit)
            separate_digit = "+"
        else:
            separate_digit += s[i]
        i += 1
    return ful_sum


log_format = '%(levelname)s: %(message)s'
logging.basicConfig(filename="", format=log_format, level=logging.DEBUG)
config()

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', PORT))
serv_sock.listen(10)

while serv_sock:
    client_sock, client_addr = serv_sock.accept()
    logging.debug('connected by ' + str(client_addr))

    data = client_sock.recv(1024)
    logging.debug('Received: ' + str(data))
    s = sum(reply_correction(data))

    client_sock.sendall(str(s).encode())
    logging.debug("Sent:" + str(s))
    client_sock.close()
