# Program server
import socket
import os

# Pengaturan Atribut
TCP_IP = "127.0.0.1"
TCP_PORT = 8080
BUFFER_SIZE = 2048

# Blok fungsi untuk menangani komunikasi dengan klien
def handle_client_connection(client_socket):
    while True:
        command = client_socket.recv(BUFFER_SIZE).decode()
        if not command:
            break
        else:
            print("\nMenerima perintah dari klien:", command)
            if command == "ls":
                list_files(client_socket)
            elif command.startswith("download"):
                file_name = command.split()[1]
                send_file(client_socket, file_name)
            elif command.startswith("upload"):
                receive_file(client_socket)
            elif command.startswith("rm"):
                file_name = command.split()[1]
                delete_file(client_socket, file_name)
            elif command.startswith("size"):
                file_name = command.split()[1]
                get_file_size(client_socket, file_name)
            else:
                client_socket.send(b"tolong masukkan inputan yang valid")
    client_socket.close()

# Blok fungsi ls, untuk mengirim list file dan direktori
def list_files(client_socket):
    server_dir = os.path.dirname(__file__)
    os.chdir(server_dir)
    files_info = []
    for file_name in os.listdir():
        file_path = os.path.join(server_dir, file_name)
        file_size = os.path.getsize(file_path)
        files_info.append(f"\n{file_name}\t{format_size(file_size)}")
    files_list = "\n".join(files_info)
    client_socket.send(files_list.encode())
    print("Mengirim daftar file ke klien.")

# Blok fungsi download, untuk klien mendownload file dari server
def send_file(client_socket, file_name):
    if os.path.exists(file_name) and os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        print("Mengirim file '{}' ({} ) ke klien.".format(file_name, format_size(file_size)))
        client_socket.send("{}\t{}".format(file_name, format_size(file_size)).encode())
    else:
        client_socket.send(b"File tidak ditemukan")

# Blok fungsi upload, untuk server menerima file dari klien
def receive_file(client_socket):
    file_name = client_socket.recv(BUFFER_SIZE).decode()
    original_file_name = file_name
    file_counter = 1
    while os.path.exists(file_name):
        file_name = "{}_{}".format(original_file_name, file_counter)
        file_counter += 1
    file_data = client_socket.recv(BUFFER_SIZE)
    with open(file_name, "wb") as file:
        file.write(file_data)
    client_socket.send(b"File berhasil diunggah")
    file_size = os.path.getsize(file_name)
    print("Menerima file '{}' ({}) dari klien.".format(file_name, format_size(file_size)))
    client_socket.send("{}\t{}".format(file_name, format_size(file_size)).encode())

# Blok fungsi rm, untuk hapus file
def delete_file(client_socket, file_name):
    if os.path.exists(file_name) and os.path.isfile(file_name):
        os.remove(file_name)
        client_socket.send(b"File berhasil dihapus")
        print("Menghapus file '{}'.".format(file_name))
    else:
        client_socket.send(b"File tidak ditemukan")

# Blok Fungsi size, untuk mendapatkan ukuran file
def get_file_size(client_socket, file_name):
    if os.path.exists(file_name) and os.path.isfile(file_name):
        file_size = os.path.getsize(file_name)
        client_socket.send("{}\t{}".format(file_name, format_size(file_size)).encode())
        client_socket.send(str(file_size).encode()) 
        print("Mengirim ukuran file '{}' ({}) ke klien.".format(file_name, format_size(file_size)))
    else:
        client_socket.send(b"File tidak ditemukan")

# Blok fungsi rumus size
def format_size(size):
    if size < 1024:
        return "{} bytes".format(size)
    elif size < 1024 * 1024:
        return "{:.2f} KB".format(size / 1024)
    else:
        return "{:.2f} MB".format(size / (1024 * 1024))

# Fungsi main
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((TCP_IP, TCP_PORT))
    server_socket.listen(5)

    print("\nFTP Server is listening on {} : {}".format(TCP_IP, TCP_PORT))

    while True:
        client_socket, address = server_socket.accept()
        print("Menerima koneksi dari {} : {}".format(address[0], address[1]))
        handle_client_connection(client_socket)

if __name__ == "__main__":
    main()
