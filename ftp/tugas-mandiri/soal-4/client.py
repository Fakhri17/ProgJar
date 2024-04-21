import socket

# Server address and port
server_address = 'localhost'
server_port = 12345

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_address, server_port))

# Send data to the server
data = 'Hello, server! saya client 1'
client_socket.send(data.encode())

# Receive response from the server
response = client_socket.recv(1024).decode()
print('Response from server:', response)

# Close the connection
client_socket.close()