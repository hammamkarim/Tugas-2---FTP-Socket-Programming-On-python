# Tugas-2-FTP-Socket-Programming-On-python

Nama : Hammam Jauharul Karim

NIM : 1203222050

Kelas : IF-02-01

## Code Program

### Server

````
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
````

### Client

````
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
````

## Penjelasan Code Program

### Code Server
![1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/4c79d454-e5e3-4c96-9efd-4804a4fe5a19)

- Import Library : Penggalan kode tersebut untuk mengimpor dua modul Python, yaitu socket dan os.
    - socket digunakan untuk membuat dan mengelola koneksi jaringan.
    - os digunakan untuk berinteraksi dengan sistem operasi, seperti operasi file dan direktori.

![2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/ea89b4d4-b42a-4d3a-88f9-f74b31f6154f)

- TCP_IP: Variabel ini menentukan alamat IP yang akan digunakan oleh server. Nilainya adalah "127.0.0.1".
- TCP_PORT: Variabel ini menentukan nomor port yang akan digunakan oleh server. Dalam hal ini, port yang dipilih adalah 8080.
- BUFFER_SIZE: Variabel ini menentukan ukuran buffer untuk menerima dan mengirim data antara server dan klien. Dalam kasus ini, ukuran buffer adalah 2048 byte

![3](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/436ff838-501f-450c-b07b-5b56fd4d7c43)

- Definisi Fungsi: def handle_client_connection(client_socket): adalah deklarasi fungsi yang mengambil client_socket sebagai argumen. client_socket adalah objek socket yang mewakili koneksi antara server dan klien.
- Loop Tanpa Batas: while True: merupakan loop tanpa batas yang berjalan selama koneksi dengan klien aktif.
- Menerima Perintah dari Klien: command = client_socket.recv(BUFFER_SIZE).decode() digunakan untuk menerima data (perintah) dari klien. Data yang diterima diubah menjadi string menggunakan decode().
  
- Pemeriksaan Perintah: Setelah menerima perintah, dilakukan pemeriksaan untuk menentukan tindakan yang akan diambil.
    - Jika perintah kosong (tidak ada data yang diterima), loop akan dihentikan dengan break.
    - Jika perintah tidak kosong, perintah tersebut akan diproses.
    - Jika perintah adalah "ls", fungsi list_files akan dipanggil untuk menampilkan daftar file dan direktori.
    - Jika perintah dimulai dengan "download", fungsi send_file akan dipanggil untuk mengirim file kepada klien.
    - Jika perintah dimulai dengan "upload", fungsi receive_file akan dipanggil untuk menerima file dari klien.
    - Jika perintah dimulai dengan "rm", fungsi delete_file akan dipanggil untuk menghapus file.
    - Jika perintah dimulai dengan "size", fungsi get_file_size akan dipanggil untuk mendapatkan ukuran file.
    - Jika perintah tidak sesuai dengan opsi yang ada, server akan mengirim pesan kepada klien untuk memasukkan perintah yang valid.
      
- Menutup Koneksi: Setelah semua perintah selesai diproses, koneksi dengan klien ditutup menggunakan client_socket.close().

![4](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/e5de80b8-2ac4-4be2-9082-504365207457)

- Definisi Fungsi: def list_files(client_socket): adalah deklarasi fungsi yang mengambil client_socket sebagai argumen. client_socket adalah objek socket yang mewakili koneksi antara server dan klien.
- Menentukan Direktori Server: server_dir = os.path.dirname(__file__) digunakan untuk mendapatkan direktori tempat program server berjalan. __file__ adalah nama file skrip saat ini.
- Berubah ke Direktori Server: os.chdir(server_dir) digunakan untuk mengubah direktori kerja saat ini ke direktori tempat program server berjalan. Ini diperlukan agar kita dapat menggunakan fungsi os.listdir() untuk mendapatkan daftar file dan direktori di dalamnya.
- Membuat Daftar File dan Direktori: Melalui loop for, program mengiterasi melalui setiap file dan direktori di dalam server_dir. Untuk setiap item, nama file dan ukuran file diambil menggunakan os.path.getsize(). Informasi ini kemudian ditambahkan ke dalam daftar files_info.
- Format Daftar File: Daftar file dan direktori diubah menjadi string dengan menggunakan "\n".join(files_info), sehingga setiap item dipisahkan dengan baris baru.
- Mengirim Daftar ke Klien: String yang berisi daftar file dan direktori dikirim kepada klien menggunakan client_socket.send(files_list.encode()). Sebelumnya, string tersebut diubah menjadi byte dengan menggunakan encode().
- Pesan Informasi: Pesan "Mengirim daftar file ke klien." dicetak ke konsol untuk memberi tahu bahwa daftar file telah berhasil dikirim ke klien.

![5](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/8f2599e6-b918-423c-a006-3be6793bef7e)

