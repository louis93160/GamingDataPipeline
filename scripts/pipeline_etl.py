from pymongo import MongoClient
from pymongo.errors import ConnectionFailure



def connexion_mongo(uri, db_name):


    try:
        client = MongoClient(uri)
        db = client[db_name]
        db.command("ping")
        print("Connexion à MongoDB réussie")
        return db
    except ConnectionFailure as e:
        print(f"Connexion à MongoDB échoué: {e}")
        return None

uri = "mongodb://127.0.0.1:27017"
db_name = "Blent"

db = connexion_mongo(uri, db_name)
