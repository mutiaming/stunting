import pickle
import numpy as np
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import StuntingPrediction, User, Anak, DeviceData
import logging
from datetime import datetime

stunting_bp = Blueprint("stunting", __name__)

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model prediksi stunting
model_path = "models/logistic_regression_model.pkl"
model = None
try:
    with open(model_path, "rb") as file:
        model = pickle.load(file)
    logger.info("✅ Model berhasil dimuat!")
except FileNotFoundError:
    logger.error("❌ File model tidak ditemukan")
except Exception as e:
    logger.error(f"❌ Gagal memuat model: {str(e)}")

# Parameter statistik dari dataset training
MEAN_TB = 84.8082191780822
STD_TB = 13.507875824296994
MEAN_BB = 11.474520547945207
STD_BB = 3.699765773778378

def hitung_z_score(bb, tb, umur, jenis_kelamin):
    """Menghitung z-score berdasarkan parameter WHO"""
    try:
        # Validasi input tidak kosong
        if bb is None or tb is None or umur is None:
            logger.warning("Data input tidak lengkap")
            return None
            
        # Konversi ke float
        try:
            bb = float(bb)
            tb = float(tb)
            umur = float(umur)
        except (ValueError, TypeError):
            logger.warning("Input bukan angka yang valid")
            return None

        # Validasi range nilai
        if bb <= 0 or tb <= 0 or umur <= 0:
            logger.warning("Nilai input harus positif")
            return None
            
        if umur > 60:  # Batas maksimal 5 tahun (60 bulan)
            logger.warning("Umur melebihi batas maksimal")
            return None

        # Hitung z-score
        z_tb = (tb - MEAN_TB) / STD_TB
        z_bb = (bb - MEAN_BB) / STD_BB
        
        # Gabungkan z-score
        z_score = (z_tb + z_bb) / 2
        return round(z_score, 2)
        
    except Exception as e:
        logger.error(f"Error dalam hitung_z_score: {str(e)}")
        return None

@stunting_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict_stunting():
    """Endpoint untuk prediksi stunting manual"""
    try:
        # Validasi request JSON
        if not request.is_json:
            return jsonify({"message": "Request harus berupa JSON"}), 400
            
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Validasi field wajib
        required_fields = ["id_anak", "nama_anak", "nik", "jenis_kelamin", "umur", "berat_badan", "tinggi_badan"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "message": "Data tidak lengkap",
                "missing_fields": missing_fields
            }), 400

        # Hitung z-score
        z_score = hitung_z_score(
            data["berat_badan"],
            data["tinggi_badan"],
            data["umur"],
            data["jenis_kelamin"]
        )
        
        if z_score is None:
            return jsonify({"message": "Gagal menghitung z-score. Periksa data input."}), 400

        # Persiapkan fitur untuk model
        try:
            jenis_kelamin_num = 1 if str(data["jenis_kelamin"]).lower() in ["laki-laki", "l"] else 0
            fitur = np.array([[
                jenis_kelamin_num,
                float(data["umur"]),
                float(data["berat_badan"]),
                float(data["tinggi_badan"]),
                z_score
            ]], dtype=np.float32)
        except Exception as e:
            logger.error(f"Gagal mempersiapkan fitur: {str(e)}")
            return jsonify({"message": "Data input tidak valid"}), 400

        # Prediksi dengan model
        if model is None:
            return jsonify({"message": "Model belum dimuat"}), 500
            
        try:
            hasil_prediksi_num = int(model.predict(fitur)[0])
            hasil_prediksi = "Stunting" if hasil_prediksi_num == 1 else "Tidak Stunting"
        except Exception as e:
            logger.error(f"Gagal melakukan prediksi: {str(e)}")
            return jsonify({"message": "Gagal melakukan prediksi"}), 500

        # Simpan ke database
        try:
            prediksi = StuntingPrediction(
                user_id=user_id,
                id_anak=data["id_anak"],
                nama_anak=data["nama_anak"],
                nik=data["nik"],
                jenis_kelamin=data["jenis_kelamin"],
                umur=data["umur"],
                berat_badan=data["berat_badan"],
                tinggi_badan=data["tinggi_badan"],
                z_score=z_score,
                hasil_prediksi=hasil_prediksi,
                tanggal_prediksi=datetime.utcnow()
            )
            db.session.add(prediksi)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error(f"Gagal menyimpan prediksi: {str(e)}")
            return jsonify({"message": "Gagal menyimpan hasil prediksi"}), 500

        return jsonify({
            "message": "Prediksi berhasil",
            "data": {
                "z_score": z_score,
                "hasil_prediksi": hasil_prediksi,
                "status": hasil_prediksi
            }
        }), 200

    except Exception as e:
        logger.error(f"Error tidak terduga: {str(e)}")
        return jsonify({"message": "Terjadi kesalahan internal"}), 500

