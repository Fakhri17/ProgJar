# Tugas 2 - FTP Socket Programming On python

### Nama  : Fakhri Alauddin | NIM : 1203220131

## Ringkasan

Program FTP Socket menggunakan Protokol TCP. Menggunakan bahasa python sebagai bahasa pemrogramannya.

### [Lihat Penjelasan](#Penjelasan) | [Lihat Penggunaan](#Penggunaan)


## Soal

buat sebuah program file transfer protocol menggunakan socket programming dengan beberapa perintah dari client seperti berikut.
- ls : ketika client menginputkan command tersebut, maka server akan memberikan daftar file dan folder. 
- rm {nama file} : ketika client menginputkan command tersebut, maka server akan menghapus file dengan acuan nama file yang diberikan pada parameter pertama.
- download {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan file dengan acuan nama file yang diberikan pada parameter pertama.
- upload {nama file} : ketika client menginputkan command tersebut, maka server akan menerima dan menyimpan file dengan acuan nama file yang diberikan pada parameter pertama.
- size {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan informasi file dalam satuan MB (Mega bytes) dengan acuan nama file yang diberikan pada parameter pertama.
- byebye : ketika client menginputkan command tersebut, maka hubungan socket client akan diputus.
- connme : ketika client menginputkan command tersebut, maka hubungan socket client akan terhubung.

## Penjelasan

**server.py**.

```py
import socket
import sys
import time
import os
import struct

print("\nSelamat datang di FTP SERVER.\n\nMenunggu koneksi dari client...\n\n")

TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()

print("\n Koneksi dengan alamat : {}".format(addr))

def upld():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    conn.send(b"1")
    file_size = struct.unpack("i", conn.recv(4))[0]
    start_time = time.time()
    print("Receiving file...")
    content = open(file_name, "wb")
    l = conn.recv(BUFFER_SIZE)
    while l:
        content.write(l)
        l = conn.recv(BUFFER_SIZE)
    content.close()
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    print("File received successfully")
    return


def list_files():
    print("Listing files...")
    listing = os.listdir(os.getcwd())
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    for i in listing:
        conn.send(struct.pack("i", sys.getsizeof(i)))
        conn.send(i.encode())
        conn.send(struct.pack("i", os.path.getsize(i)))
        total_directory_size += os.path.getsize(i)
        conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("i", total_directory_size))
    conn.recv(BUFFER_SIZE)
    print("Successfully sent file listing")
    return

def dwld():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        print("File name not valid")
        conn.send(struct.pack("i", -1))
        return
    conn.recv(BUFFER_SIZE)
    start_time = time.time()
    print("Sending file...")
    content = open(file_name, "rb")
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    print("File sent successfully")
    return

def delf():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", 1))
    else:
        conn.send(struct.pack("i", -1))
    confirm_delete = conn.recv(BUFFER_SIZE).decode()
    if confirm_delete == "Y":
        try:
            os.remove(file_name)
            conn.send(struct.pack("i", 1))
        except:
            print("Failed to delete {}".format(file_name))
            conn.send(struct.pack("i", -1))
    else:
        print("Delete abandoned by client!")
        return

def get_file_size():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        conn.send(struct.pack("i", -1))
    return


def quit():
    conn.send(b"1")
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)

while True:
    print("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE).decode()
    print("\nReceived instruction: {}".format(data))
    if data == "upload":
        upld()
    elif data == "ls":
        list_files()
    elif data == "download":
        dwld()
    elif data == "rm":
        delf()
    elif data == "size":
        get_file_size()
    elif data == "byebye":
        quit()
    data = None
```

**Output**.
```
Selamat datang di FTP SERVER.

Menunggu koneksi dari client...

```

**Analisis**.

*Inisialisasi:*.
Membuat socket menggunakan socket.socket(), mengikatnya ke alamat dan port tertentu dengan bind(), dan kemudian mendengarkan koneksi masuk dengan listen().
Ketika koneksi diterima, server menerima objek socket dan alamat dari klien yang terhubung menggunakan accept().

*Fungsi-fungsi:*
- upld(): Menerima file yang dikirim oleh klien, dengan mengirimkan dan menerima metadata file seperti nama dan ukuran file menggunakan struct.pack() dan struct.unpack(). Kemudian, file tersebut disimpan di server.
- list_files(): Mengirim daftar file yang ada di direktori kerja saat ini ke klien.
- dwld(): Mengirim file yang diminta oleh klien.
- delf(): Menghapus file yang diminta oleh klien.
- get_file_size(): Mengirim ukuran file yang diminta oleh klien.
- quit(): Menutup koneksi dan socket, dan kemudian me-restart skrip Python.

<br>

**client.py**

```py
import socket
import sys
import os
import struct
import time

TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connme():
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Koneksi berhasil!")
    except:
        print("Koneksi gagal! Pastikan server telah dijalankan dan port yang digunakan benar")

def upld(file_name):
    try:
        s.send(b"upload")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = os.path.getsize(file_name)
        s.send(struct.pack("i", file_size))
        start_time = time.time()
        print("Sending file...")
        content = open(file_name, "rb")
        l = content.read(BUFFER_SIZE)
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("f", time.time() - start_time))
        print("File sent successfully")
        return
    except:
        print("Error sending file")
        return

def list_files():
    try:
        s.send(b"ls")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        number_of_files = struct.unpack("i", s.recv(4))[0]
        for i in range(int(number_of_files)):
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            file_size = struct.unpack("i", s.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))
            s.send(b"1")
        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print("Total directory size: {}b".format(total_directory_size))
    except:
        print("Couldn't retrieve listing")
        return
    try:
        s.send(b"1")
        return
    except:
        print("Couldn't get final server confirmation")
        return

def dwld(file_name):
    try:
        s.send(b"download")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print("Error checking file")
    try:
        s.send(b"1")
        output_file = open(file_name, "wb")
        bytes_received = 0
        print("\nDownloading...")
        while bytes_received < file_size:
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_received += BUFFER_SIZE
        output_file.close()
        print("Successfully downloaded {}".format(file_name))
        s.send(b"1")
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except:
        print("Error downloading file")
        return
    return

def delf(file_name):
    try:
        s.send(b"rm")
        s.recv(BUFFER_SIZE)
    except:
        print("Couldn't connect to server. Make sure a connection has been established.")
        return
    try:
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
    except:
        print("Couldn't send file details")
        return
    try:
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == -1:
            print("The file does not exist on server")
            return
    except:
        print("Couldn't determine file existence")
        return
    try:
        confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
        while confirm_delete != "Y" and confirm_delete != "N" and confirm_delete != "YES" and confirm_delete != "NO":
            print("Command not recognized, try again")
            confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    except:
        print("Couldn't confirm deletion status")
        return
    try:
        if confirm_delete == "Y" or confirm_delete == "YES":
            s.send(b"Y")
            delete_status = struct.unpack("i", s.recv(4))[0]
            if delete_status == 1:
                print("File successfully deleted")
                return
            else:
                print("File failed to delete")
                return
        else:
            s.send(b"N")
            print("Delete abandoned by user!")
            return
    except:
        print("Couldn't delete file")
        return

def get_file_size(file_name):
    try:
        s.send(b"size")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print("File does not exist. Make sure the name was entered correctly")
            return
    except:
        print("Error checking file")
    try:
        s.send(b"1")
        print("File size: {} MB".format(file_size / 1024 / 1024))
        return
    except:
        print("Couldn't get final server confirmation")
        return

def quit():
    s.send(b"byebye")
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")
    return

print("Selamat datang dalam program FTP ( BASIC )\n")
print("INSTRUKSI :")
print("connme              : Connect to server ( jalankan ini dulu untuk lanjut perintah lain )")
print("upload <file_path>  : Upload file")
print("ls                  : List files")
print("download <file_path>: Download file")
print("rm <file_path>      : Delete file")
print("size <file_path>    : Get file size")
print("byebye              : Keluar program")


while True:
    prompt = input("\nEnter a command: ")
    if prompt[:6].lower() == "connme":
        connme()
    elif prompt[:6].lower() == "upload":
        upld(prompt[7:])
    elif prompt.lower() == "ls":
        list_files()
    elif prompt[:8].lower() == "download":
        dwld(prompt[9:])
    elif prompt[:2].lower() == "rm":
        delf(prompt[3:])
    elif prompt[:4].lower() == "size":
        get_file_size(prompt[5:])
    elif prompt.lower() == "byebye":
        quit()
        break
    else:
        print("Command not recognized; please try again")

```

**Output**.
```
Selamat datang dalam program FTP ( BASIC )

INSTRUKSI :
connme              : Connect to server ( jalankan ini dulu untuk lanjut perintah lain )
upload <file_path>  : Upload file
ls                  : List files
download <file_path>: Download file
rm <file_path>      : Delete file
size <file_path>    : Get file size
byebye              : Keluar program

Enter a command:
```

**Analisis**.

*Inisialisasi:*
Kode menginisialisasi koneksi ke server menggunakan socket.socket() dan mencoba untuk terhubung ke alamat dan port yang telah ditentukan.

*Fungsi-fungsi Utama:*
- connme(): Mencoba untuk terhubung ke server. Jika berhasil, mencetak pesan koneksi berhasil, jika tidak, mencetak pesan koneksi gagal.
- upld(file_name): Mengirim perintah "upload" ke server, kemudian mengirim metadata file seperti nama dan ukuran file, dan kemudian mengirim konten file tersebut dalam potongan-potongan yang disesuaikan dengan ukuran buffer. Setelah selesai mengirim, menerima konfirmasi dari server dan mencetak pesan keberhasilan atau kegagalan.
- list_files(): Mengirim perintah "ls" ke server untuk meminta daftar file yang ada di direktori server. Menerima respons dari server dan mencetak daftar file serta ukuran total direktori.
- dwld(file_name): Mengirim perintah "download" ke server, lalu mengirim metadata file yang diminta, menerima konten file dari server, dan menyimpannya ke dalam file lokal. Setelah selesai mengunduh, mencetak pesan keberhasilan atau kegagalan bersama dengan waktu yang dibutuhkan untuk unduhan.
- delf(file_name): Mengirim perintah "rm" ke server untuk menghapus file yang diminta. Meminta konfirmasi dari pengguna sebelum menghapus file. Menerima konfirmasi dari server dan mencetak pesan keberhasilan atau kegagalan.
- get_file_size(file_name): Mengirim perintah "size" ke server untuk meminta ukuran file yang diminta. Menerima respons dari server dan mencetak ukuran file dalam megabyte (MB).
- quit(): Mengirim perintah "byebye" ke server untuk mengakhiri koneksi, kemudian menutup socket.

## Penggunaan
Untuk menggunakan program ini harus menjalankan 2 file yaitu server.py dan client.py

```
> python server.py

Selamat datang di FTP SERVER.

Menunggu koneksi dari client...
```
```
> python client.py

Selamat datang dalam program FTP ( BASIC )

INSTRUKSI :
connme              : Connect to server ( jalankan ini dulu untuk lanjut perintah lain )
upload <file_path>  : Upload file
ls                  : List files
download <file_path>: Download file
rm <file_path>      : Delete file
size <file_path>    : Get file size
byebye              : Keluar program

Enter a command:
```

### Perintah

**connme**

``` 
Enter a command: connme
```
Digunakan untuk melakukan koneksi antara server dan client yang nantinya digunakan untuk berkomunikasi.

> Penting untuk menjalankan perintah ini terlebih dahulu karena jika tidak maka akan muncul error `Couldn't make server request. Make sure a connection has been established. `


**upload**
``` 
Enter a command: upload <file_path>
```
Contoh file_path adalah ``C:\PraktikumKuliah\SEM-4\ProgJar\ftp\coba.txt`` digunakan untuk mengupload file. Jika sukses maka akan muncul
```
Sending file...
File sent successfully
```
