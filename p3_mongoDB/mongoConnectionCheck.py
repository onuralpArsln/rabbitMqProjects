
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

## bu git ignorelandı güvenlik amaçlı 
##bu directorye şifreni password isimli bir dosyada password değişkenine atarak koyarasan otamtik çeker ama gitignorelamayı unutma
from password import yourPasswordHere


uri = "mongodb+srv://onuralparslan:"+yourPasswordHere+"@datalogcluster.pyxjkxs.mongodb.net/?appName=dataLogCluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# ping atarak bağlantı kontrol 
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# database oluşumu 

baseDb = client["basedatabase"]

print("Database adı ->")
#sistemdeki databaseleri gör 
print(client.list_database_names())

#bir koleksiyon oluştur 
logCol = baseDb["logs"]

# koleksiyonları kontrol et 

print(baseDb.list_collection_names())


# koleksiyona bir  ekleme yap 
def addOne():
    dailyLog = { "date": "today", "request": "reachingDb" }
    x = logCol.insert_one(dailyLog)

# koleksiyona toplu  ekleme yap 
def addMany():
    dailyLogs = [
  { "date": "yesterday", "request": "create"},
  { "date": "yesterday", "request": "create"},
  { "date": "yesterday", "request": "create"},
  { "date": "yesterday", "request": "create"},
  { "date": "yesterday", "request": "update"},
  { "date": "yesterday", "request": "update"},
  { "date": "today", "request": "update"},
  { "date": "today", "request": "delete"},
  { "date": "today", "request": "delete"},
  { "date": "today", "request": "read"},
  { "date": "today", "request": "read"},
  { "date": "today", "request": "read"}
]
    x = logCol.insert_many(dailyLogs)

# içindekileri gör 
def seeCol():

    for x in logCol.find():
        print(x)

# arama yap 
def search():
    query = { "request": "read" }
    logDoc = logCol.find(query)
    for x in logDoc:
        print(x)

