import socket
import ssl

server_cert = "server_certificate.pem"
server_key = "server_private.key"
ca_cert = "ca_certificate.pem"

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=ca_cert)
context.verify_mode = ssl.CERT_REQUIRED

bindsocket = socket.socket()
bindsocket.bind(('localhost', 8443))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    conn = context.wrap_socket(newsocket, server_side=True)
    print("SSL handshake completed.")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode('utf-8')}")
            conn.send(b"Hello from server!")
    finally:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
