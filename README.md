#Article Management API (Flask + Swagger)

Cette API REST permet de gérer un catalogue d'articles de science-fiction. Elle offre des fonctionnalités de création, lecture, mise à jour, suppression (CRUD) ainsi qu'un système de recherche et de filtrage.

L'API est documentée interactivement grâce à Swagger (Flasgger).

#Fonctionnalités

- CRUD complet : Gérer les articles (Titre, Auteur, Contenu, Catégorie, Tags).
- Filtrage avancé : Rechercher par auteur, par catégorie ou par date de publication.
- Recherche textuelle : Rechercher un mot-clé dans le titre ou le contenu.
- Documentation interactive : Interface Swagger UI pour tester les endpoints directement.


## Prérequis

Avant de commencer, assurez-vous d'avoir :
- Python 3.x installé.
- MySQL installé et en cours d'exécution.


## Installation

1. Cloner le projet (ou copier les fichiers) :   git clone <url-du-repo>
   cd <nom-du-dossier>
   
2. Installer les dépendances :   pip install flask pymysql flasgger

## Configuration de la Base de Données

1. Connectez-vous à votre interface MySQL (via terminal ou PHPMyAdmin).
2. Créez la base de données :   CREATE DATABASE blog_db;
   
3. Créez la table articles :   USE blog_db;

   CREATE TABLE articles (
       id INT AUTO_INCREMENT PRIMARY KEY,
       titre VARCHAR(255) NOT NULL,
       auteur VARCHAR(100) NOT NULL,
       contenu TEXT,
       date_publication DATE,
       categorie VARCHAR(100),
       tags VARCHAR(255)
   );
   
4. Note sur la sécurité : Le code utilise actuellement l'utilisateur blog_user1 avec le mot de passe felix2007. Assurez-vous de créer cet utilisateur ou de modifier les identifiants dans la fonction get_db_connection() du fichier app.py.

---

## Lancement de l'application

Lancez le serveur Flask avec la commande :python app.py

Le serveur démarrera par défaut sur : http://127.0.0.1:5000

## Documentation de l'API (Swagger)

Une fois le serveur lancé, vous pouvez accéder à la documentation interactive et tester les routes à l'adresse suivante :

[http://127.0.0.1:5000/apidocs/](http://127.0.0.1:5000/apidocs/)

Points d'entrée (Endpoints) principaux:

Méthode		Route				Description
GET		/GET/api/articles		lister tous les aricles(filtre optionnel: auteur, categorie, date_publication)	
GET		/GET/api/articles/<id>		récupère un article spécifique par son ID
GET		/GET/api/articles/search	recherche par mot-clé (paramètre: query)	
POST		/POST/api/articles		ajoute un nouvel article (JSON requis)
PUT		/PUT/api/articles/<id>		modifie un article existant
DELETE		/DELETE/api/articles/<id>	supprime un article


## Structure du JSON pour le POST

Pour ajouter un article, envoyez un corps (body) JSON comme celui-ci :

{
  "titre": "L'Empire Galactique",
  "auteur": "Isaac Asimov",
  "contenu": "L'histoire d'un empire futuriste...",
  "date_publication": "2023-10-27",
  "categorie": "Science-Fiction",
  "tags": "Espace, Robot, Futur"
}

