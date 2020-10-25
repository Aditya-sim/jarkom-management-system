# jarkom-management-system
## Tugas 3 Socket Programming

## Kelompok (A4) :

- Faishal Ridwan - 1706040201
- Insanul Fahmi - 1706979291
- Aditya Pratama - 1706039490

## Judul Proyek :

Python Master Worker Architecture

## Requirement Proyek :

- Python 3.7.1
- Library Socket
- Library Thread
- Library OS
- AWS EC2 Instance
- SSH Client

## Fitur :

- Text Previewer (Text Previewer berfungsi untuk menggunakan fungsi request dari library python untuk mengambil file dengan format .txt agar bisa ditampilkan di sisi client).
- Factorio Calculator (Deskripsi : Factorio Calculator berfungsi sebagai kalkulator untuk mengkalkulasi jumlah raw material yang dibutuhkan untuk membuat suatu item di game Factorio).

## Referensi :

- https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
- https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/

## Cara setup proyek :

1. Clone repository app on [this repository](https://github.com/Aditya-sim/jarkom-management-system)
2. Create EC2 Instance on AWS
3. Install python on EC2 Instance
4. Deploy multiconn-server.py on EC2 Instance
5. Establish with connection with EC2 server with IPv4 Global IP address

## Cara menjalankan fitur Text Previewer :

1. Pertama tama pastikan sudah didalam folder repo, requirement yang dibutuhkan sudah tersedia, dan setup proyek sudah dilakukan.
2. Run multiconn-server.py dengan python versi 3 lalu tunggu beberapa saat.
```bash
python3 multiconn-server.py
```
3. Run multiconn-client.py untuk memulai thread.
```bash
python3 multiconn-client.py
```
4. Isi field Say Something dengan “Text Previewer” dan masukan url yang akan di preview. Pada kali ini contoh url.txt yaitu [alice.txt](http://gaia.cs.umass.edu/wiresharklabs/alice.txt)
5. Jika program sudah selesai dijalankan dan ingin mengakhiri periode fitur maka bisa lakukan perintah “bye” pada periode multiconn-client.py
```bash
Say Something: bye
```

## Cara menjalankan fitur Factorio Calculator :

1. Pertama tama pastikan sudah didalam folder repo, requirement yang dibutuhkan sudah tersedia, dan setup proyek sudah dilakukan.
2. Run multiconn-server.py dengan python versi 3 lalu tunggu beberapa saat.
```bash
python3 multiconn-server.py
```
3. Run multiconn-client.py untuk memulai thread.
```bash
python3 multiconn-client.py
```
4. Isi field Say Something dengan “Factorio Calculator”.
5. Selama dalam periode fitur Factorio Calculator bisa ikuti prosedur berdikut :
 - Masukkan item yang ingin didapatkan, lalu masukkan 'proceed' untuk masuk ke stage selanjutnya
 - Pilih item yang akan dipecah, atau masukkan 0 untuk selesai
 - Pilih recipe untuk memecahkan item
 - Ketika sudah selesai, pilih apakah ingin melakukan kalkulasi lagi (y/n)
6. Jika program sudah selesai dijalankan dan ingin mengakhiri periode fitur maka bisa lakukan perintah “bye” pada periode multiconn-client.py
```bash
Say Something: bye
```



