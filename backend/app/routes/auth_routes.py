from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

# ✅ REGISTER (Daftar User)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validasi input harus lengkap
    required_fields = ['username', 'password', 'role']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"message": "Semua kolom harus diisi!"}), 400

    # Cek apakah username sudah terdaftar
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"message": "Username sudah digunakan"}), 400

    # Hash password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Simpan user ke database
    new_user = User(
        username=data.get('username'),
        password=hashed_password,
        role=data.get('role')  # Simpan role dari input frontend
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User berhasil didaftarkan"}), 201

# ✅ LOGIN (Masuk)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validasi input (username & password harus diisi)
    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username dan password harus diisi!"}), 400

    user = User.query.filter_by(username=data['username']).first()

    # Periksa password yang di-hash
    if user and bcrypt.check_password_hash(user.password, str(data['password'])):
        user_id = str(user.id)  # Pastikan ID user dikonversi ke string
        access_token = create_access_token(identity=user_id)

        return jsonify({
            "message": "Login berhasil",
            "token": access_token,
            "role": user.role  # Kirim role agar frontend bisa membedakan user/admin
        }), 200

    return jsonify({"message": "Username atau password salah"}), 401
@auth_bp.route('/list', methods=['GET'])
@jwt_required()
def get_user():
    try:
        user_list = User.query.all()
        data = [{"id": user.id, "username": user.username, "role": user.role} for user in user_list]
        return jsonify({"success": True, "data": data}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
# ✅ PROFILE (Hanya Bisa Diakses User yang Login)
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))  # Ubah kembali ke integer untuk query
    if not user:
        return jsonify({"message": "User tidak ditemukan"}), 404

    return jsonify({
        "username": user.username,
        "role": user.role
    }), 200
