import socket
import ssl

client_cert = "client_certificate.pem"
client_key = "client_private.key"
ca_cert = "ca_certificate.pem"

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)
context.load_verify_locations(cafile=ca_cert)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(sock, server_hostname='localhost')
conn.connect(('localhost', 8443))

print("SSL handshake completed.")
conn.send(b"Hello from client!")
data = conn.recv(1024)
print(f"Received: {data.decode('utf-8')}")

conn.close()
