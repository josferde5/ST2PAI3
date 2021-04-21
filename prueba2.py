import socket
import ssl

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_verify_locations(cafile="C:/client.crt")
    context.load_cert_chain(keyfile="C:/server.key", certfile="C:/server.crt")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 8443))
        s.listen(1)
        with context.wrap_socket(s, server_side=True) as ssock:
            connection, a = ssock.accept()
            print('SERVER INFO: Server up, waiting for a connection.')
            print('SERVER INFO: received connection from', connection.getpeercert())
            while True:
                data = connection.recv(2048)
                if not data:
                    continue
                received_info = str(data, 'utf-8')
                print("SERVER - Message received: " + received_info)
                break

