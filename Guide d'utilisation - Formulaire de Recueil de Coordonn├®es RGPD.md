# Guide d'utilisation - Formulaire de Recueil de Coordonnées RGPD

## Vue d'ensemble

Ce formulaire de contact a été conçu pour être entièrement conforme au Règlement Général sur la Protection des Données (RGPD). Il collecte les coordonnées des prospects tout en respectant leurs droits et en obtenant leur consentement éclairé.

## Fonctionnalités principales

### 1. Collecte des coordonnées
- **Nom et prénom** : Champs obligatoires avec validation (2-50 caractères, lettres uniquement)
- **Téléphone** : Validation pour numéros français (format 01 23 45 67 89)
- **Email** : Validation d'adresse email avec limite de 100 caractères

### 2. Préférences de contact
- **Choix du mode de contact** : Email ou téléphone (obligatoire)
- **Options téléphoniques** (affichage conditionnel) :
  - Sélection des jours de préférence (lundi à vendredi)
  - Choix de la tranche horaire (matin, après-midi, soirée)

### 3. Conformité RGPD

#### Informations transparentes
Le formulaire inclut toutes les informations requises par le RGPD :
- **Finalité du traitement** : Recontacter concernant les services
- **Base légale** : Consentement libre et éclairé
- **Droits des personnes** : Accès, rectification, effacement, portabilité, limitation, opposition
- **Conservation des données** : 3 ans maximum
- **Contact pour exercer les droits** : contact@entreprise.com

#### Consentement
- **Case obligatoire** : Consentement au traitement des données personnelles
- **Case optionnelle** : Consentement pour recevoir des informations commerciales
- **Consentement libre** : Aucune case n'est pré-cochée
- **Consentement éclairé** : Toutes les informations sont fournies avant le consentement

## Validation et sécurité

### Validation côté client
- **Validation en temps réel** : Bordures colorées (vert = valide, rouge = erreur)
- **Messages d'erreur** : Affichage des erreurs spécifiques à chaque champ
- **Validation JavaScript** : Contrôles personnalisés pour chaque type de donnée

### Sécurité
- **Validation côté serveur** : À implémenter lors de l'intégration
- **Protection CSRF** : À ajouter lors de l'intégration
- **Chiffrement HTTPS** : Recommandé pour la transmission des données

## Intégration technique

### Fichiers fournis
1. **formulaire_prospect.html** : Structure HTML complète
2. **style.css** : Styles responsive et accessibles
3. **script.js** : Logique de validation et interactivité

### Responsive design
- Compatible desktop et mobile
- Adaptation automatique des tailles d'écran
- Interface tactile optimisée

### Accessibilité
- Labels associés aux champs
- Messages d'erreur avec attributs ARIA
- Navigation au clavier supportée
- Contraste suffisant pour la lisibilité

## Points d'attention pour l'intégration

### 1. Traitement des données
- Implémenter le traitement côté serveur (PHP, Node.js, Python, etc.)
- Stocker les données de manière sécurisée
- Mettre en place les logs d'accès et de modification

### 2. Politique de confidentialité
- Créer une page "politique-confidentialite.html" détaillée
- Mettre à jour le lien dans le formulaire
- Maintenir la politique à jour selon les évolutions légales

### 3. Gestion des droits RGPD
- Mettre en place un système pour traiter les demandes d'exercice de droits
- Prévoir les procédures de suppression, rectification, portabilité
- Former les équipes sur les obligations RGPD

### 4. Conservation des données
- Implémenter la suppression automatique après 3 ans
- Mettre en place des rappels pour le nettoyage des données
- Documenter les traitements dans le registre RGPD

## Recommandations d'utilisation

### 1. Formation des équipes
- Former les commerciaux sur l'utilisation des données collectées
- Sensibiliser sur les limites du consentement obtenu
- Établir des procédures claires de recontact

### 2. Suivi et amélioration
- Analyser les taux de conversion du formulaire
- Recueillir les retours utilisateurs
- Adapter le formulaire selon les besoins métier

### 3. Veille juridique
- Suivre les évolutions de la réglementation RGPD
- Adapter le formulaire aux nouvelles exigences
- Consulter un juriste spécialisé si nécessaire

## Support technique

Pour toute question technique sur l'implémentation ou l'adaptation du formulaire, n'hésitez pas à nous contacter. Le code est documenté et modulaire pour faciliter les modifications futures.

## Conformité légale

Ce formulaire respecte les exigences du RGPD en vigueur au moment de sa création. Il est recommandé de faire valider la conformité par un Data Protection Officer (DPO) ou un juriste spécialisé avant la mise en production.

