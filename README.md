# Tugas-2-FTP-Socket-Programming-On-python

Nama : Hammam Jauharul Karim

NIM : 1203222050

Kelas : IF-02-01

## Penjelasan Code Program

### Code Server
![1](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/403a50f1-6a69-4d34-b79f-ce9a3ded5eba)
- socket: Modul ini menyediakan antarmuka untuk soket (socket), yang merupakan ujung dari saluran komunikasi dua arah yang memungkinkan komunikasi antara proses.
- os: Modul ini menyediakan berbagai fungsi yang berinteraksi dengan sistem operasi, dalam hal ini digunakan untuk operasi-operasi terkait file seperti mengirim, menerima, menghapus, atau memeriksa file di server.

![2](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/930d98ba-5ab5-4669-84a6-fbc4b79b6b12)

- Fungsi ini mengirim daftar file dan folder yang ada dalam direktori kerja server ke klien.
- **os.listdir('.')** digunakan untuk mendapatkan daftar file dan folder dalam direktori kerja saat ini.
- Daftar tersebut diubah menjadi string dengan menggunakan **'\n'.join(files)** dan dikirimkan ke klien dengan **client_socket.send().**

![3](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/ee4bc232-dd11-46a9-a368-ecd1ab26c473)

- Fungsi ini menghapus file yang ditentukan oleh klien dari server.
- Jika file ditemukan, **fungsi os.remove(filename)** akan menghapus file tersebut.
- Pesan yang sesuai (berhasil dihapus atau tidak ditemukan) dikirimkan kembali ke klien.

![4](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/55033b51-f3e4-4b57-ae6e-bfa1e903f2ef)

- Fungsi ini mengirimkan isi file yang ditentukan oleh klien dari server ke klien.
- Jika file ditemukan, file dibuka dalam mode binary ('rb') dan seluruh isinya dibaca dan dikirimkan ke klien menggunakan **client_socket.send().**
  
![5](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/4e569499-adee-4440-9f3d-8d806da50dd0)

- Fungsi ini menerima file dari klien dan menyimpannya di server dengan nama file yang ditentukan.
- Data yang diterima dari klien dibaca dan ditulis ke file yang sesuai dengan nama file yang diberikan oleh klien.
- Ketika tidak ada data lagi yang diterima, fungsi mengirimkan pesan konfirmasi kembali ke klien.

![6](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/e95ee616-4b10-441c-8f3b-51b3e9732389)

- Fungsi ini mengirimkan informasi ukuran file yang ditentukan oleh klien dari server ke klien.
- Jika file ditemukan, ukuran file dihitung menggunakan **os.path.getsize(filename)** dan dikonversi ke MB sebelum dikirimkan ke klien.

![7](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/6b59a90b-716d-4434-8e2f-07433b3ff79f)

- Fungsi ini menangani koneksi baru dari klien.
- Ketika koneksi terbentuk, fungsi ini menunggu perintah dari klien.
- Perintah diterima, dipisahkan menjadi bagian-bagian, dan nama perintahnya diekstrak.
- Berdasarkan nama perintah, fungsi memanggil fungsi yang sesuai untuk menangani perintah tersebut.
- Koneksi akan berlanjut hingga klien mengirimkan perintah **'byebye'**, yang menandakan bahwa klien ingin keluar dari koneksi.
- Pesan akan dicetak ketika koneksi selesai.

![8](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/d64431e7-9701-48e4-b6a4-ec6c1d51163e)

- Fungsi ini merupakan titik awal eksekusi program server.
- Membuat socket server, mengikatnya ke alamat IP dan port tertentu, dan mulai mendengarkan koneksi baru.
- Ketika koneksi baru diterima, **handle_connection()** dipanggil untuk menangani koneksi tersebut.
- Program akan berjalan dalam loop tak terbatas untuk terus menerima koneksi baru.

### Code Client

![9](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/cbcb8948-0f2e-4251-8efb-28816595ed07)

- Modul socket digunakan untuk membuat koneksi jaringan antara client dan server.

![10](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/5f7658c3-9383-4fb5-9b86-034632b31252)

- Fungsi main() merupakan titik awal eksekusi program client.
- Membuat socket client dan melakukan koneksi ke server yang berjalan di localhost dengan port 9999.
- Dalam loop tak terbatas, client akan meminta input dari pengguna untuk perintah yang akan dikirim ke server.
- Input perintah dari pengguna dikirim ke server menggunakan **client_socket.send(command.encode())**.
- Jika perintah yang dimasukkan adalah 'byebye', maka client akan keluar dari loop dan menutup koneksi.
- Jika perintah adalah 'connme', client akan menutup koneksi saat ini, mencetak pesan, membuat koneksi baru ke server, dan mencetak pesan bahwa koneksi baru telah tersambung.
- Jika perintah dimulai dengan 'upload', client akan menerima respons dari server dan mencetaknya.
- Untuk perintah lainnya, client menerima respons dari server dan mencetaknya.
- **client_socket.recv(1024)**: Metode ini digunakan untuk menerima data dari server. Argumen 1024 adalah ukuran buffer, yaitu berapa banyak byte yang akan diterima dari server setiap kali.
- **command.encode()**: Digunakan untuk mengonversi string perintah menjadi representasi byte karena socket bekerja dengan byte, bukan string.
- **response = client_socket.recv(1024).decode()**: Mengonversi byte yang diterima dari server menjadi string agar dapat dicetak atau diproses lebih lanjut oleh client.
- **client_socket.close()**: Menutup koneksi socket dengan server.

