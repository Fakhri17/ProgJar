import socket

# Inisialisasi socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Menghubungkan ke server
server_address = ('localhost', 5000)
sock.connect(server_address)

while True:
  # Meminta input dari pengguna
  operation = input('Masukkan operasi matematika (contoh: 1 + 1): ')

  # Memastikan input memiliki format yang benar
  if not operation:
    print("Input tidak boleh kosong.")
    continue

  # Mengirim pesan ke server
  sock.send(operation.encode())

  # Menerima pesan balasan dari server
  response = sock.recv(1024).decode()
  print('Hasil perhitungan:', response)

  # Memeriksa apakah pengguna ingin melanjutkan atau tidak
  choice = input('Lanjutkan? (y/n): ')
  if choice.lower() != 'y':
    break

# Menutup koneksi dengan server
sock.close()
