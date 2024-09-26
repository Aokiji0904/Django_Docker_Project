## Docker CLI Cheat sheet :
https://docs.docker.com/get-started/docker_cheatsheet.pdf
## Dockerfile cheat sheet : 
https://kapeli.com/cheat_sheets/Dockerfile.docset/Contents/Resources/Documents/index
## Dockercompose cheat sheet : 
https://devhints.io/docker-compose

----------------------------------------------------------------------------------------------------------------------------------------------------------
```
          Réseau virtuel Docker
+---------------------------------------------+
|                                             |
|  Hôte (127.0.0.1)                           |
|      Accès via IP:ports :                   |
|      127.0.0.1:80 -> Nginx                  |
|                 | 80                        |
|     +----------------------------+          |
|     |      Proxy (nginx)          |         |
|     |    Docker container         |         |
|     |  Expose: 8081 -> 80         |         |
|     +----------------------------+          |
|                 | 8081                      |
|      --------------------------             |
|     | 8083                   | 8001         |
|     v                        v              |
| +----------------+      +----------------+  |
| | API            |      | Frontend (Polls)| |
| | conteneur_api  |      | conteneur_polls | |
| | Expose: 8083   |      | Expose: 8001    | |
| | (8083:8083)    |      | (8001:8001)     | |
| +----------------+      +----------------+  |
|     | 8083                        8001 |    |
|     v -------------------------------- v    |
|                 | 5432                      |
|  +----------------------------------------+ |
|  |    Base de Données (PostgreSQL)        | |
|  |    Docker container                    | |
|  |    Expose: 5432 (5432:5432)            | |
|  +----------------------------------------+ |
+---------------------------------------------+
```
```
Schéma de la base de donnée

+-------------------+
|Utilisateur(Django)| 
+-------------------+
        n
        |
        |
        1
+-------------------+        +-------------------+        +-------------------+
| Serveur           |        | Classe            |        | Contenu           |
+-------------------+        +-------------------+        +-------------------+
| ID (clé primaire) |        | ID (clé primaire) |        | ID (clé primaire) |
| name (char<100)   |        | name (char<100)   |        | name (char<100)   |
+-------------------+        +-------------------+        +-------------------+
        1                        1                          1
        |                        |                          |
        |                        |                          | 
        n                        n                          n
+-------------------------------------------------------------------------+
|                                 Personnage                             |
+-------------------------------------------------------------------------+
| ID (clé primaire)                                                     |
| name (char<100)                                                       |
| serveur (clé étrangère vers Serveur)                                  |
| classe (clé étrangère vers Classe)                                    |
| contenu (clé étrangère vers Contenu)                                  |
| niveau (clé étrangère vers Niveau)                                    |
| score (integer, default=0)                                            |
+-------------------------------------------------------------------------+
                                                                 n
                                                                 |
                                                                 |
                                                                 1
                                                   +-------------------+
                                                   | Niveau            |
                                                   +-------------------+
                                                   | ID (clé primaire) |
                                                   | valeur (integer)  |
                                                   +-------------------+

```





#### Questions


### Fonctionnement de Django


1. Vous disposez d'un projet Django dans lequel une application public a été créée. Décrivez la suite de requêtes et d'exécutions permettant l'affichage d'une page HTML index.html à l'URL global / via une application public, ne nécessitant pas de contexte de données. Vous décrirez la position exacte dans l'arborescence des répertoires des différents fichiers utiles à cette exécution.

2. Dans quelle(s) section(s) de quel(s) fichier(s) peut-on configurer la base de données que l'on souhaite utiliser pour un projet Django ?

3. Dans quel(s) fichier(s) peut-on configurer le fichier de paramètres que l'on souhaite faire utiliser par le projet Django ? Si plusieurs fichers sont à mentionner, expliquez le rôle de chaque fichier.

4. Nous nous plaçons à la racine de votre projet Django. Quel effet a l'exécution python manage.py makemigrations ? Et l'exécution python manage.py migrate ? Quel(s) fichier(s) sont mis en oeuvre pendant ces exécutions ?


### Fonctionnement de Docker

1. Expliquez l'effet et la syntaxe de ces commandes, communément vues dans des fichiers Dockerfile : FROM, RUN, WORKDIR, EXPOSE, CMD.

Dans la définition d'un service dans le fichier docker-compose.yml, expliquez l'effet des mentions :

ports:
    - "80:80"

build: 
    context: .
    dockerfile: Dockerfile.api

depends_on:
    - web
    - api

environment:
    POSTGRES_DB: ${POSTGRES_DB}
    POSTGRES_USER: ${POSTGRES_USER}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}

2. Citez une méthode pour définir des variables d'environnement dans un conteneur.

