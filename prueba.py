import socket
import ssl
import time

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile="C:/server.crt")
    context.load_cert_chain(keyfile="C:/client.key", certfile="C:/client.crt")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        with context.wrap_socket(s, server_hostname='localhost') as ssock:

            # print(ssock.getpeercert())

            ssock.connect(("127.0.0.1", 8443))
            print("CLIENT INFO: Client up and connected to login server.")
            ssock.sendall(bytes("prueba", 'utf-8'))
            time.sleep(3)
