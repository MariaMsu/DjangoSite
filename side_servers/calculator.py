import socket

PORT = 53211


def config():
    try:
        from DjangoSite import settings
        global PORT
        PORT = settings.CALCULATOR_PORT
        print("port successfully configured for:", PORT)
    except Exception:
        print("configuration failed, port set by default for:", PORT)


def sum(s):
    if s[0] == 'b':  # b'' reducing Y
        s = s[2:(len(s) - 1)]
    s += "+"  # Y just for lulz
    fulSum = 0
    lingth = len(s)
    i = 0
    separateDigit = "+"
    while i < lingth:
        if s[i] == '-':
            if (separateDigit != "+") and (separateDigit != "-"):
                fulSum += int(separateDigit)
            separateDigit = "-"
        elif s[i] == '+':
            if (separateDigit != "+") and (separateDigit != "-"):
                fulSum += int(separateDigit)
            separateDigit = "+"
        else:
            separateDigit += s[i]
        i += 1
    return fulSum


config()

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('127.0.0.1', PORT))
serv_sock.listen(10)

while serv_sock:
    client_sock, client_addr = serv_sock.accept()
    print('connected by ', client_addr)
    s = ""

    data = client_sock.recv(1024)
    print('Recived: ', data)
    s += str(data)

    s = sum(s)
    print("Sent:", s)

    client_sock.sendall(str(s).encode())
    client_sock.close()
