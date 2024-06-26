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

### Server
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

- Fungsi get_file_size: Fungsi ini bertanggung jawab untuk mengirim informasi tentang ukuran file kepada klien. 
- Fungsi format_size: Fungsi ini menerima ukuran file dalam byte dan mengembalikan string yang memformat ukuran tersebut ke dalam format yang lebih mudah dibaca.a. Ukuran file dibagi-bagi menjadi kategori berdasarkan ukurannya (bytes, KB, atau MB).b. Jika ukuran file kurang dari 1024 byte, ukurannya ditampilkan langsung dalam byte.c. Jika ukuran file kurang dari 1024 * 1024 byte (1 MB), ukurannya ditampilkan dalam KB dengan dua desimal.d. Jika ukuran file sama atau lebih besar dari 1 MB, ukurannya ditampilkan dalam MB dengan dua desimal.

![9](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/ab07eaf2-bb26-44fe-b60f-adb871666393)

- Definisi Fungsi Main: def main(): adalah deklarasi fungsi main yang merupakan tempat dimulainya eksekusi program.
- Membuat Socket Server: Baris pertama di dalam fungsi main membuat objek socket untuk server menggunakan socket.socket(socket.AF_INET, socket.SOCK_STREAM). Ini menghasilkan socket menggunakan alamat IPv4 dan protokol TCP/IP.
- Mengikat Socket ke Alamat dan Port: Baris berikutnya, server_socket.bind((TCP_IP, TCP_PORT)), mengikat socket server ke alamat IP dan port yang telah ditentukan sebelumnya.
- Mendengarkan Koneksi Masuk: server_socket.listen(5) menginstruksikan socket server untuk mulai mendengarkan koneksi masuk. Argument 5 menentukan jumlah maksimum antrian koneksi yang dapat ditangani secara bersamaan.
- Menampilkan Pesan: Pesan "FTP Server is listening on {} : {}".format(TCP_IP, TCP_PORT) dicetak ke konsol untuk memberi tahu bahwa server telah dimulai dan sedang mendengarkan koneksi di alamat IP dan port yang telah ditentukan.
- Loop Penerimaan Koneksi: Selanjutnya, program memasuki loop while True: yang berjalan tanpa henti. Di dalam loop ini, server terus-menerus menerima koneksi dari klien menggunakan server_socket.accept(). Setiap kali ada koneksi baru, server menerima koneksi tersebut dan menjalankan fungsi handle_client_connection untuk menangani komunikasi dengan klien.
- Pengecekan untuk Eksekusi Main: if __name__ == "__main__": memeriksa apakah skrip ini dieksekusi secara langsung (bukan diimpor sebagai modul oleh skrip lain). Jika ya, maka fungsi main() akan dieksekusi.

### Client

![10](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/bbbf9c33-0ce8-4319-a1e9-51b476792b32)

- Import Library: Kode tersebut mengimpor modul socket, yang digunakan untuk membuat dan mengelola koneksi jaringan.
- TCP_IP: Alamat IP server FTP yang akan dihubungi oleh klien. Dalam kasus ini, alamat loopback "127.0.0.1" digunakan.
- TCP_PORT: Port yang digunakan oleh server FTP untuk menerima koneksi. Dalam hal ini, port 8080 digunakan.
- BUFFER_SIZE: Ukuran buffer untuk menerima dan mengirim data antara klien dan server. Dalam kasus ini, ukuran buffer adalah 2048 byte.

![11](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/e8875ebd-00ea-45c0-a20c-fc3cf56399ef)

- Definisi Fungsi: def send_command(command, client_socket): adalah deklarasi fungsi yang mengambil dua argumen, yaitu command (perintah yang akan dikirim) dan client_socket (objek socket yang mewakili koneksi antara klien dan server).
- Mengirim Perintah: client_socket.send(command.encode()) digunakan untuk mengirim perintah dari klien ke server. P
- Menerima Respons: Setelah perintah dikirim, klien menunggu respons dari server menggunakan client_socket.recv(BUFFER_SIZE). Respons t
- Menampilkan Respons: Respons dari server kemudian dicetak ke konsol menggunakan print(response), sehingga pengguna dapat melihat hasil dari perintah yang dikirimkan.
- Penanganan Kesalahan: Jika terjadi kesalahan selama proses pengiriman perintah atau penerimaan respons, pengecualian akan ditangkap dan pesan kesalahan akan dicetak ke konsol.

![12](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/ed4c8ad5-36f0-4864-8136-b6871e9c08f9)

- Definisi Fungsi: def connme(client_socket): adalah deklarasi fungsi yang mengambil satu argumen, yaitu client_socket (objek socket yang mewakili koneksi antara klien dan server).
- Membuat Koneksi: Dalam blok try, client_socket.connect((TCP_IP, TCP_PORT)) digunakan untuk mencoba menyambungkan klien dengan server. 
- Pesan Sukses: Jika koneksi berhasil, pesan "Koneksi berhasil tersambung!" dicetak ke konsol untuk memberi tahu pengguna bahwa koneksi berhasil dibuat.
- Penanganan Kesalahan: Jika terjadi kesalahan selama proses menyambungkan klien dengan server, pengecualian akan ditangkap dan pesan kesalahan akan dicetak ke konsol menggunakan print("Koneksi gagal!", e).

![13](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/a9c5b7f2-7f36-4793-ad7a-1a85ec85167a)

