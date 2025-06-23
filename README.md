# 🛡️ SMShield – Sistem Deteksi Pesan Berbahaya Phishing (Smishing) secara Real-Time Berbasis Aplikasi Mobile dengan Pendekatan Deep Learning

---

## 📖 Overview

**SMShield** adalah sistem deteksi smishing (SMS phishing) yang dibangun untuk menjawab kebutuhan akan perlindungan dari pesan berbahaya yang sering kali menipu pengguna melalui teknik social engineering dalam SMS.

Sistem ini bekerja secara otomatis di latar belakang, memonitor SMS masuk, lalu mengirim isi pesan ke API backend untuk diklasifikasikan dengan model deep learning. Hasil klasifikasi kemudian dikirim kembali dan ditampilkan ke pengguna dalam bentuk notifikasi.

Sistem ini terdiri dari dua komponen utama:
- **Aplikasi Android**: Mendeteksi SMS masuk dan mengirim pesan SMS ke server.
- **API Backend Flask**: Mengklasifikasikan isi SMS menggunakan model machine learning.

---

## 🛠️ Tech Stack & Tools Used

- **Android App**: Kotlin, Jetpack Compose, BroadcastReceiver, NotificationManager  
- **Backend**: Python 3, Flask, RESTful API, Requests  
- **Model**: BiLSTM
- **Server**: Linux-based ITS server (akses via SSH + VPN)  
- **Integrasi**: Retrofit2 (Android), REST API  
- **Deployment**: Virtualenv + `flask run` + `nohup`

---

## 🌐 Setup Guide: SMShield Backend on ITS Server

Untuk menjalankan API Flask di server ITS, ikuti langkah-langkah berikut:

### 1. Koneksi ke VPN ITS
- Gunakan aplikasi VPN (OpenVPN Connect).
- Setelah terhubung, pastikan kamu bisa mengakses server dengan:
  ```bash
  ping [IP_SERVER]
  ```

### 2. Login ke Server via SSH
Login ke server menggunakan perintah:
```bash
ssh username@IP_SERVER
```

### 3. Clone Proyek dari GitHub
Setelah berhasil login ke server:
```bash
git clone https://github.com/anrahmapuri/api-smshield.git
cd api-smshield
```

### 4. Buat dan Aktifkan Virtual Environment
Buat environment Python terisolasi agar dependensi tidak bentrok:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install Dependensi
Pastikan file `requirements.txt` kamu berisi:
```
Flask==2.2.5
tensorflow==2.17.1
numpy
Sastrawi
```
Kemudian jalankan:
```bash
pip install -r requirements.txt
```

### 6. Export FLASK_APP dan Jalankan API Flask
Agar Flask tahu file utama yang akan dijalankan:
```bash
export FLASK_APP=main.py
```
Jalankan Flask di background menggunakan `nohup`:
```bash
nohup flask run --host=0.0.0.0 --port=8000 > flask.log 2>&1 &
```
API sekarang berjalan dan dapat diakses melalui:
```
http://[IP_SERVER]:8000/predict
```

### 7. Tes Akses API dari Android
Pastikan aplikasi Android kamu menggunakan URL:
```
http://[IP_SERVER]:8000/predict
```
Dan perangkat sudah connect ke VPN ITS.

### 8. (Opsional) Monitoring dan Stop

**Lihat log secara real-time:**
```bash
tail -f flask.log
```

**Cek proses Flask yang berjalan:**
```bash
ps aux | grep flask
```

**Hentikan proses Flask:**
```bash
kill [PID]
```
Gantilah `[PID]` dengan nomor proses yang muncul dari perintah sebelumnya.

---

## 👩🏻‍💻 Meet the Developer

Proyek ini dikembangkan oleh **Annisa Rahmapuri** sebagai bagian dari Tugas Akhir Departemen Teknologi Informasi. 

📚 Judul Skripsi:  
**"SMShield: Sistem Deteksi Pesan Berbahaya Phishing (Smishing) secara Real-time Berbasis Aplikasi Mobile dengan Pendekatan Deep Learning"**

📍 Institusi: Institut Teknologi Sepuluh Nopember (ITS)  
📅 Tahun: 2025
