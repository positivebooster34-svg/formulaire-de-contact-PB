from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Utiliser l'instance db du modèle user
from src.models.user import db

class Prospect(db.Model):
    """Modèle pour stocker les données des prospects conformément au RGPD"""
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Coordonnées de base
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    
    # Préférences de contact
    preference_contact = db.Column(db.String(15), nullable=False)  # 'mail', 'tel' ou 'indifferent'
    jours_preference = db.Column(db.Text)  # JSON array des jours
    tranche_horaire = db.Column(db.String(20))  # 'matin', 'midi', 'apresmidi', 'soiree', 'autre'
    autre_horaire = db.Column(db.String(100)) # Champ libre pour les préférences horaires
    
    # Consentements RGPD
    consentement_rgpd = db.Column(db.Boolean, nullable=False, default=False)
    consentement_marketing = db.Column(db.Boolean, nullable=False, default=False)
    
    # Métadonnées
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modification = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # Support IPv6
    user_agent = db.Column(db.Text)
    
    # Statut du prospect
    statut = db.Column(db.String(20), nullable=False, default='nouveau')  # nouveau, contacte, converti, supprime
    
    def __repr__(self):
        return f'<Prospect {self.prenom} {self.nom} - {self.email}>'
    
    def set_jours_preference(self, jours_list):
        """Convertit une liste de jours en JSON pour le stockage"""
        if jours_list:
            self.jours_preference = json.dumps(jours_list)
        else:
            self.jours_preference = None
    
    def get_jours_preference(self):
        """Récupère la liste des jours depuis le JSON"""
        if self.jours_preference:
            return json.loads(self.jours_preference)
        return []
    
    def to_dict(self):
        """Convertit l'objet en dictionnaire pour l'API"""
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'telephone': self.telephone,
            'email': self.email,
            'preference_contact': self.preference_contact,
            'jours_preference': self.get_jours_preference(),
            'tranche_horaire': self.tranche_horaire,
            'autre_horaire': self.autre_horaire,
            'consentement_rgpd': self.consentement_rgpd,
            'consentement_marketing': self.consentement_marketing,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_modification': self.date_modification.isoformat() if self.date_modification else None,
            'statut': self.statut
        }
    
    def to_dict_anonymized(self):
        """Version anonymisée pour les logs ou exports"""
        return {
            'id': self.id,
            'nom': self.nom[:1] + '*' * (len(self.nom) - 1),
            'prenom': self.prenom[:1] + '*' * (len(self.prenom) - 1),
            'telephone': self.telephone[:2] + '*' * (len(self.telephone) - 4) + self.telephone[-2:],
            'email': self.email.split('@')[0][:2] + '*' * (len(self.email.split('@')[0]) - 2) + '@' + self.email.split('@')[1],
            'preference_contact': self.preference_contact,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'statut': self.statut
        }


class ProspectLog(db.Model):
    """Modèle pour tracer les actions sur les prospects (conformité RGPD)"""
    
    id = db.Column(db.Integer, primary_key=True)
    prospect_id = db.Column(db.Integer, db.ForeignKey('prospect.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)  # creation, modification, consultation, suppression
    details = db.Column(db.Text)  # Détails de l'action en JSON
    date_action = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    utilisateur = db.Column(db.String(100))  # Qui a effectué l'action
    
    def __repr__(self):
        return f'<ProspectLog {self.prospect_id} - {self.action} - {self.date_action}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'prospect_id': self.prospect_id,
            'action': self.action,
            'details': json.loads(self.details) if self.details else None,
            'date_action': self.date_action.isoformat(),
            'utilisateur': self.utilisateur
        }

