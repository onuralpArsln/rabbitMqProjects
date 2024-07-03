
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