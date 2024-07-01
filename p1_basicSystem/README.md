Bu klasörde basit bir rabbitMQ uygulaması görülmektedir.

producer.py dosyası belirtilen kuyruğa bir çok mesaj gönderecek.

receiver.py dosyası ise kuyruktan sırayla mesajları alacak ve işleyecek. Ancak bu gösterim amaçlı bir çalışma olduğu için her mesajı işlerken işlem yoğunluğunu taklit etmesi için random süreleri wait komutları olacak.

Birden fazla terminalde vir çok receiver çalıştırarak dene.

Sistemin çalışması için öncelikle rabbitMq kur ve lokal olarak çalıştır.

pip3 install pika ile pika kur

> rabbitmq-server

komutu ile çalıştırabilirsin

rabbitmqctl list_queues

ile kuyrukları gör
