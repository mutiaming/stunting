from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Anak

anak_bp = Blueprint('anak', __name__)

# CREATE - Tambah Anak
@anak_bp.route('/tambah', methods=['POST'])
@jwt_required()
def add_anak():
    data = request.json
    nik = data.get('nik')
    nama_anak = data.get('nama_anak')
    nama_orang_tua = data.get('nama_orang_tua')

    if not nik or not nama_anak or not nama_orang_tua:
        return jsonify({"success": False, "message": "Semua kolom wajib diisi!"}), 400
    
    # Cek apakah NIK sudah ada
    existing_anak = Anak.query.filter_by(nik=nik).first()
    if existing_anak:
        return jsonify({"success": False, "message": "NIK sudah terdaftar!"}), 400

    try:
        anak_baru = Anak(nik=nik, nama_anak=nama_anak, nama_orang_tua=nama_orang_tua)
        db.session.add(anak_baru)
        db.session.commit()
        return jsonify({"success": True, "message": "Anak berhasil ditambahkan"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# READ - Lihat daftar anak
@anak_bp.route('/list', methods=['GET'])
@jwt_required()
def get_anak():
    try:
        anak_list = Anak.query.all()
        data = [{"id": anak.id, "nik": anak.nik, "nama_anak": anak.nama_anak, "nama_orang_tua": anak.nama_orang_tua} for anak in anak_list]
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# UPDATE - Edit data anak
@anak_bp.route('/edit/<int:id>', methods=['PUT'])
@jwt_required()
def update_anak(id):
    data = request.json
    anak = Anak.query.get(id)

    if not anak:
        return jsonify({"success": False, "message": "Anak tidak ditemukan"}), 404

    try:
        anak.nik = data.get('nik', anak.nik)
        anak.nama_anak = data.get('nama_anak', anak.nama_anak)
        anak.nama_orang_tua = data.get('nama_orang_tua', anak.nama_orang_tua)
        
        db.session.commit()
        return jsonify({"success": True, "message": "Data anak berhasil diperbarui"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

# DELETE - Hapus data anak
@anak_bp.route('/hapus/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_anak(id):
    anak = Anak.query.get(id)
    
    if not anak:
        return jsonify({"success": False, "message": "Anak tidak ditemukan"}), 404
    
    try:
        db.session.delete(anak)
        db.session.commit()
        return jsonify({"success": True, "message": "Data anak berhasil dihapus"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
