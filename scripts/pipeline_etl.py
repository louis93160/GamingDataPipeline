from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta
import psycopg2


def fetch_and_store_top_games():

    # Connexion à MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Blent"]
    collection = db["VideoGame"]


    # Définir la date de fin et calculer la date de début 6 mois avant
    fin = datetime(2018, 10, 2)
    debut = fin - relativedelta(months=6)

    pipeline = [
        {
            '$match': {
                'unixReviewTime': {
                    '$gt': int(debut.timestamp()), 
                    '$lt': int(fin.timestamp())
                }
            }
        },
        {
            '$group': {
                '_id': '$asin',
                'averageRating': {'$avg': '$overall'},
                'numUsersRated': {'$sum': 1},
                'oldestRating': {'$min': '$unixReviewTime'},
                'newestRating': {'$max': '$unixReviewTime'}
            }
        },
        {
            '$addFields': {
                'averageRating': {'$round': ['$averageRating', 1]},
                'oldestRating': {
                    '$dateToString': {
                        'format': '%Y-%m-%d', 
                        'date': {'$toDate': {'$multiply': ['$oldestRating', 1000]}}
                    }
                },
                'newestRating': {
                    '$dateToString': {
                        'format': '%Y-%m-%d', 
                        'date': {'$toDate': {'$multiply': ['$newestRating', 1000]}}
                    }
                }
            }
        },
        {
            '$sort': {'averageRating': 1}
        },
        {
            '$limit': 15
        }
    ]

    # Exécuter le pipeline d'agrégation
    result = list(collection.aggregate(pipeline))

    print(result)

fetch_and_store_top_games()

#     #Connexion à PostgreSQL
#     conn = psycopg2.connect(
#         dbname = "jeux_videos",
#         user = "postgres",
#         password = "louis",
#         host = "localhost",
#         port = "5432"
#     )

#     cur = conn.cursor()

#     #Requête SQL pour insérer ou mettre à jour les données
#     upsert_query = """
#     INSERT INTO gestion_jeux.jeux_videos (id_jeux, note_moyenne, nombre_utilisateurs, note_plus_ancienne, note_plus_recente)
#         VALUES (%s, %s, %s, %s, %s)
#         ON CONFLICT (id_jeux) 
#         DO UPDATE SET
#             note_moyenne = EXCLUDED.note_moyenne,
#             nombre_utilisateurs = EXCLUDED.nombre_utilisateurs,
#             note_plus_ancienne = EXCLUDED.note_plus_ancienne,
#             note_plus_recente = EXCLUDED.note_plus_recente;


#     """

#     for doc in result:
#         cur.execute(upsert_query,(
#             doc["_id"],
#             doc["averageRating"],
#             doc["numUsersRated"],
#             doc["oldestRating"],
#             doc["newestRating"]
#         ))

#     #Valider les transactions et fermer la connexion
#     conn.commit()
#     cur.close()
#     conn.close()

# if __name__ == "__main__":
#     fetch_and_store_top_games()