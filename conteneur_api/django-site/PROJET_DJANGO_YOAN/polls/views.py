

from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import Personnage
from .forms import PersonnageForm  
from .models import Personnage, Classe, Serveur, Contenu, Niveau


def classement(request): # stockage des variables dans des dictionnaires
    personnages_par_classe = {}
    personnages_par_serveur = {}
    personnages_par_contenu = {}
    personnages_par_niveau = {}

    # Classer les personnages par classe, serveur, contenu, et niveau
    classes = Classe.objects.all()
    serveurs = Serveur.objects.all()
    contenus = Contenu.objects.all()
    niveaux = Niveau.objects.all()

    for classe in classes:
        personnages_par_classe[classe] = Personnage.objects.filter(classe=classe).order_by('-score') # classement par ordre décroissant

    for serveur in serveurs:
        personnages_par_serveur[serveur] = Personnage.objects.filter(serveur=serveur).order_by('-score')

    for contenu in contenus:
        personnages_par_contenu[contenu] = Personnage.objects.filter(contenu=contenu).order_by('-score')

    for niveau in niveaux:
        personnages_par_niveau[niveau] = Personnage.objects.filter(niveau=niveau).order_by('-score')

    # rendu en html
    return render(request, 'classement.html', { 
        'personnages_par_classe': personnages_par_classe,
        'personnages_par_serveur': personnages_par_serveur,
        'personnages_par_contenu': personnages_par_contenu,
        'personnages_par_niveau': personnages_par_niveau
    })