- Definisi Fungsi: def upload_file(file_name, client_socket): adalah deklarasi fungsi yang mengambil dua argumen, yaitu file_name (nama file yang akan diunggah) dan client_socket (objek socket yang mewakili koneksi antara klien dan server).
- Mengirim Perintah "upload": Klien pertama kali mengirimkan perintah "upload" kepada server menggunakan client_socket.send(b"upload"). Ini memberi tahu server bahwa klien akan mengunggah sebuah file.
- Mengirim Nama File: Kemudian, nama file yang akan diunggah dikirim kepada server menggunakan client_socket.send(file_name.encode()). 
- Membuka dan Mengirim Data File: Fungsi membuka file yang akan diunggah dalam mode baca binary ("rb") menggunakan open(file_name, "rb") as file. Kemudian, data dari file tersebut dibaca dan dikirim kepada server menggunakan client_socket.send(data).
- Penerimaan Konfirmasi dari Server: Setelah file selesai diunggah, klien menerima konfirmasi dari server menggunakan client_socket.recv(BUFFER_SIZE).decode(). Pesan konfirmasi ini dicetak ke konsol agar pengguna dapat melihatnya.
- Penanganan Kesalahan: Jika terjadi kesalahan selama proses mengunggah file, pengecualian akan ditangkap dan pesan kesalahan akan dicetak ke konsol menggunakan print("Terjadi kesalahan saat mengunggah file:", e).

![14](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/5e057538-48e5-4a25-90db-43866abd0ca1)

- Definisi Fungsi Main: def main(): adalah deklarasi fungsi main yang merupakan tempat dimulainya eksekusi program klien.
- Membuat Socket Klien: Program pertama-tama membuat objek socket klien menggunakan socket.socket(socket.AF_INET, socket.SOCK_STREAM). .
- Loop Interaksi Pengguna: Program memasuki loop while True: yang berjalan tanpa henti. Di dalam loop ini, program menampilkan menu perintah kepada pengguna dan menunggu input perintah dari pengguna.
- Kondisi Pengolahan Perintah: Program memproses perintah yang dimasukkan oleh pengguna sesuai dengan kondisi-kondisi berikut:
    - Jika perintah adalah "byebye", program keluar dari loop.
    - Jika perintah adalah "connme", program mencoba untuk membuat koneksi sepenuhnya ke server dengan menggunakan fungsi connme.
- Penutupan Socket: Setelah pengguna memilih untuk keluar (dengan memasukkan "byebye"), program menutup socket klien dengan menggunakan client_socket.close().
- Eksekusi Fungsi Main: if __name__ == "__main__": memeriksa apakah skrip ini dieksekusi secara langsung (bukan diimpor sebagai modul oleh skrip lain). Jika ya, maka fungsi main() akan dieksekusi.

## Dokumentasi Command

![Server](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/661f1b89-29dc-4b7d-b1c5-c73622d0fdfb)

### Command 'connme'

![connme1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/3a296bfa-5656-4679-95c3-f71713425392)

![connme2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/2ca861f2-a3f0-47d5-8867-9ed6fb4ba9ae)

### Command 'ls'

![ls1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/95d91e33-34a7-4478-be34-65ba5b316afe)

![ls2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/e527b1e5-51f0-4e6f-ba08-aedfd6ce4dc1)

### Command 'rm'

![rm1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/ee93ee2b-3593-48f4-be41-91d3a8a72432)

![rm2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/e2a54fb2-2d5d-4d14-864d-f99369099717)


### Command 'download'

![download1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/c3c9451a-d0b2-48d1-9a75-b6405fd88d9e)

![download2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/308d5c2a-a936-47c1-a981-5bc43daf0f93)

  
### Command 'upload'

![upload1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/da718622-36f0-48bc-9f4a-4b2f2dbe631c)

![upload2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/37cab3fb-df3a-4e8e-ba85-74eefed3cb9f)


### Command 'size'

![size1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/e2761d6b-069f-4218-8fbe-56ec14279abb)

![size2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/3f8317fc-78c7-4063-a2c2-f35e65e852f7)


### Command 'byebye'

![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/c58e3a11-b457-4ade-8e7e-ccfcb8208ca6)


# Modifikasi Tugas-2-FTP-Socket-Programming-On-python

1. Modifikasi agar file yang diterima dimasukkan ke folder tertentu 
2. Modifikasi program agar memberikan feedback nama file dan filesize yang diterima.
3. Apa yang terjadi jika pengirim mengirimkan file dengan nama yang sama dengan file yang telah dikirim sebelumnya? Dapat menyebabkan masalah kah ? Lalu bagaimana solusinya? Implementasikan ke dalam program, solusi yang Anda berikan.

## Soal 1 dan 2
Soal 1 dan 2 sudah ditambahkan di codingannya, penjelasan ada di bagian setiap fiturnya

## Soal 3
Dalam program sebelumnya, jika klien mengirimkan file dengan nama yang sama dengan file yang telah dikirim sebelumnya, maka file yang sudah ada dengan nama tersebut akan ditimpa (overwrite) oleh file yang baru dikirim. Hal ini dapat menyebabkan berbagai masalah. Salah satu solusi untuk mengatasi masalah ini adalah dengan menambahkan penanganan khusus di sisi server untuk menghindari penimpaan file. Salah satu pendekatan yang dapat dilakukan adalah dengan menambahkan penanganan untuk mengubah nama file baru yang akan diunggah sehingga tidak ada konflik dengan file yang telah ada.

![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/f3fe85e0-cf4f-435c-9c8f-27b0f5afa315)

![new1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/96459493-6b31-414e-b87e-4f8d9ec49843)

![new2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/236821b6-3704-408e-af65-a695cf1a4b85)

![new3](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/3877d52f-aee8-4181-b05e-a94281242c75)

![new4](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/f7f54afe-d1c3-477d-91c9-16aa7b8e7c36)


