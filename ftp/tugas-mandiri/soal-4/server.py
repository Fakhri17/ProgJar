import socket
import threading

def handle_client(client_socket):
  # Handle client logic here
  # This function will be executed in a separate thread for each client

  # Example: Echo server
  while True:
    data = client_socket.recv(1024)
    if not data:
      break
    client_socket.send(data)

  client_socket.close()

def start_server():
  # Create a TCP socket
  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  # Bind the socket to a specific address and port
  server_address = ('localhost', 12345)
  server_socket.bind(server_address)

  # Listen for incoming connections
  server_socket.listen(5)
  print('Server listening on {}:{}'.format(*server_address))

  while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('New connection from {}:{}'.format(*client_address))

    # Start a new thread to handle the client
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

start_server()