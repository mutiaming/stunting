from app import db

class Anak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    nama_anak = db.Column(db.String(100), nullable=False)
    nama_orang_tua = db.Column(db.String(100), nullable=False)
