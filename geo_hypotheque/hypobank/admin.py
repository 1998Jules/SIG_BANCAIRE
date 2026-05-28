from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import AgentLeve, Proprietaire, Parcelle, ParcelleProprietaire, TitreFoncier, Hypotheque, Paiement, Document

admin.site.register(AgentLeve)
admin.site.register(Proprietaire)
admin.site.register(Parcelle)
admin.site.register(ParcelleProprietaire)
admin.site.register(TitreFoncier)
admin.site.register(Hypotheque)
admin.site.register(Paiement)
admin.site.register(Document)