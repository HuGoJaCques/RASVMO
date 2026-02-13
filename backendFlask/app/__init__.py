import os
from flask import Flask, request, jsonify

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text
from flask_cors import CORS

from app.config import DevelopmentConfig, ProductionConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
   
    CORS(app, origins=app.config['CORS_ORIGINS'])

    db.init_app(app)
    migrate.init_app(app, db)

    #Import des routes
    from app.routes.routine import bp as routine_bp
    app.register_blueprint(routine_bp)
    
    from app.routes.frequence import bp as frequence_bp
    app.register_blueprint(frequence_bp)

    from app.routes.routine_jour import bp as routine_jour_bp
    app.register_blueprint(routine_jour_bp)

    from app.routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from app.routes.routine_log import bp as routine_log_bp
    app.register_blueprint(routine_log_bp)
    
    return app
