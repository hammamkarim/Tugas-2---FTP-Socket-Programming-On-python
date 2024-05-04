# Program Klien
import socket

# Pengaturan Atribut
TCP_IP = "127.0.0.1"
TCP_PORT = 8080
BUFFER_SIZE = 2048

# Blok fungsi untuk menyimpan sintaks command
def send_command(command, client_socket):
    try:
        client_socket.send(command.encode())
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)
    except Exception as e:
        print("Terjadi kesalahan:", e)

# Fungsi connme, untuk menyambungkan koneksi sepeuhnya antara klien dengan server
def connme(client_socket):
    try:
        client_socket.connect((TCP_IP, TCP_PORT))
        print("\nKoneksi berhasil tersambung!")
    except Exception as e:
        print("Koneksi gagal!", e)

# Blok Fungsi upload, untuk klien mengupload file ke server
def upload_file(file_name, client_socket):
    try:
        client_socket.send(b"upload")
        client_socket.send(file_name.encode())
        with open(file_name, "rb") as file:
            data = file.read()
            client_socket.send(data)
        print(client_socket.recv(BUFFER_SIZE).decode())
    except Exception as e:
        print("Terjadi kesalahan saat mengunggah file:", e)

# Fungsi main
def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_connected = False

    while True:
        # Menu Perintah
        print("\nPerintah : ")
        print("1. connme - Buat koneksi sepenuhnya ke server")
        print("2. ls - Tampilkan daftar file")
        print("3. download [filePath] - Unduh file")
        print("4. upload [filePath] - Unggah file")
        print("5. rm [filePath] - Hapus file")
        print("6. size [filePath] - Lihat ukuran File")
        print("7. byebye - Keluar")

        command = input("Masukkan perintah : ")

        # Kondisi yang akan dijalankan jika klien menginputkan "byebye"
        if command == "byebye":
            break
        # Kondisi yang akan dijalankan jika klien menginputkan "connme
        elif command == "connme":
            connme(client_socket)
            is_connected = True 
        elif command.startswith("upload"):
            if not is_connected:
                print("\nKoneksi belum tersambung sepenuhnya. Silakan buat koneksi terlebih dahulu dengan perintah 'connme'.")
            else:
                file_name = command.split()[1]
                upload_file(file_name, client_socket)
        else:
            if not is_connected:
                print("\nKoneksi belum tersambung sepenuhnya. Silakan buat koneksi terlebih dahulu dengan perintah 'connme'.")
            else:
                send_command(command, client_socket)

    client_socket.close()

if __name__ == "__main__":
    main()
