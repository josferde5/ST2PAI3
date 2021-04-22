import socket
import ssl
import time

username = "st2pai3"
passwd = "prueba"

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_verify_locations(cafile="C:/client.crt")
    context.load_cert_chain(keyfile="C:/server.key", certfile="C:/server.crt")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 8443))
        s.listen(1)
        with context.wrap_socket(s, server_side=True) as ssock:
            print('SERVER INFO: Server up, waiting for a connection.')
            connection, a = ssock.accept()
            print('SERVER INFO: received connection from', a)
            while True:
                data = connection.recv(2048)
                if not data:
                    continue
                received_info = str(data, 'utf-8')
                print("SERVER - Message received: " + received_info)
                received_info_sp = received_info.split(",")
                if len(received_info_sp) < 2:
                    connection.sendall(bytes("Username and password required", "utf-8"))
                if received_info_sp[0].strip() != username or received_info_sp[1].strip() != passwd:
                    connection.sendall(bytes("Bad credentials: username or password incorrect", "utf-8"))
                else:
                    connection.sendall(bytes("Message received successfully", "utf-8"))
                time.sleep(1)
                break