- Definisi Fungsi: def send_file(client_socket, file_name): adalah deklarasi fungsi yang mengambil dua argumen, yaitu client_socket (objek socket yang mewakili koneksi antara server dan klien) dan file_name (nama file yang akan dikirim).
- Pemeriksaan Ketersediaan File: if os.path.exists(file_name) and os.path.isfile(file_name): digunakan untuk memeriksa apakah file yang diminta oleh klien tersedia di server dan apakah itu merupakan sebuah file (bukan direktori).
- Mengirim Informasi File: Jika file tersebut tersedia, ukuran file dihitung menggunakan os.path.getsize(file_name) dan pesan yang berisi informasi nama file dan ukuran file dikirim kepada klien menggunakan client_socket.send("{}\t{}".format(file_name, format_size(file_size)).encode()). Pesan ini dikodekan ke dalam bentuk byte sebelum dikirim.
- Penanganan Jika File Tidak Ditemukan: Jika file tidak ditemukan di server, pesan "File tidak ditemukan" dikirim kepada klien menggunakan client_socket.send(b"File tidak ditemukan").

![6](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/41f9dd6e-83c3-4cdd-a09c-bdd95c7dccbb)

- Penerimaan Nama File: file_name = client_socket.recv(BUFFER_SIZE).decode() digunakan untuk menerima nama file yang dikirim oleh klien. Nama file ini di-decode dari byte menjadi string.
- Penanganan Nama File yang Sudah Ada: Jika file dengan nama yang sama sudah ada di server, maka nama file tersebut akan diubah agar tidak terjadi konflik. Hal ini dilakukan dengan menambahkan nomor urut pada nama file yang baru, hingga nama file yang unik ditemukan.
- Penerimaan Data File: Setelah nama file ditentukan, data file dikirim oleh klien dan diterima oleh server menggunakan client_socket.recv(BUFFER_SIZE).
- Penyimpanan Data ke File: Data file yang diterima disimpan di server dengan membuka file dengan mode "wb" (write binary) dan menulis data yang diterima ke dalamnya.
- Pengiriman Konfirmasi ke Klien: Setelah file selesai diunggah, server mengirim pesan "File berhasil diunggah" kepada klien menggunakan client_socket.send(b"File berhasil diunggah").
- Pengiriman Informasi File: Informasi mengenai nama file dan ukuran file dikirim kembali kepada klien sebagai konfirmasi. Pesan tersebut dikodekan ke dalam bentuk byte sebelum dikirim.

![7](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/5a1242e4-ebe8-4344-aa77-cac3f8bd640a)

- Pemeriksaan Ketersediaan File: if os.path.exists(file_name) and os.path.isfile(file_name): digunakan untuk memeriksa apakah file yang akan dihapus ada di server dan apakah itu merupakan sebuah file (bukan direktori).
- Penghapusan File: Jika file tersebut tersedia, fungsi os.remove(file_name) digunakan untuk menghapus file tersebut dari sistem operasi.
- Konfirmasi Kepada Klien: Setelah file dihapus, pesan "File berhasil dihapus" dikirim kepada klien menggunakan client_socket.send(b"File berhasil dihapus").
- Pesan Jika File Tidak Ditemukan: Jika file tidak ditemukan di server, pesan "File tidak ditemukan" dikirim kepada klien menggunakan client_socket.send(b"File tidak ditemukan").

![8](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/f61e5ace-bc6c-4b72-a8fa-d2e492be6212)

- Fungsi get_file_size: Fungsi ini bertanggung jawab untuk mengirim informasi tentang ukuran file kepada klien. Mari kita bahas bagian per bagian:a. Pemeriksaan Ketersediaan File: if os.path.exists(file_name) and os.path.isfile(file_name): digunakan untuk memeriksa apakah file yang diminta oleh klien ada di server dan apakah itu merupakan sebuah file (bukan direktori).b. Penghitungan Ukuran File: Jika file tersebut tersedia, file_size = os.path.getsize(file_name) digunakan untuk mengambil ukuran file. Kemudian, informasi tentang nama file dan ukuran file dikirim kepada klien dengan menggunakan client_socket.send("{}\t{}".format(file_name, format_size(file_size)).encode()). Ini mencakup nama file dan ukuran file dalam format yang sesuai.c. Pengiriman Ukuran File dalam Byte: Ukuran file dalam byte juga dikirim kepada klien dengan menggunakan client_socket.send(str(file_size).encode()). Ini dilakukan untuk memberikan ukuran file dalam bentuk bilangan bulat yang mudah diproses oleh klien jika diperlukan.d. Penanganan Jika File Tidak Ditemukan: Jika file tidak ditemukan di server, pesan "File tidak ditemukan" dikirim kepada klien menggunakan client_socket.send(b"File tidak ditemukan").
- Fungsi format_size: Fungsi ini menerima ukuran file dalam byte dan mengembalikan string yang memformat ukuran tersebut ke dalam format yang lebih mudah dibaca.a. Ukuran file dibagi-bagi menjadi kategori berdasarkan ukurannya (bytes, KB, atau MB).b. Jika ukuran file kurang dari 1024 byte, ukurannya ditampilkan langsung dalam byte.c. Jika ukuran file kurang dari 1024 * 1024 byte (1 MB), ukurannya ditampilkan dalam KB dengan dua desimal.d. Jika ukuran file sama atau lebih besar dari 1 MB, ukurannya ditampilkan dalam MB dengan dua desimal.

## Dokumentasi dan Penjelasan Command

### Command 'ls'



### Command 'rm'


### Command 'download'

  
### Command 'upload'


### Command 'size'


### Command 'byebye'

### Command 'connme'

# Modifikasi Tugas-2-FTP-Socket-Programming-On-python

