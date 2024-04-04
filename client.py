# Program Client

import socket

# Fungsi utama client
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 9999))
    
    while True:
        command = input("Masukkan Perintah : ")
        client_socket.send(command.encode())

        if command == 'byebye':
            break
        elif command == 'connme':
            client_socket.close()  # Menutup koneksi saat ini
            print("Koneksi Ditutup")
            # Membuat koneksi baru ke server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', 9999))
            print("Koneksi Baru Tersambung")
        elif command.startswith('upload'):
            # Menerima respons dari server
            response = client_socket.recv(1024).decode()  
            print(response)
        else:
            response = client_socket.recv(1024).decode()
            print(response)

    client_socket.close()

if __name__ == "__main__":
    main()
