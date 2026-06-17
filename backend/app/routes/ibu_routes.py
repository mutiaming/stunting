from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import CalonIbuPrediction, User
from sqlalchemy.exc import SQLAlchemyError

ibu_bp = Blueprint('ibu', __name__)

# Fungsi untuk menentukan kategori BMI
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesitas"

# ✅ Menyimpan prediksi calon ibu
@ibu_bp.route('/predict', methods=['POST'])
@jwt_required()
def calon_ibu_prediction():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User tidak ditemukan"}), 404

        data = request.get_json()
        usia = data.get('usia')
        riwayat_gizi = data.get('riwayat_gizi')
        konsumsi_gizi = data.get('konsumsi_gizi')
        cek_kesehatan = data.get('cek_kesehatan')
        riwayat_stunting = data.get('riwayat_stunting')
        pendidikan = data.get('pendidikan')
        pola_asuh = data.get('pola_asuh')
        ekonomi = data.get('ekonomi')
        tinggi_badan = data.get('tinggi_badan')
        berat_badan = data.get('berat_badan')

        if not usia or not tinggi_badan or not berat_badan:
            return jsonify({"error": "Usia, tinggi badan, dan berat badan wajib diisi"}), 400

        try:
            tinggi_badan = float(tinggi_badan)
            berat_badan = float(berat_badan)
            usia = int(usia)
            if tinggi_badan <= 0 or berat_badan <= 0 or usia <= 0:
                return jsonify({"error": "Usia, tinggi badan, dan berat badan harus lebih dari 0"}), 400
        except ValueError:
            return jsonify({"error": "Usia, tinggi badan, dan berat badan harus berupa angka"}), 400

        # Hitung BMI
        bmi = berat_badan / ((tinggi_badan / 100) ** 2)
        bmi_category = get_bmi_category(bmi)  # Dapatkan kategori BMI

        # Hitung risiko
        risk_score = 0
        if usia < 20 or usia > 35:
            risk_score += 2
        if riwayat_gizi == 'ya':
            risk_score += 2
        if konsumsi_gizi in ['jarang', 'tidak pernah']:
            risk_score += 2
        if cek_kesehatan == 'tidak':
            risk_score += 2
        if riwayat_stunting == 'tidak':
            risk_score += 2
        if pendidikan == 'tidak sekolah':
            risk_score += 2
        if pola_asuh == 'belum':
            risk_score += 2
        if ekonomi == 'kurang baik':
            risk_score += 2

        # Gabungkan hasil prediksi dengan keterangan BMI
        hasil_prediksi = (
            f"Risiko rendah | BMI: {bmi:.2f} ({bmi_category})"
            if risk_score < 5
            else f"Risiko sedang | BMI: {bmi:.2f} ({bmi_category})"
            if risk_score < 10
            else f"Risiko tinggi | BMI: {bmi:.2f} ({bmi_category})"
        )

        # Simpan ke database
        new_prediction = CalonIbuPrediction(
            id_user=user.id,
            username=user.username,
            usia=usia,
            riwayat_gizi=riwayat_gizi,
            konsumsi_gizi=konsumsi_gizi,
            cek_kesehatan=cek_kesehatan,
            riwayat_stunting=riwayat_stunting,
            pendidikan=pendidikan,
            pola_asuh=pola_asuh,
            ekonomi=ekonomi,
            tinggi_badan=tinggi_badan,
            berat_badan=berat_badan,
            hasil_prediksi=hasil_prediksi  # Simpan hasil prediksi dengan keterangan BMI
        )

        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({
            "message": "Prediksi berhasil disimpan!",
            "hasil_prediksi": hasil_prediksi  # Hasil prediksi dengan keterangan BMI
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Kesalahan database: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Kesalahan: {str(e)}"}), 400


# ✅ Mendapatkan riwayat prediksi
@ibu_bp.route('/history', methods=['GET'])
@jwt_required()
def get_prediction_history():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User tidak ditemukan"}), 404

        # Jika user adalah admin, tampilkan semua data
        if user.role == 'admin':
            predictions = CalonIbuPrediction.query.order_by(CalonIbuPrediction.created_at.desc()).all()
        else:
            # Jika user bukan admin, tampilkan hanya data miliknya
            predictions = CalonIbuPrediction.query.filter_by(id_user=user_id).order_by(CalonIbuPrediction.created_at.desc()).all()

        result = [
            {
                "id_prediction": p.id_prediction,
                "username": p.username,
                "usia": p.usia,
                "tinggi_badan": p.tinggi_badan,
                "berat_badan": p.berat_badan,
                "hasil_prediksi": p.hasil_prediksi,  # Hasil prediksi sudah termasuk keterangan BMI
                "created_at": p.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            for p in predictions
        ]

        return jsonify({"predictions": result}), 200

    except Exception as e:
        return jsonify({"error": f"Kesalahan: {str(e)}"}), 500
    
# ✅ DELETE - Hapus data prediksi calon ibu berdasarkan ID
@ibu_bp.route('/hapus/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ibu(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

    try:
        # Cari data prediksi berdasarkan id_prediction
        prediction = CalonIbuPrediction.query.get(id)
        
        if not prediction:
            return jsonify({"success": False, "message": "Data prediksi tidak ditemukan"}), 404
        
        # Jika bukan admin, hanya bisa menghapus milik sendiri
        if user.role != 'admin' and prediction.id_user != user.id:
            return jsonify({"success": False, "message": "Anda tidak memiliki izin untuk menghapus data ini"}), 403

        db.session.delete(prediction)
        db.session.commit()
        return jsonify({"success": True, "message": "Data prediksi calon ibu berhasil dihapus"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
