from tinydb import TinyDB

db = TinyDB("db.json", sort_keys=True, indent=4, separators=(',', ': '))

def getDb() -> TinyDB:
    return db
