# Program Server

import socket
import os

# Fungsi untuk mengirim daftar file dan folder
def send_list(client_socket):
    files = os.listdir('.')
    file_str = '\n'.join(files)
    client_socket.send(file_str.encode())

# Fungsi untuk menghapus file
def remove_file(client_socket, filename):
    try:
        os.remove(filename)
        client_socket.send("File Berhasil Dihapus".encode())
    except FileNotFoundError:
        client_socket.send("File Tidak Ditemukan".encode())

# Fungsi untuk mengirim file
def send_file(client_socket, filename):
    try:
        with open(filename, 'rb') as file:
            data = file.read()
            client_socket.send(data)
    except FileNotFoundError:
        client_socket.send("File Tidak Ditemukan".encode())

# Fungsi untuk menerima file
def receive_file(client_socket, filename):
    with open(filename, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
    client_socket.send("File Berhasil Dibuat".encode())

# Fungsi untuk mengirim informasi ukuran file
def send_file_size(client_socket, filename):
    try:
        size = os.path.getsize(filename) / (1024 * 1024) 
        client_socket.send(f"{size:.2f} MB".encode())
    except FileNotFoundError:
        client_socket.send("File Tidak Ditemukan".encode())

# Fungsi untuk menangani koneksi baru
def handle_connection(client_socket, address):
    print(f"Koneksi Baru dari {address} telah Berhasil Tersambung")

    while True:
        command = client_socket.recv(1024).decode()

        if not command:
            break

        command_parts = command.split(' ')
        command_name = command_parts[0]

        if command_name == 'ls':
            send_list(client_socket)
        elif command_name == 'rm':
            filename = ' '.join(command_parts[1:])
            remove_file(client_socket, filename)
        elif command_name == 'download':
            filename = ' '.join(command_parts[1:])
            send_file(client_socket, filename)
        elif command_name == 'upload':
            filename = ' '.join(command_parts[1:])
            receive_file(client_socket, filename)
        elif command_name == 'size':
            filename = ' '.join(command_parts[1:])
            send_file_size(client_socket, filename)
        elif command_name == 'byebye':
            break

    print("Klien Keluar dari Koneksi")

# Fungsi utama server
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print("Menunggu Koneksi.....")

    while True:
        client_socket, address = server_socket.accept()
        handle_connection(client_socket, address)

    server_socket.close()

if __name__ == "__main__":
    main()
