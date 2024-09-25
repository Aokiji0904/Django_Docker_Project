from polls.serializers import PersonnageSerializer, ServeurSerializer, NiveauSerializer, ClasseSerializer, ContenuSerializer
from django.contrib import messages

from rest_framework import viewsets
import csv
from django.shortcuts import render, redirect
from polls.models import Personnage, Classe, Serveur, Contenu, Niveau
from django.http import HttpResponse, JsonResponse

def importer_personnages(request):
    message = ""  # Initialise la variable message

    if request.method == 'POST':
        fichier_txt = request.FILES.get('fichier_txt')

        if not fichier_txt or not fichier_txt.name.endswith('.txt'):
            message = "Le fichier doit être au format .txt"
            return render(request, 'importer_personnages.html', {'message': message, 'is_api': True})

        fichier_txt = fichier_txt.read().decode('utf-8').splitlines()
        reader = csv.reader(fichier_txt, delimiter=',')

        for row in reader:
            # Ignore les lignes vides et vérifie le bon nombre de colonnes
            if not row or len(row) != 6:
                continue  # Passe à la ligne suivante si elle est vide ou mal formatée
            
            name, classe_name, serveur_name, contenu_name, niveau_valeur, score = row

            # Ignore la première ligne si elle contient les en-têtes
            if name.lower() == "name":
                continue

            # Vérifie si `niveau_valeur` est bien un nombre
            try:
                niveau_valeur = int(niveau_valeur)  # Convertit en entier
            except ValueError:
                message = f"Le niveau '{niveau_valeur}' n'est pas un nombre valide."
                return render(request, 'importer_personnages.html', {'message': message, 'is_api': True})

            # Récupérer ou créer les objets associés
            classe, _ = Classe.objects.get_or_create(name=classe_name)
            serveur, _ = Serveur.objects.get_or_create(name=serveur_name)
            contenu, _ = Contenu.objects.get_or_create(name=contenu_name)

            niveau = Niveau.objects.filter(valeur=niveau_valeur).first()
            if niveau is None:
                niveau = Niveau.objects.create(valeur=niveau_valeur)

            # Créer et sauvegarder le personnage
            Personnage.objects.create(
                name=name,
                classe=classe,
                serveur=serveur,
                contenu=contenu,
                niveau=niveau,
                score=int(score)  # Convertit le score en entier
            )

        messages.success(request, "Importation réussie !")
        return redirect('importer_personnages')

    # Retourne la page d'importation avec un message vide
    return render(request, 'importer_personnages.html', {'is_api': True, 'messages': messages.get_messages(request)})





class PersonnageViewSet(viewsets.ModelViewSet):
    queryset = Personnage.objects.all()  # Détermine quels objets seront retournés
    serializer_class = PersonnageSerializer  # Détermine comment les objets seront sérialisés



class ContenuViewSet(viewsets.ModelViewSet):
    queryset = Contenu.objects.all()
    serializer_class = ContenuSerializer



class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer



class NiveauViewSet(viewsets.ModelViewSet):
    queryset = Niveau.objects.all()
    serializer_class = NiveauSerializer




class ServeurViewSet(viewsets.ModelViewSet):
    queryset = Serveur.objects.all()
    serializer_class = ServeurSerializer







