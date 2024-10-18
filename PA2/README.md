Ansible Playbook
local machine or in virtual environment:
cd PA1/PA2
ansible-playbook -i Inventory -e "@variables.yaml" playbook_master.yaml

Zookeeper & Kafka
vm3:
cd Apps/kafka_2.13-3.6.2 && bin/zookeeper-server-start.sh config/zookeeper.properties
vm3:
cd Apps/kafka_2.13-3.6.2 && bin/kafka-server-start.sh config/server.properties

DB
vm3:
(instructions from https://docs.vultr.com/install-an-apache-couchdb-database-server-on-ubuntu-20-04)
sudo apt update
sudo apt install -y curl apt-transport-https gnupg
curl https://couchdb.apache.org/repo/keys.asc | gpg --dearmor | sudo tee /usr/share/keyrings/couchdb-archive-keyring.gpg >/dev/null 2>&1 source /etc/os-release
echo "deb [signed-by=/usr/share/keyrings/couchdb-archive-keyring.gpg] https://apache.jfrog.io/artifactory/couchdb-deb/ focal main" | sudo tee /etc/apt/sources.list.d/couchdb.list >/dev/null
sudo apt update
sudo apt install -y couchdb

Choose standalone configuration
Change bind address as 0.0.0.0 to support distributed communication with couchDB hosts
sudo nano /opt/couchdb/etc/local.ini
Change bind address as 0.0.0.0
sudo systemctl restart couchdb

Inference
vm3:
cd PA1/PA2/inference_consumer
sudo docker build -t inference_consumer .
sudo docker run -it --network host --rm --name inference_consumer inference_consumer

DB
vm4:
cd PA1/PA2/db_consumer
sudo docker build -t db_consumer .
sudo docker run -it --network host --rm --name db_consumer db_consumer

Experiment with one producer
vm1:
cd PA1/PA2/iot_producer
sudo nano dockerfile (insert iot_producer_one_1)
sudo docker build -t iot_producer_one_1 .
sudo docker run --network host --name iot_producer_one_1 -it -v "$(pwd)"/target:/app/output iot_producer_one_1

Experiment with two producers
vm1:
sudo nano dockerfile (insert iot_producer_two_1)
sudo docker build -t iot_producer_two_1 .
sudo docker run --network host --name iot_producer_two_1 -it -v "$(pwd)"/target:/app/output iot_producer_two_1
vm2:
cd PA/PA2/iot_producer
sudo nano dockerfile (insert iot_producer_two_2)
sudo docker build -t iot_producer_two_2 .
sudo docker run --network host --name iot_producer_two_2 -it -v "$(pwd)"/target:/app/output iot_producer_two_2

Experiment with three producers
vm1:
sudo nano dockerfile (insert iot_producer_three_1)
sudo docker build -t iot_producer_three_1 .
sudo docker run --network host --name iot_producer_three_1 -it -v "$(pwd)"/target:/app/output iot_producer_three_1
vm2:
sudo nano dockerfile (insert iot_producer_three_2)
sudo docker build -t iot_producer_three_2 .
sudo docker run --network host --name iot_producer_three_2 -it -v "$(pwd)"/target:/app/output iot_producer_three_2
vm3:
cd PA1/PA2/iot_producer
sudo nano dockerfile (insert iot_producer_three_3)
sudo docker build -t iot_producer_three_3 .
sudo docker run --network host --name iot_producer_three_3 -it -v "$(pwd)"/target:/app/output iot_producer_three_3

Experiment with four producers
vm1:
sudo nano dockerfile (insert iot_producer_four_1)
sudo docker build -t iot_producer_four_1 .
sudo docker run --network host --name iot_producer_four_1 -it -v "$(pwd)"/target:/app/output iot_producer_four_1
vm2:
sudo nano dockerfile (insert iot_producer_four_2)
sudo docker build -t iot_producer_four_2 .
sudo docker run --network host --name iot_producer_four_2 -it -v "$(pwd)"/target:/app/output iot_producer_four_2
vm3:
sudo nano dockerfile (insert iot_producer_four_3)
sudo docker build -t iot_producer_four_3 .
sudo docker run --network host --name iot_producer_four_3 -it -v "$(pwd)"/target:/app/output iot_producer_four_3
vm4:
cd PA1/PA2/iot_producer
sudo nano dockerfile (insert iot_producer_four_4)
sudo docker build -t iot_producer_four_4 .
sudo docker run --network host --name iot_producer_four_4 -it -v "$(pwd)"/target:/app/output iot_producer_four_4

Saving the results
vm1:
cd target
git add iot_producer_one_1.json
git add iot_producer_two_1.json
git add iot_producer_three_1.json
git add iot_producer_four_1.json
git commit -m "json files with latencies for plotting"
git push
