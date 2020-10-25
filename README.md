# jarkom-management-system
## Tugas 3 Socket Programming

## Anggota Kelompok :

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

- Text Previewer
- Factorio Calculator

## Referensi :

- 

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
5. Jika program sudah selesai dijalankan dan ingin mengakhiri periode fitur maka bisa ketik perintah “bye” pada periode multiconn-client.py
```bash
Say Something: bye
```




