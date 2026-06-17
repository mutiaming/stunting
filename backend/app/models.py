from app import db
from sqlalchemy.sql import func

# ✅ Model User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='user')  # 'user', 'admin', 'bidan'

# ✅ Model Anak
class Anak(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(16), unique=True, nullable=False)
    nama_anak = db.Column(db.String(100), nullable=False)
    nama_orang_tua = db.Column(db.String(100), nullable=False)
    
    # Relasi ke StuntingPrediction
    predictions = db.relationship('StuntingPrediction', backref='anak', lazy=True)

# ✅ Model Prediksi Stunting
class StuntingPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_anak = db.Column(db.Integer, db.ForeignKey('anak.id'), nullable=False)  # ✅ Relasi ke Anak
    nik = db.Column(db.String(16), nullable=False)
    nama_anak = db.Column(db.String(100), nullable=False)
    jenis_kelamin = db.Column(db.Integer, nullable=False)  
    umur = db.Column(db.Integer, nullable=False)
    berat_badan = db.Column(db.Float, nullable=False)
    tinggi_badan = db.Column(db.Float, nullable=False)
    z_score = db.Column(db.Float, nullable=False)
    hasil_prediksi = db.Column(db.String(20), nullable=False)
    tanggal_prediksi = db.Column(db.DateTime, default=func.now())  # ✅ Timestamp otomatis

    def __repr__(self):
        return f'<StuntingPrediction {self.id} - {self.nama_anak} ({self.hasil_prediksi})>'

# ✅ Model Prediksi Calon Ibu
class CalonIbuPrediction(db.Model):
    id_prediction = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    usia = db.Column(db.Integer, nullable=False)
    riwayat_gizi = db.Column(db.String(10), nullable=False)
    konsumsi_gizi = db.Column(db.String(10), nullable=False)
    cek_kesehatan = db.Column(db.String(10), nullable=False)
    riwayat_stunting = db.Column(db.String(10), nullable=False)
    pendidikan = db.Column(db.String(20), nullable=False)
    pola_asuh = db.Column(db.String(10), nullable=False)
    ekonomi = db.Column(db.String(20), nullable=False)
    tinggi_badan = db.Column(db.Float, nullable=False)
    berat_badan = db.Column(db.Float, nullable=False)
    hasil_prediksi = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())

# ✅ Model MPASI
class MPASI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_makanan = db.Column(db.String(255), nullable=False)
    usia_minimum = db.Column(db.Integer, nullable=False)
    deskripsi = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    
class DeviceData(db.Model):
    __tablename__ = 'device_raw_data'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Data dari perangkat
    berat_badan = db.Column(db.Float, nullable=False)    # Berat badan dari alat
    tinggi_badan = db.Column(db.Float, nullable=False)   # Tinggi badan dari alat
    status = db.Column(db.String(30), nullable=False)    # Status hasil klasifikasi stunting
    
    timestamp = db.Column(db.DateTime, default=func.now())  # Otomatis diisi saat data masuk

    def __repr__(self):
        return f'<DeviceData {self.id} | {self.berat_badan}kg | {self.tinggi_badan}cm | {self.status}>'