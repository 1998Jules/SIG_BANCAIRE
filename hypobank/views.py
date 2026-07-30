from django.shortcuts import render
from .models import Parcelle, ParcelleProprietaire, Paiement
import json
from django.db.models import Sum
from .models import Document

from django.shortcuts import render, get_object_or_404, redirect
from .models import Parcelle, ParcelleProprietaire, Paiement, Document
from django.db.models import Sum
import json
from django.contrib.auth.decorators import login_required


#@login_required
def index(request):
    parcelles = []

    for parcelle in Parcelle.objects.all():

        # --- Propriétaires ---
        proprietaires_qs = ParcelleProprietaire.objects.filter(parcelle=parcelle)
        noms_prop = []

        for pp in proprietaires_qs:
            if pp.proprietaire.type == 'physique':
                noms_prop.append(f"{pp.proprietaire.nom} {pp.proprietaire.prenom}")
            else:
                noms_prop.append(pp.proprietaire.raison_sociale)

        # --- Titre ---
        titre = parcelle.titrefoncier_set.first()
        numero_titre = titre.numero_titre if titre else 'N/A'

        # --- Valeurs par défaut (IMPORTANT) ---
        total_paye = 0
        montant_total = 0
        reste = 0
        statut = "Aucune hypothèque"
        date_fin = "N/A"

        # --- Hypothèque ---
        if titre:
            hypotheque = titre.hypotheque_set.first()

            if hypotheque:
                total_paye = Paiement.objects.filter(
                    hypotheque=hypotheque
                ).aggregate(Sum('montant'))['montant__sum'] or 0

                montant_total = hypotheque.montant
                reste = montant_total - total_paye
                statut = hypotheque.statut_remboursement
                date_fin = hypotheque.date_fin.strftime("%Y") if hypotheque.date_fin else "N/A"

        # --- Documents ---
        documents = []
        if titre:
            docs_qs = Document.objects.filter(titre=titre)
            for doc in docs_qs:
                documents.append({
                    "url": doc.fichier.url,
                    "type": doc.type_document
                })

        # --- GeoJSON ---
        geom_obj = json.loads(parcelle.geom.geojson)

        parcelles.append({
            "type": "Feature",
            "geometry": geom_obj,
            "properties": {
                "id": parcelle.id,  # 🔥 CORRECTION ICI
                "titre": numero_titre,
                "proprietaires": ", ".join(noms_prop),
                "statut": statut,
                "montant_total": montant_total,
                "total_paye": total_paye,
                "documents": documents,
                "reste": reste,
                "date_fin": date_fin
            }
        })

    parcelles_geojson = json.dumps({
        "type": "FeatureCollection",
        "features": parcelles
    })

    return render(request, 'hypobank/index.html', {
        'parcelles_geojson': parcelles_geojson
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Parcelle
from .forms import *

def enrichir_parcelle(request, parcelle_id):
    parcelle = get_object_or_404(Parcelle, id=parcelle_id)

    prop_form = ProprietaireForm()
    titre_form = TitreFoncierForm()
    hyp_form = HypothequeForm()
    pay_form = PaiementForm()
    doc_form = DocumentForm()

    context = {
        'parcelle': parcelle,
        'prop_form': prop_form,
        'titre_form': titre_form,
        'hyp_form': hyp_form,
        'pay_form': pay_form,
        'doc_form': doc_form,
    }

    return render(request, 'hypobank/enrichir_parcelle.html', context)

def ajouter_proprietaire(request, parcelle_id):
    if request.method == 'POST':
        form = ProprietaireForm(request.POST)
        if form.is_valid():
            proprietaire = form.save()

            ParcelleProprietaire.objects.create(
                parcelle_id=parcelle_id,
                proprietaire=proprietaire
            )

    return redirect('enrichir_parcelle', parcelle_id=parcelle_id)

def ajouter_hypotheque(request, titre_id):
    if request.method == 'POST':
        form = HypothequeForm(request.POST)
        if form.is_valid():
            hyp = form.save(commit=False)
            hyp.titre_id = titre_id
            hyp.save()

    return redirect('index')

def ajouter_paiement(request, hypotheque_id):
    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            paiement = form.save(commit=False)
            paiement.hypotheque_id = hypotheque_id
            paiement.save()

    return redirect('index')

def ajouter_document(request, titre_id):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.titre_id = titre_id
            doc.save()

    return redirect('index')
def ajouter_titre(request, parcelle_id):
    if request.method == 'POST':
        form = TitreFoncierForm(request.POST)
        if form.is_valid():
            titre = form.save(commit=False)
            titre.parcelle_id = parcelle_id
            titre.save()

    return redirect('enrichir_parcelle', parcelle_id=parcelle_id)


from django.db.models import Sum
from .models import Parcelle, Proprietaire, TitreFoncier, Hypotheque, Paiement

def dashboard(request):
    parcelles = Parcelle.objects.count()
    proprietaires = Proprietaire.objects.count()
    titres = TitreFoncier.objects.count()
    hypotheques = Hypotheque.objects.count()

    total_montant = Hypotheque.objects.aggregate(Sum('montant'))['montant__sum'] or 0
    total_paye = Paiement.objects.aggregate(Sum('montant'))['montant__sum'] or 0

    en_attente = Hypotheque.objects.filter(statut_remboursement='en_attente').count()
    en_cours = Hypotheque.objects.filter(statut_remboursement='en_cours').count()
    rembourse = Hypotheque.objects.filter(statut_remboursement='rembourse').count()

    context = {
        'parcelles': parcelles,
        'proprietaires': proprietaires,
        'titres': titres,
        'hypotheques': hypotheques,
        'total_montant': total_montant,
        'total_paye': total_paye,
        'reste': total_montant - total_paye,
        'en_attente': en_attente,
        'en_cours': en_cours,
        'rembourse': rembourse,
    }

    return render(request, 'hypobank/dashboard.html', context)