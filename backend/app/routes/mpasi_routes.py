from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import MPASI, User

mpasi_bp = Blueprint('mpasi', __name__)

# ✅ Fungsi untuk cek apakah user adalah admin
def is_admin():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user and user.role == "admin"

# ✅ 1. Tambah MPASI (Admin Only)
@mpasi_bp.route('/add', methods=['POST'])
@jwt_required()
def tambah_mpasi():
    if not is_admin():
        return jsonify({"message": "Akses ditolak, hanya admin yang bisa menambah MPASI!"}), 403

    data = request.get_json()
    try:
        new_mpasi = MPASI(
            nama_makanan=data['nama_makanan'],
            usia_minimum=data['usia_minimum'],
            deskripsi=data['deskripsi']
        )
        db.session.add(new_mpasi)
        db.session.commit()

        return jsonify({"message": "MPASI berhasil ditambahkan!"}), 201
    except Exception as e:
        return jsonify({"message": "Gagal menambahkan MPASI", "error": str(e)}), 500

# ✅ 2. Tampilkan semua MPASI atau berdasarkan usia minimum
@mpasi_bp.route('/list', methods=['GET'])
def get_mpasi():
    usia = request.args.get('usia', type=int)

    if usia is not None:
        rekomendasi = MPASI.query.filter(MPASI.usia_minimum <= usia).all()
    else:
        rekomendasi = MPASI.query.all()

    if not rekomendasi:
        return jsonify({"message": "Tidak ada data MPASI yang tersedia"}), 404

    result = [
        {
            "id": m.id,
            "nama_makanan": m.nama_makanan,
            "usia_minimum": m.usia_minimum,
            "deskripsi": m.deskripsi
        }
        for m in rekomendasi
    ]

    return jsonify(result), 200

# ✅ 3. Edit MPASI (Admin Only)
@mpasi_bp.route('/edit/<int:id>', methods=['PUT'])
@jwt_required()
def update_mpasi(id):
    if not is_admin():
        return jsonify({"message": "Akses ditolak, hanya admin yang bisa mengedit MPASI!"}), 403

    data = request.get_json()
    mpasi = MPASI.query.get(id)

    if not mpasi:
        return jsonify({"message": "MPASI tidak ditemukan"}), 404

    mpasi.nama_makanan = data.get('nama_makanan', mpasi.nama_makanan)
    mpasi.usia_minimum = data.get('usia_minimum', mpasi.usia_minimum)
    mpasi.deskripsi = data.get('deskripsi', mpasi.deskripsi)

    db.session.commit()
    return jsonify({"message": "MPASI berhasil diperbarui"}), 200

# ✅ 4. Hapus MPASI (Admin Only)
@mpasi_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_mpasi(id):
    if not is_admin():
        return jsonify({"message": "Akses ditolak, hanya admin yang bisa menghapus MPASI!"}), 403

    mpasi = MPASI.query.get(id)

    if not mpasi:
        return jsonify({"message": "MPASI tidak ditemukan"}), 404

    db.session.delete(mpasi)
    db.session.commit()
    return jsonify({"message": "MPASI berhasil dihapus"}), 200
