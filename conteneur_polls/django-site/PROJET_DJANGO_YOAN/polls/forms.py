from django import forms
from .models import Personnage

class PersonnageForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ['name', 'classe', 'serveur', 'contenu', 'niveau', 'score']  
# permet de simplifier le code grâce au formulaire Django 