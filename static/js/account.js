/**
 * GeoHeritage - Account JavaScript
 * Fonctionnalités spécifiques aux comptes utilisateurs
 */

class GeoHeritageAccount {
    constructor() {
        this.init();
    }

    init() {
        // Initialisation sera ajoutée plus tard
    }
}

// Initialiser quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.account-form') || document.querySelector('.user-sidebar')) {
        window.geoHeritageAccount = new GeoHeritageAccount();
    }
});

// Exporter pour utilisation globale
window.GeoHeritageAccount = GeoHeritageAccount;
