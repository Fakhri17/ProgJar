import socket

# Server IP address and port
server_ip = '127.0.0.1'
server_port = 12345

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Continuously send messages
while True:
  message = input("Enter a message: ")

  # Send the message to the server
  client_socket.sendto(message.encode(), (server_ip, server_port))

  # Receive the response from the server
  response, server_address = client_socket.recvfrom(1024)
  print("Response from server:", response.decode())

# Close the socket
client_socket.close()