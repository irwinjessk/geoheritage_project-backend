/**
 * GeoHeritage - Base JavaScript
 * Fonctionnalités communes pour toute l'application
 */

class GeoHeritageBase {
    constructor() {
        this.init();
    }

    init() {
        // Initialisation sera ajoutée plus tard
    }
}

// Initialiser quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    window.geoHeritageBase = new GeoHeritageBase();
});

// Exporter pour utilisation globale
window.GeoHeritageBase = GeoHeritageBase;
