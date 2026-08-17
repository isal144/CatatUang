# CatatUang

CatatUang adalah web aplikasi sederhana untuk mencatat dan memantau pengeluaran sehari-hari.

## Fitur
- Menambahkan pengeluaran
- Menyimpan data dengan SQLite
- Menampilkan daftar pengeluaran
- Menghapus pengeluaran
- Menghitung total pengeluaran hari ini
- Menghitung total pengeluaran minggu ini
- Menghitung total pengeluaran bulan ini
- Menghitung total pengeluaran tahun ini
- Filter berdasarkan periode
- Filter berdasarkan kategori

## Teknologi
- Python
- Flask
- SQLite
- HTML

## Menjalankan di Termux

```bash
pkg install python
pip install flask
python app.py
```

Kemudian buka browser dan akses:

```text
http://127.0.0.1:5000
```

## Struktur proyek

```text
CatatUang/
├── app.py
├── templates/
│   └── index.html
├── .gitignore
└── README.md
```

Database `database.db` dibuat otomatis ketika aplikasi dijalankan.
