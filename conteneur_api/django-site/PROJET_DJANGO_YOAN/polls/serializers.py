from rest_framework import serializers
from .models import Personnage, Serveur, Classe, Niveau, Contenu

class PersonnageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personnage
        fields = '__all__'


class ServeurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serveur
        fields = ['id', 'name']



class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = ['id', 'valeur']



class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'name']


class ContenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contenu
        fields = ['id', 'name']


    # permet à l'api de récupérer les modèles de l'application polls