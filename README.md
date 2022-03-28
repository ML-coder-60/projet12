![Epic Events](epic_events.png)

[![forthebadge](https://forthebadge.com/images/badges/cc-0.svg)](https://forthebadge.com) 
[![forthebadge](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://img.shields.io) 
[![forthebadge](https://img.shields.io/badge/Postgres-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://img.shields.io)
[![forthebadge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://img.shields.io)


# Projet12
Développez une architecture back-end sécurisée en utilisant Django ORM

_Testé sous Debian 11 - Python 3.9.2 - Django 4.0.3 - DRF 3.13.1 - simplejwt 5.1.0_

## Installation

[**Python 3**](https://wiki.python.org/moin/BeginnersGuide/Download) et [**PostgreSQL**](https://wiki.postgresql.org/wiki/Detailed_installation_guides) sont nécessaire pour le fonctionnement de l’application.

1. Récupérer les sources du projet https://github.com/ML-coder-60/projet12

```shell
git clone https://github.com/ML-coder-60/projet12
cd projet12
```

2. Installation/initialisation de l'environnement virtuel

```shell
python -m venv env
source env/bin/activate

```

3. Installation des composants
- Python 3
- Django REST Framework 
- JSON Web Token

```shell
pip install -r requirements.txt
```

4. Paramétrage PostgreSQL
 
4.1 Créer la base de données 'epic_events' sur le server Postgres.

```shell
postgres psql
CREATE DATABASE  epic_events;
```

4.2 Configurer un compte de connexion 'psql_django_account'  

4.2.1 Création du compte
```shell
CREATE USER psql_django_account WITH ENCRYPTED PASSWORD 'unmotdepasse';
```

4.2.2 [Optimisation](https://docs.djangoproject.com/en/3.0/ref/databases/#optimizing-postgresql-s-configuration)

```shell
ALTER ROLE psql_django_account SET client_encoding TO 'utf8';
ALTER ROLE psql_django_account SET default_transaction_isolation TO 'read committed';
ALTER ROLE psql_django_account SET timezone TO 'UTC';
ALTER USER psql_django_account CREATEDB;
```

4.2.3  Configuration des du nouveau compte 'psql_django_account'

```shell
GRANT ALL PRIVILEGES ON DATABASE epic_events TO psql_django_account;
```

5. Modifier le fichier setting.py «Paramètres de connexions SQL» pour être conforme à la configuration postgres

```python
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'epic_events',
       'USER': 'psql_django_account',
       'PASSWORD': 'unmotdepasse',
       'HOST': '127.0.0.1',
       'PORT': '5432',
   }
}
```

6. Appliquer les migrations en base et créer  un compte administrateur

```shell
python manage.py migrate
python manage.py createsuperuser
```

7. Démarrer l'application 

```shell
$ python manage.py runserver
```
 
8. Administration

___
    Seuls les membres de l'équipe de gestion ont accès 
    à la console d'administration de l'application.

    C'est interface permet de gérer les comptes , les clients, les contracts, les événements
    Le changement des mots de passe est a réaliser par les utilisateurs  depuis API 
___

La page d'administration est disponible depuis 
    
    http://127.0.0.1:8080/gestion/



9. API Epic Events

Le détail des points d'entrées ce trouve ici =>  

### Liste de points d'entrées

|  #  | Points de terminaison de l'API Epic Events             |  HTTP Method | URI   {example}           |
|:---:|--------------------------------------------------------|:------------:|:--------------------------|
|  1. | Connexion des utilisateurs (Token )                    |     POST     | /login/                   |
|  2. | Modifier le mot de passe de l'utilisateur authentifié  |     POST     | /change-password/         |
|  3. | Lister les clients                                     |     GET      | /clients/                 |
|  4. | Lister des clients par recherche*                      |     GET      | /clients/?search={str}    |
|  5. | Lister des clients par {filtre}*                       |     GET      | /clients/?{filtre}=value  |
|  6. | Détail d'un client                                     |     GET      | /clients/{id_du_client}   |
|  7. | Créer un client                                        |     POST     | /clients                  |
|  8. | Modifier un client                                     |     PUT      | /clients/{id_du_client}   |
|  9. | Lister des contrats                                    |     GET      | /contracts/               |
| 10. | Lister des contrats par recherche*                     |     GET      | /contracts/?search={str}  |
| 11. | Lister des contrats par {filtre}*                      |     GET      | /contracts/?{filtre}=value|
| 12. | Détail d'un contrat                                    |     GET      | /contracts/{id_du_contrat}|
| 13. | Créer un contrat                                       |     POST     | /contracts/               |
| 14. | Modifier un contrat                                    |     PUT      | /contracts/{id_du_contrat}|
| 13. | Lister les événements                                  |     GET      | /events/                  |
| 14. | Lister des événements par recherche*                   |     GET      | /events/?search={str}     |
| 15. | Lister des événements par {filtre}*                    |     GET      | /events/?{filtre}=value   |
| 16. | Détail d'un événement                                  |     GET      | /events/{id_events}       |
| 17. | Modifier un événement                                  |     PUT      | /events/{id_events}       |

* Pour des informations complémentaires merci de consulter la [documentation](https://documenter.getpostman.com/view/19223491/UVsJx7ga)

10. Logs

Les événements de l'application sont loggés dans le fichier     

    epic_events.log:  niveau du log(WARNING)


Information sur  le  [niveau des logs](https://docs.djangoproject.com/fr/4.0/topics/logging/)

11. Tests

Un suite de tests est disponible dans le dossier  epic_events/tests/ 

Pour exécuter les tests,  depuis le dossier 'epic_events' lancer la commande 

```shell
pytest -v 
``` 



