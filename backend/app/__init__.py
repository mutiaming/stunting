from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import pymysql
from flask_migrate import Migrate
from config import Config

pymysql.install_as_MySQLdb()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    # Configure CORS
    cors.init_app(
        app,
        resources={r"/*": {"origins": app.config['ALLOWED_ORIGINS']}},
        supports_credentials=True
    )

    # Register blueprints
    from app.main import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.stunting_routes import stunting_bp
    from app.routes.ibu_routes import ibu_bp
    from app.routes.mpasi_routes import mpasi_bp
    from app.routes.anak_routes import anak_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(stunting_bp, url_prefix='/stunting')
    app.register_blueprint(ibu_bp, url_prefix='/ibu')
    app.register_blueprint(mpasi_bp, url_prefix="/mpasi")
    app.register_blueprint(anak_bp, url_prefix="/anak")

    return app