## Dokumentasi dan Penjelasan Command

### Command 'ls'
![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/c87a16f8-33aa-48b7-b0ed-6954a78ee4a2)

- Ketika server menerima perintah 'ls' dari klien, fungsi **handle_connection()** akan memprosesnya.
- Fungsi **handle_connection()** memecah pesan yang diterima dari klien menjadi bagian-bagian, dan mengekstrak nama perintahnya.
- Karena nama perintah adalah 'ls', maka server akan memanggil fungsi **send_list(client_socket)**.
- Fungsi **send_list(client_socket)** akan digunakan untuk mengirim daftar file dan folder yang ada di direktori kerja server ke klien.
- Fungsi ini menggunakan **os.listdir('.')** untuk mendapatkan daftar file dan folder dalam direktori kerja saat ini.
- Daftar tersebut kemudian diubah menjadi string dengan menggunakan '\n'.**join(files)** dan dikirimkan ke klien dengan **client_socket.send()**
- Setelah mengirimkan perintah 'ls', klien akan menunggu respons dari server.
- Klien akan menerima respons dari server melalui **client_socket.recv(1024).decode()**.
- Respons yang diterima akan di-decode menjadi string.
- String tersebut berisi daftar file dan folder yang dikirimkan oleh server.
- Klien akan mencetak daftar file dan folder tersebut sehingga pengguna dapat melihatnya..
- Cara menggunakan command tersebut adalah dengan mengetikkan saja perintah **'ls'** pada terminalnya.


### Command 'rm'

![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/d2438980-6335-4a7a-b279-a6f29fdae285)
- Ketika server menerima perintah 'rm' dari klien, **fungsi handle_connection()** akan memprosesnya.
- Fungsi **handle_connection()** akan memecah pesan yang diterima dari klien menjadi bagian-bagian, dan mengekstrak nama perintahnya serta nama file yang akan dihapus.
- Setelah mendapatkan nama file yang akan dihapus, server akan memanggil fungsi **remove_file(client_socket, filename)**.
- Fungsi **remove_file(client_socket, filename)** akan mencoba untuk menghapus file yang ditentukan dari server menggunakan **os.remove(filename)**.
- Jika file berhasil dihapus, server akan mengirim pesan "File Berhasil Dihapus" kepada klien melalui **client_socket.send()**.
- Jika file tidak ditemukan, server akan mengirim pesan "File Tidak Ditemukan" kepada klien melalui **client_socket.send()**.
- Setelah mengirimkan perintah 'rm', klien akan menunggu respons dari server.
- Klien akan menerima respons dari server melalui **client_socket.recv(1024).decode()**.
- Respons yang diterima akan di-decode menjadi string.
- Klien akan mencetak pesan respons yang diterima dari server, baik itu "File Berhasil Dihapus" jika file berhasil dihapus, atau "File Tidak Ditemukan" jika file tidak ditemukan atau gagal dihapus.
- Cara menggunakan command tersebut adalah dengan cara mengetikkan perintah 'rm namaFile' dan diikuti dengan format dari file tersebut (jika ada).
### Command 'download'
![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/52c4bc13-cfda-4a09-a24b-2a2fd351fe88)
- Ketika server menerima perintah 'download' dari klien, fungsi **handle_connection()** akan memprosesnya.
- Fungsi **handle_connection()** akan memecah pesan yang diterima dari klien menjadi bagian-bagian, dan mengekstrak nama perintahnya serta nama file yang akan di-download.
- Setelah mendapatkan nama file yang akan di-download, server akan memanggil fungsi **send_file(client_socket, filename)**.
- Fungsi **send_file(client_socket, filename)** akan mencoba membuka file yang ditentukan dalam mode baca biner ('rb') dan membaca seluruh isi file tersebut.
- Kemudian, isi file akan dikirimkan ke klien menggunakan **client_socket.send()**.
- Setelah mengirimkan perintah 'download', klien akan menunggu respons dari server.
- Klien akan menerima data file dari server dalam bentuk byte array menggunakan **client_socket.recv(1024)**.
- Data file yang diterima akan disimpan dalam buffer atau file baru di sisi klien, sesuai dengan implementasi program.
- Setelah menerima seluruh isi file, klien akan menerima pesan konfirmasi "File Berhasil Dibuat" dari server melalui **client_socket.recv(1024).decode()**
- Cara menggunakan command tersebut adalah dengan cara mengetikkan perintah 'download namaFile' dan diikuti dengan format dari file tersebut (jika ada).
  
