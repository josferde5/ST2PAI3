import socket
import ssl
from threading import Thread
import sys
import config
import stdiomask
import logging

c = config.Config()

format = '[%(asctime)s] CLIENT - %(levelname)s : %(message)s'
logging.basicConfig(format=format, level=logging.INFO, filename='tls.log', datefmt='%d-%m-%y %H:%M:%S')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(format, datefmt='%d-%m-%y %H:%M:%S'))
logging.getLogger().addHandler(handler)

def tls13_client(is_test):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='certs/server.crt')
    context.load_cert_chain(keyfile='certs/client.key', certfile='certs/client.crt')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with context.wrap_socket(s, server_hostname='example.com') as ssock:
            ssock.connect(('127.0.0.1', c.port))
            logging.info('Client up and connected to login server')
            if is_test:
                username = c.username
                password = c.password
            else:
                username = input('Enter username: ')
                password = stdiomask.getpass(prompt='Enter password: ')

            ssock.sendall(bytes(username + '#' + password, 'utf-8'))
            while True:
                data = ssock.recv(2048)
                if not data:
                    continue
                else:
                    received_info = str(data, 'utf-8')
                    logging.info(received_info)
                    if received_info == 'Successful login!':
                        if is_test:
                            message = 'Test message'
                        else:
                            message = input('Enter a message: ')

                        ssock.sendall(bytes(message, 'utf-8'))
                        continue
                    elif received_info == 'Message received successfully':
                        break
                    else:
                        username = input('Enter username: ')
                        password = stdiomask.getpass(prompt='Enter password: ')
                        ssock.sendall(bytes(username + '#' + password, 'utf-8'))
                        continue


if __name__ == '__main__':
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'Test':
        counter = 0
        while counter < c.connections:
            p = Thread(target=tls13_client(True))
            p.start()
            counter += 1
    else:
        tls13_client(False)


