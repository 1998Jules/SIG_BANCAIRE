from django.urls import path
from . import views

urlpatterns = [
    path('carte/', views.index, name='index'),
     path('parcelle/<int:parcelle_id>/enrichir/', views.enrichir_parcelle, name='enrichir_parcelle'),

    path('parcelle/<int:parcelle_id>/proprietaire/', views.ajouter_proprietaire, name='ajouter_proprietaire'),
    path('parcelle/<int:parcelle_id>/titre/', views.ajouter_titre, name='ajouter_titre'),

    path('titre/<int:titre_id>/hypotheque/', views.ajouter_hypotheque, name='ajouter_hypotheque'),
    path('hypotheque/<int:hypotheque_id>/paiement/', views.ajouter_paiement, name='ajouter_paiement'),

    path('titre/<int:titre_id>/document/', views.ajouter_document, name='ajouter_document'),
    path('dashboard/', views.dashboard, name='dashboard')
]