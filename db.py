import redis
import pymongo
import json

# Verbindung zur MongoDB herstellen
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Datenbank und Collection auswählen
db = client["IMDB"]
collection = db["movie_title"]

r = redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8")


def get_n_entries(n):
    # Abfrage erstellen (z. B. alle Dokumente abrufen und auf 100 begrenzen)
    query = {}  # Leere Abfrage, um alle Dokumente abzurufen

    # Filme aus der Datenbank abrufen (maximal 100)
    return collection.find(query).limit(n)


def find_movie(name: str, limit: int = 100):
    search_query = {"$text": {"$search": name}}

    # Filme aus der Datenbank abrufen (bis zu 100 Ergebnisse)
    results = collection.find(search_query).limit(limit)

    # Ergebnisse zurückgeben
    return list(results)


def get_recents(username: str = "test"):
    result = r.lrange(f"{username}:recents", 0, -1)
    return map(lambda x: json.loads(x), result)


def add_to_recents(movie: dict, username: str = "test"):
    r.lpush(f"{username}:recents", json.dumps(movie))


def write_data_to_redis(key, data):
    # Daten in Redis schreiben
    r.set(key, data)


def read_data_from_redis(key: str):
    # Daten aus Redis lesen
    return r.get(key)



