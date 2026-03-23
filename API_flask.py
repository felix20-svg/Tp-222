from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)
app.config["DEBUG"] = True

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
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/GET/api/articles', methods=['GET'])
def get_articles1():
    connection=get_db_coonection()
    try:
        with connection.cursor() as cursor:
            auteur = request.args.get('auteur')
            categorie = request.args.get('categorie')
            date = request.args.get('date_publication')
            if auteur:
                sql="SELECT* FROM articles WHERE auteur LIKE %s"
                cursor.execute(sql, (f"%{auteur}%",))
                result=cursor.fetchall()
                return jsonify(result), 200
            elif categorie:
                sql="SELECT* FROM articles WHERE categorie LIKE %s"
                cursor.execute(sql, (f"%{categorie}%",))
                result=cursor.fetchall()
                return jsonify(result), 200
            elif date:
                sql="SELECT* FROM articles WHERE date_publication LIKE %s "
                cursor.execute(sql, (date))
                result=cursor.fetchall()
                return jsonify(result), 200
            else:
                sql="SELECT* FROM articles"
                cursor.execute(sql)
                result=cursor.fetchall()
                return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
    finally:
        connection.close()

@app.route('/GET/api/articles/<int:id>', methods=['GET'])
def get_articles_id(id):
    connection=get_db_coonection()
    try:
        with connection.cursor() as cursor:
            sql="SELECT* FROM articles WHERE id = %s"
            cursor.execute(sql, (id))
            result=cursor.fetchone()
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
    connection=get_db_coonection()
    try:
        with connection.cursor() as cursor:
            query = request.args.get('query')
            if query:
                sql="SELECT* FROM articles WHERE contenu LIKE %s OR titre LIKE %s"
                valeur = f"%{query}%"
                cursor.execute(sql, (valeur, valeur))
                result=cursor.fetchall()
            if result:
                return jsonify(result), 200
            else:
                return jsonify("erreur article introuvable"), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
    finally:
        connection.close()


@app.route('/POST/api/articles', methods=['POST'])
def set_articles():
    connection=get_db_coonection()
    
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
    connection=get_db_coonection()
    
    donnees = request.get_json()
    
    titre = donnees.get('titre')
    contenu = donnees.get('contenu')
    tags = donnees.get('tags') 
    categorie = donnees.get('categorie')
    
    try:
        with connection.cursor() as cursor:
            if titre:
                sql = "UPDATE articles SET titre=%s WHERE id=%s"
                cursor.execute(sql, (titre, id))
                connection.commit()
                return jsonify({"message": "modification réussie"}), 200
            elif contenu:
                sql = "UPDATE articles SET contenu=%s WHERE id=%s"
                cursor.execute(sql, (contenu, id))
                connection.commit()
                return jsonify({"message": "modification réussie"}), 200
            elif tags:
                sql = "UPDATE articles SET tags=%s WHERE id=%s"
                cursor.execute(sql, (tags, id))
                connection.commit()
                return jsonify({"message": "modification réussie"}), 200
            elif categorie:
                sql = "UPDATE articles SET categorie=%s WHERE id=%s"
                cursor.execute(sql, (categorie, id))
                connection.commit()
                return jsonify({"message": "modification réussie"}), 200
            else:
                return jsonify({"error": "modification impossible"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
            
    finally:
        connection.close()

@app.route('/DELETE/api/articles/<int:id>', methods=['DELETE'])
def delete_articles(id):
    connection=get_db_coonection()
    
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

app.run()
