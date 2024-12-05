sudo docker pull wurstmeister/kafka
sudo docker tag wurstmeister/kafka 192.168.5.145:5000/kafka
sudo docker push 192.168.5.145:5000/kafka

sudo docker pull wurstmeister/zookeeper
sudo docker tag wurstmeister/zookeeper 192.168.5.145:5000/zookeeper
sudo docker push 192.168.5.145:5000/zookeeper

sudo docker pull couchdb
sudo docker tag couchdb 192.168.5.145:5000/database
sudo docker push 192.168.5.145:5000/database


sudo docker build -t trading-bot1 ../trading-bot1
sudo docker tag trading-bot1 192.168.5.145:5000/trading-bot1
sudo docker push 192.168.5.145:5000/trading-bot1

sudo docker build -t exchange ../exchange
sudo docker tag exchange 192.168.5.145:5000/exchange
sudo docker push 192.168.5.145:5000/exchange

sudo docker build -t database-consumer ../database-consumer
sudo docker tag database-consumer 192.168.5.145:5000/database-consumer
sudo docker push 192.168.5.145:5000/database-consumer

sudo docker build -t order-fetcher ../profit-analyzer
sudo docker tag order-fetcher 192.168.5.145:5000/order-fetcher
sudo docker push 192.168.5.145:5000/order-fetcher

kubectl apply -f ../Deployment/zookeeper-deployment.yaml
kubectl apply -f ../Deployment/kafka-deployment.yaml
kubectl apply -f ../Deployment/database-deployment.yaml
kubectl apply -f ../Deployment/database-consumer-deployment.yaml
kubectl apply -f ../Service/zookeeper-service.yaml
kubectl apply -f ../Service/kafka-service.yaml
kubectl apply -f ../Service/database-service.yaml

sleep 30
kubectl apply -f ../Job/exchange-job.yaml
kubectl apply -f ../Job/trading-bot1-job.yaml

echo "All services deployed successfully!"