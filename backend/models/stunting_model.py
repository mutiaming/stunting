from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StuntingPrediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_anak = db.Column(db.Integer, db.ForeignKey('anak.id'), nullable=False)  # ✅ Pastikan ini ada
    nama_anak = db.Column(db.String(100), nullable=False)
    nik = db.Column(db.String(16), nullable=False)
    jenis_kelamin = db.Column(db.Integer, nullable=False)  
    umur = db.Column(db.Integer, nullable=False)
    berat_badan = db.Column(db.Float, nullable=False)
    tinggi_badan = db.Column(db.Float, nullable=False)
    z_score = db.Column(db.Float, nullable=False)
    hasil_prediksi = db.Column(db.String(20), nullable=False)
    tanggal_prediksi = db.Column(db.DateTime, default=db.func.current_timestamp())  # ✅ Sudah benar

    def __repr__(self):
        return f'<StuntingPrediction {self.id} - {self.nama_anak} ({self.hasil_prediksi})>'
