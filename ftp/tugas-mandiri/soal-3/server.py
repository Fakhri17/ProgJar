import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server address and port
server_address = ('localhost', 12345)

# Bind the socket to the server address and port
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print('Server is running and listening for connections...')

while True:
  # Wait for a client to connect
  client_socket, client_address = server_socket.accept()
  print(f'Client connected: {client_address}')

  try:
    while True:
      # Receive data from the client
      data = client_socket.recv(1024).decode()

      if not data:
        # If no data received, client has disconnected
        print(f'Client disconnected: {client_address}')
        break

      # Process the received data
      # (You can add your own logic here)
      print(f'Received data from client {client_address}: {data}')

      # Send a response back to the client
      response = 'Server received your message: ' + data
      client_socket.sendall(response.encode())

  finally:
    # Close the client socket
    client_socket.close()

# Close the server socket
server_socket.close()