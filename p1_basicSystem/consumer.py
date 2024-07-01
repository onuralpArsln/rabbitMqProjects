import pika
import time
import random
import sys
import os

def main():
    # mevcut yayına bağlanmak için 
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)


    print(' [*] Waiting for messages. To exit press a key')


    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        # Rastgele süre beklemeye sebep olarak zaman alan işlemi taklit ediyoruz
        time.sleep(0.3 * random.randint(0, 16))
        print(" [x] Done")
        # görev tamamlanınca yenisini al
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # her seferinde tek görev al
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

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