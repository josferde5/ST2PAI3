import socket
import ssl
import time
from threading import Thread, Lock
import sys
import config
import logging

c = config.Config()
config.set_logging_configuration(True)
i = 0


def tls13_client(is_test, tic):
    global i
    lock = Lock()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='certs/server.crt')
    context.load_cert_chain(keyfile='certs/client.key', certfile='certs/client.crt')
    context.set_ciphers("CHACHA20")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with context.wrap_socket(s, server_hostname='example.com') as ssock:
            ssock.connect(('127.0.0.1', c.port))
            logging.info('Client up and connected to login server')
            if is_test:
                username = c.username
                password = c.password
                message = c.message
            else:
                username = input('Enter username: ')
                password = input('Enter password: ')
                message = input('Enter a message: ')

            ssock.sendall(bytes(username + '#' + password + '#' + message, 'utf-8'))
            while True:
                data = ssock.recv(2048)
                if not data:
                    continue
                else:
                    received_info = str(data, 'utf-8')
                    logging.info(received_info)
                    break

    if is_test:
        with lock:
            i = i + 1
            if i == c.connections:
                tac = time.perf_counter()
                logging.debug(f"Time elapsed: {tac - tic} seconds")


if __name__ == '__main__':
    if len(sys.argv) > 1 and str(sys.argv[1]) == 'test':
        counter = 0
        timestamp_start = time.perf_counter()
        while counter < c.connections:
            p = Thread(target=tls13_client(True, timestamp_start))
            p.start()
            counter += 1
    else:
        tls13_client(False, None)
