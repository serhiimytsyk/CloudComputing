# PA1
CS 4287 PA 1 Team 17

CIFAR Dependencies/Install Commands:
- mkdir CIFAR10
- wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
- tar -xvzf cifar-10-python.tar.gz
- sudo pip install tensorflow
- sudo pip install numpy
- sudo pip install pandas
- sudo pip install opencv-python
- sudo pip install kafka

Producer side commands:
1. On one terminal window, run ssh vm2
2. On three other terminal windows, run ssh vm1
3. On vm1-1, run bin/zookeeper-server-start.sh config/zookeeper.properties (leave running)
4. On vm1-2, run bin/kafka-server-start.sh config/server.properties (leave running)
5. On vm1-3, run bin/kafka-topics.sh --create --topic images --bootstrap-server 192.168.5.97:9092
6. On vm1-3, run bin/kafka-topics.sh --create --topic prediction --bootstrap-server 192.168.5.97:9092
7. On vm2, run python3 iot_producer/iot_producer.py (leave running)

Consumer side commands:
1. run python3 '/home/cc/PA1/db_consumer/database_consumer.py'
It will start listening to the "images" and "prediction" topics from kafka broker and insert/update entries in couchDB 
database based on received json objects.
