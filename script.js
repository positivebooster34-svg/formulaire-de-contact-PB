// Attendre que le DOM soit chargé
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prospectForm');
    const preferencesTel = document.getElementById('preferencesTel');
    const contactMail = document.getElementById('contactMail');
    const contactTel = document.getElementById('contactTel');
    const contactIndifferent = document.getElementById('contactIndifferent');
    const successMessage = document.getElementById('successMessage');

    // Gestion de l'affichage conditionnel des préférences téléphoniques
    function togglePreferencesTel() {
        if (contactTel.checked || contactIndifferent.checked) {
            preferencesTel.classList.remove('hidden');
        } else {
            preferencesTel.classList.add('hidden');
            // Réinitialiser les champs quand on cache la section
            const checkboxes = preferencesTel.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(cb => cb.checked = false);
            document.getElementById('trancheHoraire').value = '';
        }
    }

    // Écouter les changements sur les boutons radio de préférence de contact
    contactMail.addEventListener('change', togglePreferencesTel);
    contactTel.addEventListener('change', togglePreferencesTel);
    contactIndifferent.addEventListener('change', togglePreferencesTel);

    // Initialiser l'état au chargement
    togglePreferencesTel();

    // Validation personnalisée
    const validators = {
        nom: {
            element: document.getElementById('nom'),
            errorElement: document.getElementById('nom-error'),
            validate: function(value) {
                if (!value.trim()) return 'Le nom est obligatoire.';
                if (value.trim().length < 2) return 'Le nom doit contenir au moins 2 caractères.';
                if (value.trim().length > 50) return 'Le nom ne peut pas dépasser 50 caractères.';
                if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(value.trim())) return 'Le nom ne peut contenir que des lettres, espaces, tirets et apostrophes.';
                return '';
            }
        },
        prenom: {
            element: document.getElementById('prenom'),
            errorElement: document.getElementById('prenom-error'),
            validate: function(value) {
                if (!value.trim()) return 'Le prénom est obligatoire.';
                if (value.trim().length < 2) return 'Le prénom doit contenir au moins 2 caractères.';
                if (value.trim().length > 50) return 'Le prénom ne peut pas dépasser 50 caractères.';
                if (!/^[a-zA-ZÀ-ÿ\s\-']+$/.test(value.trim())) return 'Le prénom ne peut contenir que des lettres, espaces, tirets et apostrophes.';
                return '';
            }
        },
        tel: {
            element: document.getElementById('tel'),
            errorElement: document.getElementById('tel-error'),
            validate: function(value) {
                if (!value.trim()) return 'Le téléphone est obligatoire.';
                // Pattern pour numéros français
                const telPattern = /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/;
                if (!telPattern.test(value.trim())) return 'Veuillez saisir un numéro de téléphone français valide.';
                return '';
            }
        },
        email: {
            element: document.getElementById('email'),
            errorElement: document.getElementById('email-error'),
            validate: function(value) {
                if (!value.trim()) return 'L\'email est obligatoire.';
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(value.trim())) return 'Veuillez saisir une adresse email valide.';
                if (value.length > 100) return 'L\'email ne peut pas dépasser 100 caractères.';
                return '';
            }
        }
    };

    // Validation en temps réel
    Object.keys(validators).forEach(fieldName => {
        const validator = validators[fieldName];
        validator.element.addEventListener('blur', function() {
            validateField(fieldName);
        });
        validator.element.addEventListener('input', function() {
            // Effacer l'erreur pendant la saisie
            if (validator.errorElement.textContent) {
                validator.errorElement.textContent = '';
                validator.element.style.borderColor = '';
            }
        });
    });

    function validateField(fieldName) {
        const validator = validators[fieldName];
        const value = validator.element.value;
        const error = validator.validate(value);
        
        validator.errorElement.textContent = error;
        if (error) {
            validator.element.style.borderColor = '#e53e3e';
            return false;
        } else {
            validator.element.style.borderColor = '#38a169';
            return true;
        }
    }

    // Validation des préférences de contact
    function validatePreferenceContact() {
        const preferenceError = document.getElementById('preference-error');
        const isSelected = contactMail.checked || contactTel.checked || contactIndifferent.checked;
        
        if (!isSelected) {
            preferenceError.textContent = 'Veuillez choisir une préférence de contact.';
            return false;
        } else {
            preferenceError.textContent = '';
            return true;
        }
    }

    // Validation du consentement RGPD
    function validateConsent() {
        const consentCheckbox = document.getElementById('consentementRGPD');
        const consentError = document.getElementById('consent-error');
        
        if (!consentCheckbox.checked) {
            consentError.textContent = 'Vous devez accepter le traitement de vos données personnelles.';
            return false;
        } else {
            consentError.textContent = '';
            return true;
        }
    }

    // Écouter les changements sur les boutons radio de préférence
    contactMail.addEventListener('change', function() {
        if (this.checked) validatePreferenceContact();
        toggleSpamWarning();
    });
    contactTel.addEventListener('change', function() {
        if (this.checked) validatePreferenceContact();
        toggleSpamWarning();
    });
    contactIndifferent.addEventListener('change', function() {
        if (this.checked) validatePreferenceContact();
        toggleSpamWarning();
    });

    // Écouter les changements sur la case de consentement
    document.getElementById('consentementRGPD').addEventListener('change', validateConsent);

    // Gestion de la soumission du formulaire
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Valider tous les champs
        let isValid = true;
        
        // Validation des champs de base
        Object.keys(validators).forEach(fieldName => {
            if (!validateField(fieldName)) {
                isValid = false;
            }
        });
        
        // Validation des préférences de contact
        if (!validatePreferenceContact()) {
            isValid = false;
        }
        
        // Validation du consentement
        if (!validateConsent()) {
            isValid = false;
        }
        
        if (isValid) {
            // Simuler l'envoi du formulaire
            submitForm();
        } else {
            // Faire défiler vers la première erreur
            const firstError = document.querySelector('.error-message:not(:empty)');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

    function submitForm() {
        const submitBtn = document.querySelector('.btn-submit');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Envoi en cours...';
        
        const formData = new FormData(form);
        const data = {};
        // Convertir les données du formulaire en objet JSON
        for (let [key, value] of formData.entries()) {
            if (data[key]) {
                // Gérer les cases à cocher multiples (jours de préférence)
                if (Array.isArray(data[key])) {
                    data[key].push(value);
                } else {
                    data[key] = [data[key], value];
                }
            } else {
                data[key] = value;
            }
        }
        
        // S'assurer que les jours de préférence sont un tableau même s'il n'y a qu'un seul jour
        if (data.joursPreference && !Array.isArray(data.joursPreference)) {
            data.joursPreference = [data.joursPreference];
        } else if (!data.joursPreference) {
            data.joursPreference = [];
        }

        fetch('/api/prospects', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                // Si la réponse n'est pas OK (statut 4xx ou 5xx)
                return response.json().then(err => { throw new Error(err.message || 'Erreur lors de l\'envoi du formulaire.'); });
            }
            return response.json();
        })
        .then(result => {
            console.log('Succès:', result);
            // Masquer le formulaire et afficher le message de succès
            form.style.display = 'none';
            successMessage.classList.remove('hidden');
            
            // Faire défiler vers le message de succès
            successMessage.scrollIntoView({ behavior: 'smooth' });
        })
        .catch(error => {
            console.error('Erreur:', error);
            // Afficher le message d'erreur à l'utilisateur
            alert('Une erreur est survenue lors de l\'envoi : ' + error.message);
            // Réactiver le bouton de soumission
            submitBtn.disabled = false;
            submitBtn.textContent = 'Envoyer ma demande';
        });
    }

    // Ajout de la fonction pour afficher l'avertissement spam
    function toggleSpamWarning() {
        const spamWarning = document.getElementById('spamWarning');
        if (contactMail.checked) {
            spamWarning.classList.remove('hidden');
        } else {
            spamWarning.classList.add('hidden');
        }
    }

    // Initialisation de l'avertissement spam
    const spamWarningContainer = document.createElement('div');
    spamWarningContainer.id = 'spamWarning';
    spamWarningContainer.classList.add('spam-warning', 'hidden');
    spamWarningContainer.innerHTML = '<p>⚠️ Pensez à vérifier vos courriers indésirables/spams !</p>';
    
    // Trouver l'endroit où insérer l'avertissement (après les préférences de contact)
    const preferencesSection = document.querySelector('.preferences');
    if (preferencesSection) {
        preferencesSection.appendChild(spamWarningContainer);
    }
    
    // Initialiser l'état de l'avertissement spam
    toggleSpamWarning();

    // Améliorer l'accessibilité
    form.addEventListener('keydown', function(e) {
        // Permettre la soumission avec Ctrl+Enter
        if (e.ctrlKey && e.key === 'Enter') {
            form.dispatchEvent(new Event('submit'));
        }
    });
});