### Command 'upload'
![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/403f27a8-5a26-4018-95db-f03f06ca43c9)
- Ketika klien memasukkan perintah 'upload', fungsi main() akan memprosesnya.
- Klien akan mengirimkan perintah 'upload' ke server menggunakan **client_socket.send(command.encode())**.
- Setelah mengirim perintah 'upload', klien akan menunggu respons dari server.
- Klien menerima respons dari server melalui **client_socket.recv(1024).decode()**.
- Ketika server menerima perintah 'upload' dari klien, fungsi **handle_connection()** akan memprosesnya.
- Fungsi ini akan memecah pesan yang diterima dari klien menjadi bagian-bagian, dan mengekstrak nama perintahnya serta nama file yang akan di-upload.
- Setelah mendapatkan nama file yang akan di-upload, server akan memanggil fungsi **receive_file(client_socket, filename)**.
- Fungsi **receive_file(client_socket, filename)** akan menerima file yang dikirimkan oleh klien.
- Server membuka file baru dan menuliskan data yang diterima dari klien ke file tersebut hingga semua data telah diterima.
- Setelah file selesai ditulis, server mengirim pesan konfirmasi "File Berhasil Dibuat" kepada klien.
- Cara menggunakan command tersebut adalah dengan cara mengetikkan perintah 'upload namaFile' dan diikuti dengan format dari file tersebut (jika ingin).

### Command 'size'
![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/2d52058d-eac5-4f6d-88be-e36ed080126b)
- Ketika server menerima perintah 'size' dari klien, fungsi **handle_connection()** akan memprosesnya.
- Fungsi ini akan memecah pesan yang diterima dari klien menjadi bagian-bagian, dan mengekstrak nama perintahnya serta nama file yang akan diambil ukurannya.
- Setelah mendapatkan nama file, server akan memanggil fungsi **send_file_size(client_socket, filename)**.
- Fungsi **send_file_size(client_socket, filename)** akan mencoba untuk mendapatkan ukuran file yang ditentukan dari server menggunakan **os.path.getsize(filename)**.
- Ukuran file akan dihitung dan dikirimkan ke klien melalui **client_socket.send()** dalam format yang telah ditentukan.
- Setelah mengirimkan perintah 'size', klien akan menunggu respons dari server.
- Klien akan menerima respons dari server melalui **client_socket.recv(1024).decode()**.
- Respons yang diterima akan di-decode menjadi string.
- Klien akan mencetak ukuran file yang diterima dari server.
- Cara menggunakan command tersebut adalah dengan cara mengetikkan perintah 'size namaFile' dan diikuti dengan format dari file tersebut (jika ada).

### Command 'byebye'
![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/f74f1cfd-090a-40cc-9ae3-f107a81a8612)
- Ketika klien memasukkan perintah 'byebye', fungsi main() akan memprosesnya.
- Klien akan mengirimkan perintah 'byebye' ke server menggunakan **client_socket.send(command.encode())**.
- Setelah mengirim perintah 'byebye', klien akan keluar dari loop utama dan menutup koneksi socket dengan server menggunakan **client_socket.close()**.
- Ketika klien memasukkan perintah 'byebye', fungsi main() akan memprosesnya.
- Klien akan mengirimkan perintah 'byebye' ke server menggunakan **client_socket.send(command.encode())**.
- Setelah mengirim perintah 'byebye', klien akan keluar dari loop utama dan menutup koneksi socket dengan server menggunakan **client_socket.close()**.
- Cara menggunakan command tersebut adalah dengan mengetikkan saja perintah **'byebye'** pada terminalnya.
### Command 'connme'
![image](https://github.com/hammamkarim/Tugas-2---FTP-Socket-Programming-On-python/assets/114963944/efb6205e-ac1b-4895-bca6-d5a815c03eb4)
- Ketika klien memasukkan perintah 'connme', fungsi **main()** akan memprosesnya.
- Klien akan menutup koneksi socket saat ini dengan menggunakan **client_socket.close()**.
- Setelah menutup koneksi saat ini, klien akan mencetak pesan "Koneksi Ditutup" untuk memberi tahu pengguna bahwa koneksi telah ditutup.
- Selanjutnya, klien akan membuat koneksi baru ke server menggunakan **socket.socket(socket.AF_INET, socket.SOCK_STREAM)** dan **client_socket.connect(('localhost', 9999))**.
- Klien mencetak pesan "Koneksi Baru Tersambung" untuk memberi tahu pengguna bahwa koneksi baru telah berhasil dibuat.
- Cara menggunakan command tersebut adalah dengan mengetikkan saja perintah **'connme'** pada terminalnya.


