import socket
#membuat objek socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#mengatur opsi socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, (1,5))


# mengirim pesan ke socket client
message = 'Hello, client!'
client_socket.sendto(message.encode())
