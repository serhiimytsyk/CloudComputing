# sudo kubeadm reset
# sudo rm -rf ~/.kube
# sudo rm -rf /etc/cni/net.d/

# sudo swapoff -a
# sudo kubeadm init --apiserver-advertise-address 192.168.5.173 --control-plane-endpoint 192.168.5.173 --pod-network-cidr=10.244.0.0/16
# sudo mkdir -p $HOME/.kube
# sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
# sudo chown $(id -u):$(id -g) $HOME/.kube/config
# sudo kubectl taint nodes --all node-role.kubernetes.io/control-plane-
# sudo systemctl restart kubelet docker containerd
# sudo kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
# sudo systemctl restart kubelet docker containerd

sudo docker tag wurstmeister/kafka 192.168.1.81:5000/team17/kafka
sudo docker push 192.168.1.81:5000/team17/kafka

sudo docker tag couchdb 192.168.1.81:5000/team17/database
sudo docker push 192.168.1.81:5000/team17/database

sudo docker tag wurstmeister/zookeeper 192.168.1.81:5000/team17/zookeeper
sudo docker push 192.168.1.81:5000/team17/zookeeper

sudo docker build -t inference-consumer ./inference_consumer
sudo docker tag inference-consumer 192.168.1.81:5000/team17/inference-consumer
sudo docker push 192.168.1.81:5000/team17/inference-consumer

sudo docker build -t database-consumer ./db_consumer
sudo docker tag database-consumer 192.168.1.81:5000/team17/database-consumer
sudo docker push 192.168.1.81:5000/team17/database-consumer

sudo docker build -t iot-producer ./iot_producer
sudo docker tag iot-producer 192.168.1.81:5000/team17/iot-producer
sudo docker push 192.168.1.81:5000/team17/iot-producer

sudo docker build -f ./Spark/spark_dockerfile -t my-spark .
sudo docker tag my-spark:latest 192.168.1.81:5000/team/my-spark
sudo docker push 192.168.1.81:5000/team17/my-spark

kubectl apply -f ./Spark/spark-master-svc.yaml
kubectl apply -f ./Spark/spark-driver-svc.yaml
kubectl apply -f ./Spark/spark-master-deploy.yaml
kubectl apply -f ./Spark/spark-worker-deploy.yaml
kubectl apply -f ./Spark/spark-driver-deploy.yaml

kubectl apply -f ./Deployment/database-deployment.yaml
kubectl apply -f ./Deployment/db-consumer-deployment.yaml
kubectl apply -f ./Deployment/inference-consumer-deployment.yaml
kubectl apply -f ./Deployment/kafka-deployment.yaml
kubectl apply -f ./Deployment/zookeeper-deployment.yaml

kubectl apply -f ./Service/database-service.yaml
kubectl apply -f ./Service/kafka-service.yaml
kubectl apply -f ./Service/zookeeper-service.yaml

kubectl apply -f ./Job/iot-producer1-job.yaml
#kubectl apply -f ./Job/iot-producer2-job.yaml
#kubectl apply -f ./Job/iot-producer3-job.yaml
#kubectl apply -f ./Job/iot-producer4-job.yaml
#kubectl apply -f ./Job/iot-producer5-job.yaml

echo "All services deployed successfully!"
