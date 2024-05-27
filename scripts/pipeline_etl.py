from pymongo import MongoClient
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
        '$sort': {'_id': 1}
    }
]

# Exécuter le pipeline d'agrégation
result = list(collection.aggregate(pipeline))

# Afficher les résultats
for doc in result:
    print(doc)
