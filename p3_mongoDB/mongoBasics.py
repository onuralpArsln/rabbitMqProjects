
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

## bu git ignorelandı güvenlik amaçlı 
##bu directorye şifreni password isimli bir dosyada password değişkenine atarak koyarasan otamtik çeker ama gitignorelamayı unutma
import password as password

uri = "mongodb+srv://onuralparslan:"+password.password+"@datalogcluster.pyxjkxs.mongodb.net/?appName=dataLogCluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)