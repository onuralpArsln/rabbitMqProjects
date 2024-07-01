
# aslında proje birin hemen hemen aynısı ancak data_banknote değerlerine göre random bi değer uretip atcaz
# bakalım ne tahmin yapacak, değerler en altta verildi

import pika
import sys
import random


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='auth_queue', durable=True)

limMin=[ -7.0421, -13.7731 , -5.2861, -7.8719]
limMax= [ 6.8248 , 12.9516 , 17.9274  , 2.4495]


for i in range(30):
    message = ""

    # verilen min ve max limitler arasında rastgele değer oluşturup / ile ayırarak yan yana yazdık öbür tarafta parse 
    # / karakterine göre yapılacak. 
    for j in range(4):
        random_value= str(random.uniform(limMin[j], limMax[j]))
        message += random_value[:6]
        message += "/"



    channel.basic_publish(
        exchange='',
        routing_key='auth_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  
    ))

    print(" [x] Sent %r" % message)

connection.close()




"""
değerler 

Minimum values for each column:
var     -7.0421
skew   -13.7731
curt    -5.2861
entr    -7.8719
auth     0.0000
dtype: float64

Maximum values for each column:
var      6.8248
skew    12.9516
curt    17.9274
entr     2.4495
auth     1.0000
dtype: float64


"""