@stunting_bp.route("/alat-predict", methods=["POST"])
def receive_from_alat():
    """Endpoint untuk menerima data dari alat pengukur"""
    try:
        berat = request.form.get('berat')
        tinggi = request.form.get('tinggi')
        status = request.form.get('status')

        if not all([berat, tinggi, status]):
            return jsonify({'message': 'Data tidak lengkap'}), 400

        try:
            berat = float(berat)
            tinggi = float(tinggi)
        except ValueError:
            return jsonify({'message': 'Data berat/tinggi tidak valid'}), 400

        # Simpan ke database
        new_data = DeviceData(
            berat_badan=berat,
            tinggi_badan=tinggi,
            status=status
        )
        db.session.add(new_data)
        db.session.commit()

        return jsonify({'message': 'Data berhasil disimpan'}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error menyimpan data alat: {str(e)}")
        return jsonify({'message': 'Gagal menyimpan data alat'}), 500

@stunting_bp.route('/alat/latest', methods=['GET'])
def get_latest_device_data():
    """Mendapatkan data terbaru dari alat"""
    try:
        latest_data = DeviceData.query.order_by(DeviceData.timestamp.desc()).first()
        if latest_data:
            return jsonify({
                'data': {
                    'tinggi_badan': latest_data.tinggi_badan,
                    'berat_badan': latest_data.berat_badan
                }
            })
        return jsonify({'message': 'Data alat tidak ditemukan'}), 404
    except Exception as e:
        logger.error(f"Error mengambil data alat: {str(e)}")
        return jsonify({'message': 'Gagal mengambil data alat'}), 500

@stunting_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    """Endpoint untuk mendapatkan riwayat prediksi"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User tidak ditemukan"}), 404

        # Query dasar
        query = db.session.query(
            StuntingPrediction.id,
            StuntingPrediction.id_anak,
            StuntingPrediction.nik,
            StuntingPrediction.nama_anak,
            StuntingPrediction.tinggi_badan,
            StuntingPrediction.berat_badan,
            StuntingPrediction.jenis_kelamin,
            StuntingPrediction.umur,
            StuntingPrediction.z_score,
            StuntingPrediction.hasil_prediksi,
            StuntingPrediction.tanggal_prediksi,
            Anak.nama_orang_tua,
        ).join(
            Anak, StuntingPrediction.id_anak == Anak.id
        ).order_by(
            StuntingPrediction.id.desc()
        )

        if user.role != "admin":
            query = query.filter(StuntingPrediction.user_id == user_id)

        predictions = query.all()

        history_data = [
            {
                "id": pred.id,
                "id_anak": pred.id_anak,
                "nik": pred.nik,
                "nama_anak": pred.nama_anak,
                "nama_ortu": pred.nama_orang_tua,
                "tinggi_badan": float(pred.tinggi_badan),
                "berat_badan": float(pred.berat_badan),
                "jenis_kelamin": pred.jenis_kelamin,
                "umur": int(pred.umur),
                "z_score": float(pred.z_score),
                "hasil_prediksi": pred.hasil_prediksi,
                "tanggal_prediksi": pred.tanggal_prediksi.strftime("%d-%m-%Y")
            }
            for pred in predictions
        ]

        return jsonify({
            "message": "Riwayat prediksi ditemukan",
            "history": history_data
        }), 200

    except Exception as e:
        logger.error(f"Error mendapatkan riwayat: {str(e)}")
        return jsonify({"message": "Gagal mendapatkan riwayat"}), 500