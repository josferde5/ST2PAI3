import socket
import ssl
from threading import Thread

import config

c = config.Config()


def tls13_client():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile="certs/server.crt")
    context.load_cert_chain(keyfile="certs/client.key", certfile="certs/client.crt")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with context.wrap_socket(s, server_hostname='example.com') as ssock:
            ssock.connect(("127.0.0.1", c.port))
            print("CLIENT INFO: Client up and connected to login server.")
            ssock.sendall(bytes("st2pai3, prueba, Mensajito", 'utf-8'))
            while True:
                data = ssock.recv(2048)
                if not data:
                    continue
                received_info = str(data, 'utf-8')
                print("Received from server: " + received_info)
                break


if __name__ == "__main__":
    counter = 0
    while counter < 300:
        p = Thread(target=tls13_client)
        p.start()
        counter += 1