3. Dans un même réseau Docker, nous disposons d'un conteneur nginx (utilisant l'image nginx:latest) et d'un conteneur web (utilisant une image contenant un projet web Django, ayant la commande python manage.py runserver 0.0.0.0:8000 de lancée au démarrage du conteneur). Comment adresser le serveur web tournant dans le conteneur web depuis le conteneur nginx, sans utiliser les adresses IP des conteneurs ?


#### Réponses aux questions


 ### Fonctionnement de Django

1. 

   Lorsqu'un utilisateur accède à l'URL `/`, voici la suite d'exécutions qui permet l'affichage d'une page `index.html` dans Django :
   
   - Configuration de l'URL: 
     
     Dans le fichier `urls.py` de l'application `public` (ex. `public/urls.py`), il y a une association entre l'URL `/` et une vue (`view`).
     
     ```python
     # public/urls.py
     from django.urls import path
     from . import views

     urlpatterns = [
         path('', views.index, name='index'),
     ]
     ```

   - Vue associée à l'URL :
     
     La fonction `index` dans le fichier `views.py` de l'application `public` renvoie un template HTML (`index.html`).
     
     ```python
     # public/views.py
     from django.shortcuts import render

     def index(request):
         return render(request, 'public/index.html')
     ```

   - Template `index.html` :
     
     Le template `index.html` est situé dans `public/templates/public/index.html` et contient le contenu HTML à afficher.
     
     ```html
     <!-- public/templates/public/index.html -->
     <!DOCTYPE html>
     <html>
     <head>
         <title>Page d'accueil</title>
     </head>
     <body>
         <h1>Bienvenue sur la page d'accueil</h1>
     </body>
     </html>
     ```

   - Configuration globale des URLS du projet :
     
     Le fichier `urls.py` au niveau du projet (ex. `mysite/urls.py`) doit inclure les URLs de l'application `public` :
     
     ```python
     # mysite/urls.py
     from django.contrib import admin
     from django.urls import include, path

     urlpatterns = [
         path('admin/', admin.site.urls),
         path('', include('public.urls')),
     ]
     ```


2. 

   La configuration de la base de données se fait dans le fichier `settings.py`, généralement situé à la racine de l'application principale du projet (par exemple `mysite/settings.py`), dans la section `DATABASES` :
   
   ```python
   # mysite/settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',  # Utilisation de PostgreSQL
           'NAME': 'nom_base_de_donnees',
           'USER': 'utilisateur',
           'PASSWORD': 'mot_de_passe',
           'HOST': 'localhost',  # Adresse de la base de données
           'PORT': '5432',  # Port de PostgreSQL
       }
   }
   ```

3. 

   - Fichier `wsgi.py` (ex. `mysite/wsgi.py`) : Ce fichier est utilisé pour les serveurs de production et spécifie le fichier de paramètres à utiliser :
     
     ```python
     import os
     from django.core.wsgi import get_wsgi_application

     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
     application = get_wsgi_application()
     ```

   - Fichier `manage.py` (ex. `mysite/manage.py`) : Lors de l'exécution des commandes Django en local (comme `runserver`), le fichier `manage.py` définit également le fichier de paramètres :
     ```python
     import os
     import sys

     def main():
         os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
         ...
     ```

4. 

   - `makemigrations` : Cette commande crée des fichiers de migration basés sur les modifications apportées aux modèles Django. Les fichiers générés sont enregistrés dans le dossier `migrations` de chaque application concernée (par ex. `public/migrations/`).
   
   - `migrate` : Cette commande applique les migrations à la base de données, en modifiant sa structure en fonction des fichiers de migration créés. Les fichiers `migrations` sont lus et la base de données est mise à jour.

 Fonctionnement de Docker

1. 

   - `FROM` : Définit l'image de base à utiliser pour créer le conteneur. Exemple :
     ```dockerfile
     FROM python:3.8-alpine
     ```

   - `RUN` : Exécute une commande pendant la construction de l'image Docker. Exemple :
     ```dockerfile
     RUN pip install -r requirements.txt
     ```

   - `WORKDIR` : Définit le répertoire de travail à l'intérieur du conteneur. Exemple :
     ```dockerfile
     WORKDIR /app
     ```

   - `EXPOSE` : Indique le port que le conteneur va écouter. Exemple :
     ```dockerfile
     EXPOSE 8000
     ```

   - `CMD` : Spécifie la commande par défaut qui sera exécutée au démarrage du conteneur. Exemple :
     ```dockerfile
     CMD ["gunicorn", "mysite.wsgi:application"]
     ```

