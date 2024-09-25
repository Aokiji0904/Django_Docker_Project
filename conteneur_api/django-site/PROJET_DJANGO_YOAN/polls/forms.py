from django import forms
from .models import Personnage

class PersonnageForm(forms.ModelForm):
    class Meta:
        model = Personnage
        fields = ['name', 'classe', 'serveur', 'contenu', 'niveau', 'score']  #pour éviter de redéfinir les champs à chaque appel
