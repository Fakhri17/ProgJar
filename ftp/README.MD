# Tugas 2 - FTP Socket Programming On python

#### Nama  : Fakhri Alauddin | NIM : 1203220131

## Ringkasan
Program FTP Socket menggunakan Protokol TCP. Menggunakan bahasa python sebagai bahasa pemrogramannya.

## Soal
buat sebuah program file transfer protocol menggunakan socket programming dengan beberapa perintah dari client seperti berikut.
- ls : ketika client menginputkan command tersebut, maka server akan memberikan daftar file dan folder. 
- rm {nama file} : ketika client menginputkan command tersebut, maka server akan menghapus file dengan acuan nama file yang diberikan pada parameter pertama.
- download {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan file dengan acuan nama file yang diberikan pada parameter pertama.
- upload {nama file} : ketika client menginputkan command tersebut, maka server akan menerima dan menyimpan file dengan acuan nama file yang diberikan pada parameter pertama.
- size {nama file} : ketika client menginputkan command tersebut, maka server akan memberikan informasi file dalam satuan MB (Mega bytes) dengan acuan nama file yang diberikan pada parameter pertama.
- byebye : ketika client menginputkan command tersebut, maka hubungan socket client akan diputus.
- connme : ketika client menginputkan command tersebut, maka hubungan socket client akan terhubung.

## Penjelasan