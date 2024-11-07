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

sudo docker tag strimzi/kafka 192.168.5.173:5000/kafka
sudo docker push 192.168.5.173:5000/kafka

sudo docker tag couchdb 192.168.5.173:5000/database
sudo docker push 192.168.5.173:5000/database

sudo docker tag zookeeper 192.168.5.173:5000/zookeeper
sudo docker push 192.168.5.173:5000/zookeeper

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
kubectl apply -f zookeeper-deployment.yaml

kubectl apply -f ./Service/database-service.yaml
kubectl apply -f ./Service/kafka-service.yaml
kubectl apply -f zookeeper-service.yaml

kubectl apply -f ./Job/iot-producer1-job.yaml

echo "All services deployed successfully!"