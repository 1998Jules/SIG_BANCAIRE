from django import forms
from .models import (
    Proprietaire, TitreFoncier, Hypotheque, Paiement, Document
)

class ProprietaireForm(forms.ModelForm):
    class Meta:
        model = Proprietaire
        fields = '__all__'


class TitreFoncierForm(forms.ModelForm):
    class Meta:
        model = TitreFoncier
        fields = '__all__'


class HypothequeForm(forms.ModelForm):
    class Meta:
        model = Hypotheque
        fields = '__all__'


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'