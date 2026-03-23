from flask import Flask, request, jsonify
import pymysql
from flasgger import Swagger

app = Flask(__name__)
app.config["DEBUG"] = True

# Configuration de Swagger
swagger = Swagger(app)

def get_db_coonection():
    return pymysql.connect(
        host='localhost',
        user='blog_user1',
        password='felix2007',
        database='blog_db',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET'])
def home():
    """Page d'accueil de l'API
    ---
    responses:
      200:
        description: Message de bienvenue
    """
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
   
@app.route('/GET/api/articles', methods=['GET'])
def get_articles1():
    """Récupérer tous les articles ou filtrer par auteur/catégorie/date
    ---
    parameters:
      - name: auteur
        in: query
        type: string
        description: Nom de l'auteur
      - name: categorie
        in: query
        type: string
        description: Nom de la catégorie
      - name: date_publication
        in: query
        type: string
        description: Date (AAAA-MM-JJ)
    responses:
      200:
        description: Liste des articles trouvés
      500:
        description: Erreur serveur
    """
    connection = get_db_coonection()
    try:
        with connection.cursor() as cursor:
            auteur = request.args.get('auteur')
            categorie = request.args.get('categorie')
            date = request.args.get('date_publication')
            
            if auteur:
                sql = "SELECT * FROM articles WHERE auteur LIKE %s"
                cursor.execute(sql, (f"%{auteur}%",))
            elif categorie:
                sql = "SELECT * FROM articles WHERE categorie LIKE %s"
                cursor.execute(sql, (f"%{categorie}%",))
            elif date:
                sql = "SELECT * FROM articles WHERE date_publication = %s"
                cursor.execute(sql, (date,))
            else:
                sql = "SELECT * FROM articles"
                cursor.execute(sql)
                
            result = cursor.fetchall()
            return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/GET/api/articles/<int:id>', methods=['GET'])
def get_articles_id(id):
    """Récupérer un article par son ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID de l'article
    responses:
      200:
        description: Détails de l'article
      404:
        description: Article introuvable
    """
    connection = get_db_coonection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM articles WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if result:
                return jsonify(result), 200
            else:
                return jsonify("erreur article introuvable"), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/GET/api/articles/search', methods=['GET'])
def get_articles2():
    """Recherche plein texte dans le titre ou le contenu
    ---
    parameters:
      - name: query
        in: query
        type: string
        required: true
        description: Mot-clé à rechercher
    responses:
      200:
        description: Articles correspondants
      404:
        description: Aucun article trouvé
    """
    connection = get_db_coonection()
    try:
        with connection.cursor() as cursor:
            query = request.args.get('query')
            if query:
                sql = "SELECT * FROM articles WHERE contenu LIKE %s OR titre LIKE %s"
                valeur = f"%{query}%"
                cursor.execute(sql, (valeur, valeur))
                result = cursor.fetchall()
                if result:
                    return jsonify(result), 200
            return jsonify("erreur article introuvable"), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/POST/api/articles', methods=['POST'])
def set_articles():
    """Ajouter un nouvel article
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            titre:
              type: string
            auteur:
              type: string
            contenu:
              type: string
            date_publication:
              type: string
              example: "2023-10-27"
            categorie:
              type: string
            tags:
              type: string
    responses:
      200:
        description: Ajout réussi
      400:
        description: Données manquantes
    """
    connection = get_db_coonection()
    donnees = request.get_json()
    
    titre = donnees.get('titre')
    auteur = donnees.get('auteur')
    contenu = donnees.get('contenu')
    date = donnees.get('date_publication')
    tags = donnees.get('tags') 
    categorie = donnees.get('categorie')
    
    if not titre or not auteur:
        return jsonify({"erreur": "titre et auteur sont requis"}), 400
    
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO articles (titre, auteur, contenu, date_publication, categorie, tags) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (titre, auteur, contenu, date, categorie, tags))
            connection.commit()
            return jsonify({"message": "ajout réussi"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/PUT/api/articles/<int:id>', methods=['PUT'])
def modify_articles(id):
    """Modifier partiellement un article
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        schema:
          properties:
            titre:
              type: string
            contenu:
              type: string
            tags:
              type: string
            categorie:
              type: string
    responses:
      200:
        description: Modification réussie
      400:
        description: Impossible de modifier
    """
    connection = get_db_coonection()
    donnees = request.get_json()
    
    # Logique simplifiée : on prend le premier champ trouvé dans le JSON
    fields = ['titre', 'contenu', 'tags', 'categorie']
    field_to_update = next((f for f in fields if f in donnees), None)
    
    if not field_to_update:
        return jsonify({"error": "modification impossible"}), 400

    try:
        with connection.cursor() as cursor:
            sql = f"UPDATE articles SET {field_to_update}=%s WHERE id=%s"
            cursor.execute(sql, (donnees[field_to_update], id))
            connection.commit()
            return jsonify({"message": "modification réussie"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

@app.route('/DELETE/api/articles/<int:id>', methods=['DELETE'])
def delete_articles(id):
    """Supprimer un article
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Suppression réussie
    """
    connection = get_db_coonection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM articles WHERE id=%s"
            cursor.execute(sql, (id,))
            connection.commit()
            return jsonify({"message": "suppression réussie"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run()
