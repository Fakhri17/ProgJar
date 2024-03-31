import socket
import sys
import os
import struct

TCP_IP = "127.0.0.1"
TCP_PORT = 1456
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn():
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection successful")
    except:
        print("Connection unsuccessful. Make sure the server is online.")

def upld(file_name):
    try:
        s.send(b"UPLD")
    except:
        print("Couldn't make server request. Make sure a connection has been established.")
        return
    try:
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("i", os.path.getsize(file_name)))
    except:
        print("Error sending file details")
    try:
        content = open(file_name, "rb")
        l = content.read(BUFFER_SIZE)
        print("\nSending...")
        while l:
            s.send(l)
            l = content.read(BUFFER_SIZE)
        content.close()
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except:
        print("Error sending file")
        return
    return

def list_files():
    try:
        s.send(b"LIST")
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
        s.send(b"DWLD")
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
        s.send(b"DELF")
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

def quit():
    s.send(b"QUIT")
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")
    return

print("\n\nWelcome to the FTP client.\n\nCall one of the following functions:\nCONN           : Connect to server\nUPLD file_path : Upload file\nLIST           : List files\nDWLD file_path : Download file\nDELF file_path : Delete file\nQUIT           : Exit")

while True:
    prompt = input("\nEnter a command: ")
    if prompt[:4].upper() == "CONN":
        conn()
    elif prompt[:4].upper() == "UPLD":
        upld(prompt[5:])
    elif prompt[:4].upper() == "LIST":
        list_files()
    elif prompt[:4].upper() == "DWLD":
        dwld(prompt[5:])
    elif prompt[:4].upper() == "DELF":
        delf(prompt[5:])
    elif prompt[:4].upper() == "QUIT":
        quit()
        break
    else:
        print("Command not recognized; please try again")
