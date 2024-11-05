sudo kubeadm reset
sudo rm -fr /etc/cni/net.d
sudo rm -fr ~/.kube

sudo docker tag apache/kafka 192.168.5.173:5000/kafka
sudo docker push 192.168.5.173:5000/kafka

sudo docker tag couchdb 192.168.5.173:5000/database
sudo docker push 192.168.5.173:5000/database

sudo docker build -t inference-consumer ./inference_consumer
sudo docker tag inference-consumer 192.168.5.173:5000/inference-consumer
sudo docker push 192.168.5.173:5000/inference-consumer

sudo docker build -t database-consumer ./db_consumer
sudo docker tag database-consumer 192.168.5.173:5000/database-consumer
sudo docker push 192.168.5.173:5000/database-consumer

sudo docker build -t iot-producer ./iot_producer
sudo docker tag iot-producer 192.168.5.173:5000/iot-producer
sudo docker push 192.168.5.173:5000/iot-producer

kubectl apply -f ./Deployment/database-deployment.yaml
kubectl apply -f ./Deployment/db-consumer-deployment.yaml
kubectl apply -f ./Deployment/inference-consumer-deployment.yaml
kubectl apply -f ./Deployment/kafka-deployment.yaml

kubectl apply -f ./Service/database-service.yaml
kubectl apply -f ./Service/kafka-service.yaml

kubectl apply -f ./Job/iot-producer1-job.yaml

echo "All services deployed successfully!"