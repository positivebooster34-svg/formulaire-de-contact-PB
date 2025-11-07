import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.extensions import mail

def create_app():
    app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
    app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

    # Configuration de Flask-Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'positivebooster34@gmail.com'
    app.config['MAIL_PASSWORD'] = 'hyhrslqgejefulcf'
    app.config['MAIL_DEFAULT_SENDER'] = 'positivebooster34@gmail.com'

    mail.init_app(app)

    # Activer CORS pour permettre les requêtes depuis le frontend
    CORS(app)

    from src.routes.user import user_bp
    from src.routes.prospect import prospect_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(prospect_bp, url_prefix='/api')

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        static_folder_path = app.static_folder
        if static_folder_path is None:
                return "Static folder not configured", 404

        if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
            return send_from_directory(static_folder_path, path)
        else:
            index_path = os.path.join(static_folder_path, 'formulaire_prospect.html')
            if os.path.exists(index_path):
                return send_from_directory(static_folder_path, 'formulaire_prospect.html')
            else:
                return "formulaire_prospect.html not found", 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