2. 

   - `ports: "80:80"` : Associe le port `80` de l'hôte au port `80` du conteneur. Exemple :
     ```yaml
     ports:
       - "80:80"
     ```

   - `build: context` et `dockerfile` : Spécifie le chemin du contexte de construction (`.` pour le répertoire courant) et le fichier Dockerfile à utiliser pour la construction. Exemple :
     ```yaml
     build:
       context: .
       dockerfile: Dockerfile.api
     ```

   - `depends_on` : Définit les services qui doivent être démarrés avant le service en cours. Exemple :
     ```yaml
     depends_on:
       - web
       - api
     ```

   - `environment` : Définit les variables d'environnement pour le conteneur. Exemple :
     ```yaml
     environment:
       POSTGRES_DB: ${POSTGRES_DB}
       POSTGRES_USER: ${POSTGRES_USER}
       POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
     ```

3. 

   Une méthode courante est d'utiliser le fichier `.env` avec des variables d'environnement, ou directement dans `docker-compose.yml` via la clé `environment` :
   ```yaml
   environment:
     POSTGRES_DB: mydb
     POSTGRES_USER: user
     POSTGRES_PASSWORD: password
   ```

4. 

   Dans un même réseau Docker, on peut utiliser le nom du service défini dans `docker-compose.yml` pour adresser un autre conteneur. Par exemple, pour adresser le conteneur `web`, on peut configurer Nginx avec l'upstream suivant :

   ```nginx
   upstream django_server {
       server web:8000;
   }

   server {
       listen 80;
       location / {
           proxy_pass http://django_server;
       }
   }
   ```
   Ici, `web` est le nom du service défini dans `docker-compose.yml`.


Différents endpoints : 

API : 

http://localhost:8083

    - /api
    - /importer-personnages

POLLS :

http://localhost:8001

    - /admin
    - /admin/polls
    - /classement




#### Comment importer une liste de personnages depuis la page web http://localhost:8083/importer-personnages ?

Il faut simplement que le fichier importé respecte une certaine syntaxe.

Exemple (personnages.txt) : 
```
name,classe,serveur,contenu,niveau,score
Arthas,Guerrier,Serveur_1,Donjon,50,1500
Jaina,Mage,Serveur_2,Raid,60,2100
Thrall,Chaman,Serveur_3,Quête,40,1300
Sylvanas,Chasseur,Serveur_1,PvP,55,1800
Illidan,Démoniste,Serveur_4,Donjon,58,1700
Tyrande,Druide,Serveur_2,Raid,60,2200
Guldan,Prêtre,Serveur_3,Donjon,45,1400
Velen,Guerrier,Serveur_1,PvP,52,1600
Khadgar,Mage,Serveur_4,Quête,48,1350
Malfurion,Druide,Serveur_2,Raid,60,2250
Anduin,Paladin,Serveur_3,PvP,53,1750
Garrosh,Guerrier,Serveur_5,Donjon,57,1550
Uther,Paladin,Serveur_1,Raid,60,2300
Bolvar,Chevalier de la Mort,Serveur_3,Quête,49,1370
Vol'jin,Voleur,Serveur_4,PvP,56,1700
Rexxar,Chasseur,Serveur_2,Donjon,54,1650
Kael'thas,Mage,Serveur_1,Raid,60,2400
Grommash,Guerrier,Serveur_3,PvP,58,1900
Liadrin,Paladin,Serveur_2,Donjon,55,1800
Medivh,Mage,Serveur_4,Quête,47,1400
Chen,Druide,Serveur_3,Raid,60,2150
Baine,Guerrier,Serveur_5,PvP,52,1650
Kel'Thuzad,Nécromancien,Serveur_2,Donjon,50,1700
Maiev,Voleur,Serveur_1,Raid,60,2000
Zul'jin,Chasseur,Serveur_3,PvP,59,1850
Thrallmar,Chaman,Serveur_4,Quête,48,1450
Lor'themar,Guerrier,Serveur_5,Raid,60,2100
Valeera,Voleur,Serveur_2,PvP,53,1600
Fandral,Druide,Serveur_1,Donjon,56,1750
Ysera,Démoniste,Serveur_4,Quête,49,1500
Nozdormu,Mage,Serveur_3,Raid,60,2200
```

Cela permet d'éviter d'importer les personnages via ces commandes dans le terminal : 

## Obtenir l'adresse IP du conteneur "conteneur_api"
```
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' conteneur_api
```
## Récupérer le contenu de la page pour obtenir le CSRF token
```
response=$(curl -c cookies.txt http://172.18.0.4:8083/importer-personnages/)
csrf_token=$(echo "$response" | grep -oP 'name="csrfmiddlewaretoken" value="\K[^"]+')
```
## Envoyer le fichier avec le cookie et le token CSRF
```
curl -X POST http://172.18.0.4:8083/importer-personnages/ \
-F "csrfmiddlewaretoken=$csrf_token" \
-F "fichier_txt=@../Téléchargements/personnages.txt" \
-b cookies.txt
```

#### Execution avec docker compose up --build


Les données de la base de données sont persistentes (volume présent), et les dépendances sont dans requirements.txt.




--------------------------------------------------------------------------------------------------------------------------------------------------------# Django_Docker_Project
