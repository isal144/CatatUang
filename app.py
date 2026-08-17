from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date, timedelta

app = Flask(__name__, template_folder=".")
DATABASE = "database.db"


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengeluaran (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nominal INTEGER NOT NULL,
            kategori TEXT NOT NULL,
            tanggal TEXT NOT NULL,
            keterangan TEXT
        )
    """)
    conn.commit()
    conn.close()


def ambil_data():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM pengeluaran
        ORDER BY tanggal DESC, id DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data


def hitung_total(data, periode):
    hari_ini = date.today()
    total = 0

    for item in data:
        tanggal = date.fromisoformat(item[4])

        if periode == "hari":
            if tanggal == hari_ini:
                total += item[2]

        elif periode == "minggu":
            awal_minggu = hari_ini - timedelta(days=hari_ini.weekday())
            akhir_minggu = awal_minggu + timedelta(days=6)
            if awal_minggu <= tanggal <= akhir_minggu:
                total += item[2]

        elif periode == "bulan":
            if tanggal.month == hari_ini.month and tanggal.year == hari_ini.year:
                total += item[2]

        elif periode == "tahun":
            if tanggal.year == hari_ini.year:
                total += item[2]

    return total


@app.route("/")
def halaman_utama():
    data = ambil_data()

    total_hari = hitung_total(data, "hari")
    total_minggu = hitung_total(data, "minggu")
    total_bulan = hitung_total(data, "bulan")
    total_tahun = hitung_total(data, "tahun")

    periode = request.args.get("periode", "semua")
    kategori = request.args.get("kategori", "Semua")
    data_tampil = data

    if periode != "semua":
        hari_ini = date.today()
        hasil = []

        for item in data:
            tanggal = date.fromisoformat(item[4])
            cocok = False

            if periode == "hari":
                cocok = tanggal == hari_ini
            elif periode == "minggu":
                awal_minggu = hari_ini - timedelta(days=hari_ini.weekday())
                akhir_minggu = awal_minggu + timedelta(days=6)
                cocok = awal_minggu <= tanggal <= akhir_minggu
            elif periode == "bulan":
                cocok = tanggal.month == hari_ini.month and tanggal.year == hari_ini.year
            elif periode == "tahun":
                cocok = tanggal.year == hari_ini.year

            if cocok:
                hasil.append(item)

        data_tampil = hasil

    if kategori != "Semua":
        data_tampil = [item for item in data_tampil if item[3] == kategori]

    return render_template(
        "index.html",
        data=data_tampil,
        total_hari=total_hari,
        total_minggu=total_minggu,
        total_bulan=total_bulan,
        total_tahun=total_tahun
    )


@app.route("/tambah", methods=["POST"])
def tambah():
    nama = request.form["nama"]
    nominal = int(request.form["nominal"])
    kategori = request.form["kategori"]
    tanggal = request.form["tanggal"]
    keterangan = request.form["keterangan"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pengeluaran
        (nama, nominal, kategori, tanggal, keterangan)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, nominal, kategori, tanggal, keterangan))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/hapus/<int:id>")
def hapus(id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pengeluaran WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
