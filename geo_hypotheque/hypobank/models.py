from django.db import models

# Create your models here.
from django.contrib.gis.db import models

# Agent de levé
class AgentLeve(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)
    structure = models.CharField(max_length=150, blank=True)

# Propriétaire
class Proprietaire(models.Model):
    TYPE_CHOICES = [
        ('physique', 'Personne Physique'),
        ('morale', 'Société'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    nom = models.CharField(max_length=100, blank=True)
    prenom = models.CharField(max_length=100, blank=True)
    raison_sociale = models.CharField(max_length=200, blank=True)

    sexe = models.CharField(max_length=10, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    nationalite = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)

    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    adresse = models.TextField(blank=True)
    domicile = models.CharField(max_length=200, blank=True)

# Parcelle
class Parcelle(models.Model):
    geom = models.PolygonField()
    agent_leve = models.ForeignKey(AgentLeve, on_delete=models.SET_NULL, null=True)
    date_leve = models.DateField()

# Relation Parcelle - Propriétaire
class ParcelleProprietaire(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE)

# Titre foncier
class TitreFoncier(models.Model):
    numero_titre = models.CharField(max_length=100)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    verrouillage = models.BooleanField(default=False)

# Hypothèque
class Hypotheque(models.Model):
    titre = models.ForeignKey(TitreFoncier, on_delete=models.CASCADE)
    banque = models.CharField(max_length=100)
    montant = models.FloatField()

    date_debut = models.DateField()
    date_fin = models.DateField()
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('rembourse', 'Remboursé'),
    ]
    statut_remboursement = models.CharField(
        max_length=20,  # suffisant pour tes valeurs
        choices=STATUT_CHOICES,
        default='en_attente'
    )

# Paiement
class Paiement(models.Model):
    hypotheque = models.ForeignKey(Hypotheque, on_delete=models.CASCADE)
    montant = models.FloatField()
    date_paiement = models.DateField()
    reference = models.CharField(max_length=100, blank=True)

# Document
class Document(models.Model):
    titre = models.ForeignKey(TitreFoncier, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='documents/')
    type_document = models.CharField(max_length=100)
    date_upload = models.DateField(auto_now_add=True)