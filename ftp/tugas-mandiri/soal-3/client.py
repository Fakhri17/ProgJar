import socket

# Server address and port
server_address = ('localhost', 12345)

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect(server_address)

while True:
  # Get user input
  message = input("Enter a message: ")

  # Send the message to the server
  client_socket.sendall(message.encode())

  # Receive response from the server
  response = client_socket.recv(1024).decode()

  # Print the response
  print("Server response:", response)

# Close the socket
client_socket.close()