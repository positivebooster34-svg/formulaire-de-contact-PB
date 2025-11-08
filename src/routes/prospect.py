from flask import Blueprint, request, jsonify, current_app
from src.models.prospect import Prospect
from src.models.user import db
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

prospect_bp = Blueprint('prospect_routes', __name__)

def send_prospect_email(data):
    """Envoie un email de notification pour un nouveau prospect via SendGrid."""
    
    # Construction du corps de l'email
    body = f"""
    Nouveau prospect enregistré !
    
    Nom: {data.get('nom')}
    Prénom: {data.get('prenom')}
    Téléphone: {data.get('tel')}
    Email: {data.get('email')}
    
    Préférence de contact: {data.get('preferenceContact')}
    """
    
    if data.get('preferenceContact') in ['tel', 'indifferent']:
        jours = ', '.join(data.get('joursPreference', []))
        body += f"""
    Jours de préférence: {jours if jours else 'Non spécifié'}
    Tranche horaire: {data.get('trancheHoraire', 'Non spécifié')}
    """
    
    body += f"""
    Consentement RGPD: {'Oui' if data.get('consentementRGPD') else 'Non'}
    Consentement Marketing: {'Oui' if data.get('consentementMarketing') else 'Non'}
    """
    
     message = Mail(
        from_email='positivebooster34@gmail.com',
        to_emails='positivebooster34@gmail.com',
        subject="[Nouveau Prospect RGPD] " + data.get('prenom') + " " + data.get('nom'),
        plain_text_content=body
    )
    
    try:
        sg = SendGridAPIClient(current_app.config.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email envoyé ! Status code: {response.status_code}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {e}")
        return False

@prospect_bp.route('/prospects', methods=['POST'])
def submit_prospect():
    try:
        data = request.get_json()
        
        # 1. Validation des données
        required_fields = ['nom', 'prenom', 'tel', 'email', 'preferenceContact', 'consentementRGPD']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Champ manquant: {field}"}), 400

        # 2. Enregistrement dans la base de données
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        
        # Gestion des jours de préférence
        jours_preference = data.get('joursPreference', [])
        if not isinstance(jours_preference, list):
            jours_preference = [jours_preference]

        new_prospect = Prospect(
            nom=data['nom'],
            prenom=data['prenom'],
            telephone=data['tel'],
            email=data['email'],
            preference_contact=data['preferenceContact'],
            jours_preference=json.dumps(jours_preference),
            tranche_horaire=data.get('trancheHoraire'),
            consentement_rgpd=bool(data.get('consentementRGPD')),
            consentement_marketing=bool(data.get('consentementMarketing')),
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.session.add(new_prospect)
        db.session.commit()
        
        # 3. Envoi de l'email de notification
        email_sent = send_prospect_email(data)
        
        if not email_sent:
             print(f"Avertissement: Email de notification échoué pour le prospect {new_prospect.id}.")
            
        return jsonify({"message": "Formulaire soumis avec succès et prospect enregistré.", "email_notification": "succès" if email_sent else "échec"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Erreur serveur lors de la soumission: {e}")
        return jsonify({"message": "Erreur interne du serveur lors de la soumission du formulaire."}), 500


