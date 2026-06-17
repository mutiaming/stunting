import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'db_stunting')

    SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"  )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')

    ALLOWED_ORIGINS = os.getenv(
        'ALLOWED_ORIGINS',
        'https://growtrack.harkatnegeri.ac.id'
    ).split(',')

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:@localhost/db_stunting')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwtsecret')

#     # ✅ Tambahkan baris ini:
#     ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
