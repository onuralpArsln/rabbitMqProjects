import pika
import time
import random
import sys
import os

import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler


#Pickleleardan modeli al
with open('logistic_regression_model.pkl', 'rb') as file:
    clf_loaded = pickle.load(file)
with open('scalar.pickle', 'rb') as f:
    scalar = pickle.load(f)


#Atlasa bağlan 
from password import yourPasswordHere
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://onuralparslan:"+yourPasswordHere+"@datalogcluster.pyxjkxs.mongodb.net/?appName=dataLogCluster"
client = MongoClient(uri, server_api=ServerApi('1')) 
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

baseDb = client["basedatabase"]
logCol = baseDb["mLlogs"]

def addToDb(message,guess):
    dailyLog = { "message": message, "guess": guess }
    x = logCol.insert_one(dailyLog)

def makeGuess(val:str )-> str:
    global scalar
    global clf_loaded
    val = val.lstrip("b'")
    vals=val.split('/')
    vals.pop()  # sondaki boş elamanı yok et
    print(vals)
    val_array = [float(part) for part in vals]
    new_banknote = np.array([val_array[0], val_array[1], val_array[2], val_array[3]], ndmin=2)
    new_banknote = scalar.transform(new_banknote)
    return f'Prediction:  Class{clf_loaded.predict(new_banknote)[0]}'



def main():
    # mevcut yayına bağlanmak için 
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='auth_queue', durable=True)
    print(' [*] Waiting for messages. To exit press a key')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        guess = makeGuess(str(body))
        print(" [x] Done")
        addToDb(str(body),guess)
        # görev tamamlanınca yenisini al
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # her seferinde tek görev al
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='auth_queue', on_message_callback=callback)

    channel.start_consuming()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

