import pika
import time
import random
import sys
import os

import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler


#### Bu pickle okumaların çalışması için doğru adreste olduğuna emin ol

# pickle kullanarak eğitilmiş modeli aldık
with open('logistic_regression_model.pkl', 'rb') as file:
    clf_loaded = pickle.load(file)

# scalar fittingi aldık 
with open('scalar.pickle', 'rb') as f:
    scalar = pickle.load(f)




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
        print(guess)
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

