sudo docker rmi -f $(sudo docker images -q)
sudo docker image prune -a
sudo kubectl delete job exchange 
sudo kubectl delete job trading-bot1
sudo kubectl delete deployment database 
sudo kubectl delete deployment database-consumer 
sudo kubectl delete deployment zookeeper 
sudo kubectl delete statefulset kafka

sudo docker pull wurstmeister/kafka
sudo docker tag wurstmeister/kafka 192.168.5.245:5000/kafka
sudo docker push 192.168.5.245:5000/kafka

sudo docker pull wurstmeister/zookeeper
sudo docker tag wurstmeister/zookeeper 192.168.5.245:5000/zookeeper
sudo docker push 192.168.5.245:5000/zookeeper

sudo docker pull couchdb
sudo docker tag couchdb 192.168.5.245:5000/database
sudo docker push 192.168.5.245:5000/database

sudo docker build --no-cache -t trading-bot1 ../trading-bot1
sudo docker tag trading-bot1 192.168.5.245:5000/trading-bot1
sudo docker push 192.168.5.245:5000/trading-bot1

sudo docker build --no-cache -t exchange ../exchange
sudo docker tag exchange 192.168.5.245:5000/exchange
sudo docker push 192.168.5.245:5000/exchange

sudo docker build --no-cache -t database-consumer ../database-consumer
sudo docker tag database-consumer 192.168.5.245:5000/database-consumer
sudo docker push 192.168.5.245:5000/database-consumer

sudo docker build --no-cache -t order-fetcher ../profit-analyzer
sudo docker tag order-fetcher 192.168.5.245:5000/order-fetcher
sudo docker push 192.168.5.245:5000/order-fetcher

sudo kubectl apply -f ../Deployment/zookeeper-deployment.yaml
sudo kubectl apply -f ../Deployment/kafka-deployment.yaml
sudo kubectl apply -f ../Deployment/database-deployment.yaml
sudo kubectl apply -f ../Deployment/database-consumer-deployment.yaml

sudo kubectl apply -f ../Service/zookeeper-service.yaml
sudo kubectl apply -f ../Service/kafka-service.yaml
sudo kubectl apply -f ../Service/database-service.yaml

sudo kubectl apply -f ../Job/exchange-job.yaml
sudo kubectl apply -f ../Job/trading-bot1-job.yaml

sudo echo "All services deployed successfully!"
sudo sleep 20
sudo kubectl get pods -A -o wide