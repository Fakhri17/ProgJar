import socket
import time
import threading

def english_to_indonesian_color(english_color):
    color_mapping = {
        "red": "merah",
        "green": "hijau",
        "blue": "biru",
        "yellow": "kuning",
        "purple": "ungu",
        "orange": "oranye",
    }
    return color_mapping.get(english_color.lower(), "tidak dikenali")

server_ip = "127.0.0.1"  # Ganti dengan alamat IP server
server_port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



while True:
    try:
        def input_with_timeout(prompt ,timeout):
            print(prompt, flush=True)
            response = [None]  # Response will be stored here
            def input_thread():
                try:
                    response[0] = input()
                except:
                    pass

            thread = threading.Thread(target=input_thread)
            thread.start()
            thread.join(timeout)

            if thread.is_alive():
                print(f"\nAnda tidak menjawab selama {timeout} detik\n")
                print("jawab apapun untuk melanjutkan")
                thread.join()
                
                return None
            else:
                return response[0]
            
        client_socket.sendto("request_color".encode("utf-8"), (server_ip, server_port))
        color, server_address = client_socket.recvfrom(1024)
        color = color.decode("utf-8")
        print(f"Warna yang diterima: {color}")

        # Klien memiliki waktu 5 detik untuk merespons
        response = input_with_timeout("Apa warna dalam bahasa Indonesia? ", 5)

        indonesian_color = english_to_indonesian_color(color)
        if response is None:
            print("Waktu habis. Nilai feedback: 0")
        elif response.lower() == indonesian_color:
            print("Jawaban benar! Nilai feedback: 100")
        else:
            print("Jawaban salah. Nilai feedback: 0")

        print("\nTunggu 10 detik sebelum mengirim permintaan lagi.\n")
        time.sleep(10)  # Tunggu 10 detik sebelum mengirim permintaan lagi
    except KeyboardInterrupt:
        print("\nKlien berhenti.")
        break

client_socket.close()