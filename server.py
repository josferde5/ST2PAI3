import socket
import ssl
import _thread
import config
import logging
import sys

c = config.Config()

format = '[%(asctime)s] SERVER - %(levelname)s : %(message)s'
logging.basicConfig(format=format, level=logging.INFO, filename='tls.log', datefmt='%d-%m-%y %H:%M:%S')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter(format, datefmt='%d-%m-%y %H:%M:%S'))
logging.getLogger().addHandler(handler)

def threaded_client(connection):
    while True:
        data = connection.recv(2048)
        if not data:
            continue
        received_info = str(data, 'utf-8')
        received_info_sp = received_info.split('#')

        if len(received_info_sp) == 3:
            if received_info_sp[0].strip() != c.username or received_info_sp[1].strip() != c.password:
                logging.info('The message has been discarded due to an error in the credentials')
                connection.sendall(bytes('The message has been discarded due to an error in the credentials', 'utf-8'))
            else:
                logging.info('{Username: ' + received_info_sp[0].strip() + ', Message: ' + received_info_sp[2].strip() + '}')
                connection.sendall(bytes('Message saved successfully', 'utf-8'))
        else:
            logging.info('The message has been discarded due to an error in the format')
            connection.sendall(bytes('The message has been discarded due to an error in the format', 'utf-8'))



def tls13_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_verify_locations(cafile='certs/client.crt')
    context.load_cert_chain(keyfile='certs/server.key', certfile='certs/server.crt')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', c.port))
        s.listen()
        logging.info('Server up, waiting for a connection')
        with context.wrap_socket(s, server_side=True) as ssock:
            while True:
                connection, a = ssock.accept()
                logging.info('Received connection from ' + str(a))
                _thread.start_new_thread(threaded_client, (connection,))


if __name__ == '__main__':
    tls13_server()
