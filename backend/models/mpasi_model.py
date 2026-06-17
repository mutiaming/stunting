from app import db

class MPASI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_makanan = db.Column(db.String(255), nullable=False)  # Nama makanan
    usia_minimum = db.Column(db.Integer, nullable=False)  # Usia minimum bayi (bulan)
    deskripsi = db.Column(db.Text, nullable=False)  # Deskripsi makanan
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())  # Waktu dibuat
