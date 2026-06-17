from app import db

class CalonIbuPrediction(db.Model):
    __tablename__ = "calon_ibu_prediction"

    id_prediction = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # FK ke User
    username = db.Column(db.String(50), nullable=False)  # Menyimpan username dari User
    usia = db.Column(db.Integer, nullable=False)
    riwayat_gizi = db.Column(db.Enum('ya', 'tidak', name="riwayat_gizi"), nullable=False)
    konsumsi_gizi = db.Column(db.Enum('sering', 'jarang', 'tidak pernah', name="konsumsi_gizi"), nullable=False)
    cek_kesehatan = db.Column(db.Enum('ya', 'tidak', name="cek_kesehatan"), nullable=False)
    riwayat_stunting = db.Column(db.Enum('ya', 'tidak', name="riwayat_stunting"), nullable=False)
    pendidikan = db.Column(db.Enum('tidak sekolah', 'sd', 'smp', 'sma', 'd3', 's1', 's2', name="pendidikan"), nullable=False)
    pola_asuh = db.Column(db.Enum('sudah', 'belum', name="pola_asuh"), nullable=False)
    ekonomi = db.Column(db.Enum('kurang baik', 'cukup baik', 'baik', 'baik sekali', name="ekonomi"), nullable=False)
    tinggi_badan = db.Column(db.Float, nullable=False)
    berat_badan = db.Column(db.Float, nullable=False)
    hasil_prediksi = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)

    user = db.relationship('User', backref=db.backref('predictions', lazy=True))
