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
    
    # Configuration SendGrid
    app.config['SENDGRID_API_KEY'] = os.environ.get('SENDGRID_API_KEY')
    
    # Activer CORS pour permettre les requêtes depuis le frontend
    CORS(app)
    
    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    # ✅ Enregistrement des blueprints UNE SEULE FOIS
    from src.routes.user import user_bp
    from src.routes.prospect import prospect_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(prospect_bp, url_prefix='/api')
    
    # Route de test
    @app.route('/test-email')
    def test_email():
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        
        try:
            # Vérifier que la clé existe
            api_key = app.config.get('SENDGRID_API_KEY')
            if not api_key:
                return "❌ SENDGRID_API_KEY n'est pas configurée"
            
            if not api_key.startswith('SG.'):
                return f"❌ La clé API ne semble pas valide : {api_key[:10]}..."
            
            message = Mail(
                from_email='positivebooster34@gmail.com',
                to_emails='positivebooster34@gmail.com',
                subject='[TEST] Email de test depuis Render',
                plain_text_content='Ceci est un test SendGrid depuis Render !'
            )
            
            sg = SendGridAPIClient(api_key)
            response = sg.send(message)
            return f"✅ Email envoyé avec succès ! Status: {response.status_code}"
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            return f"❌ Erreur : {type(e).__name__} - {str(e)}<br><br>Détails:<br><pre>{error_detail}</pre>"
    
    # Route serve    
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
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)