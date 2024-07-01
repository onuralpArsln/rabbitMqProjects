
# pika rabbitMQ için py clienti
import pika
import sys

#cihazındaki lokal hostta yürütülen rabbitMQ serverine bir bağlantı at
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# rabbitMQ da bir sürü kuyruk olabilir. bu yüzden isimlendir.
# durable parametresi ile sistem kapanırsa güç yeniden geldiğinde de mesajlar korunacak
channel.queue_declare(queue='task_queue', durable=True)


for i in range(10):
    message = "Mesaj no: "+ str(i)


    ## bir exhange oluşturup fanout yapsaydık her mesaj her consumera giderdi. Biz tek consumera atacağız.
    # routing key hangi kuyruğa attığımız

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # mesajları güc kaybında koru
    ))

    print(" [x] Sent %r" % message)

# mesaj gönderme işi bitince bağlantı kapanacak
connection.close()