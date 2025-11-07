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

    @app.route('/test-email')
    def test_email():
        from src.routes.prospect import send_prospect_email
        data_test = {
            "nom": "Test",
            "prenom": "Email",
            "tel": "0000000000",
            "email": "test@example.com",
            "preferenceContact": "indifferent",
            "joursPreference": ["Lundi", "Mardi"],
            "trancheHoraire": "Matin",
            "consentementRGPD": True,
            "consentementMarketing": False
        }
        success = send_prospect_email(data_test)
        if success:
            return "✅ Email envoyé avec succès !"
        else:
            return "❌ Échec de l'envoi de l'email."
    
    return app   

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

