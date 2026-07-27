// Récupérer les données JSON depuis le HTML
var parcelles = JSON.parse(document.getElementById('parcelles-data').textContent);

// Créer la carte
var map = L.map('map').setView([6.116, 1.274], 13);

// Fond OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Variable globale
var parcellesLayer;

// Couleur selon statut
function getColor(statut) {
    switch(statut) {
        case 'en_attente': return 'red';
        case 'en_cours': return 'orange';
        case 'rembourse': return 'green';
        default: return 'gray';
    }
}

// Style
function styleFeature(feature) {
    return {
        color: getColor(feature.properties.statut),
        weight: 2,
        fillOpacity: 0.4
    };
}

// Popup
function onEachFeature(feature, layer) {
    var p = feature.properties;

    // 📄 Documents
    var docsHtml = "";

    if (p.documents && p.documents.length > 0) {
        docsHtml += "<b>Documents:</b><br>";

        p.documents.forEach(function(doc) {
            docsHtml += `
                <a href="${doc.url}" target="_blank">📄 ${doc.type}</a><br>
            `;
        });
    } else {
        docsHtml += "<b>Documents:</b> Aucun<br>";
    }

    // 🔗 Lien vers enrichissement
    var enrichLink = `
        <br><br>
        <a href="/parcelle/${p.id}/enrichir/" target="_blank" 
           style="color:white; background:#007bff; padding:5px 10px; text-decoration:none; border-radius:4px;">
           ⚙️ Enrichir cette parcelle
        </a>
    `;

    // Popup complet
    var popupContent = `
        <b>Titre:</b> ${p.titre}<br>
        <b>Propriétaires:</b> ${p.proprietaires}<br>
        <b>Statut:</b> ${p.statut}<br>
        <b>Montant total:</b> ${p.montant_total} FCFA<br>
        <b>Payé:</b> ${p.total_paye} FCFA<br>
        <b>Reste:</b> ${p.reste} FCFA<br>
        <b>Année fin:</b> ${p.date_fin}<br>
        ${docsHtml}
        ${enrichLink}
    `;

    layer.bindPopup(popupContent);
}

// Ajouter les parcelles
parcellesLayer = L.geoJSON(parcelles, {
    style: styleFeature,
    onEachFeature: onEachFeature
}).addTo(map);

// 🔍 Fonction de recherche
window.searchParcelle = function() {
    var searchValue = document.getElementById("search").value.toLowerCase();

    parcellesLayer.eachLayer(function(layer) {
        var titre = (layer.feature.properties.titre || "").toLowerCase();

        if (titre.includes(searchValue)) {
            map.fitBounds(layer.getBounds());
            layer.openPopup();
        }
    });
};

document.addEventListener("DOMContentLoaded", function () {

    const userMenuButton =
        document.getElementById("userMenuButton");

    const userDropdown =
        document.getElementById("userDropdown");


    if (userMenuButton && userDropdown) {

        userMenuButton.addEventListener(
            "click",
            function (event) {

                event.stopPropagation();

                userDropdown.classList.toggle("show");

            }
        );


        // Fermer le menu en cliquant ailleurs
        document.addEventListener(
            "click",
            function () {

                userDropdown.classList.remove("show");

            }
        );

    }

});