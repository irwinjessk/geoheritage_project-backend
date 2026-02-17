/**
 * GeoHeritage - Heritage JavaScript
 * Fonctionnalités pour les sites patrimoniaux
 */

class GeoHeritageHeritage {
    constructor() {
        this.init();
    }

    init() {
        // Initialisation sera ajoutée plus tard
    }
}

// Initialiser quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.heritage-card') || document.querySelector('#heritage-map')) {
        window.geoHeritageHeritage = new GeoHeritageHeritage();
    }
});

// Exporter pour utilisation globale
window.GeoHeritageHeritage = GeoHeritageHeritage;
