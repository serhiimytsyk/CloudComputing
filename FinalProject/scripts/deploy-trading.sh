sudo sleep 1
sudo docker pull wurstmeister/kafka
sudo sleep 1
sudo docker tag wurstmeister/kafka 192.168.5.245:5000/kafka
sudo sleep 1
sudo docker push 192.168.5.245:5000/kafka
sudo sleep 1
sudo docker pull wurstmeister/zookeeper
sudo sleep 1
sudo docker tag wurstmeister/zookeeper 192.168.5.245:5000/zookeeper
sudo sleep 1
sudo docker push 192.168.5.245:5000/zookeeper
sudo sleep 1
sudo docker pull couchdb
sudo sleep 1
sudo docker tag couchdb 192.168.5.245:5000/database
sudo sleep 1
sudo docker push 192.168.5.245:5000/database
sudo sleep 1
sudo docker build --no-cache -t trading-bot1 ../trading-bot1
sudo sleep 1
sudo docker tag trading-bot1 192.168.5.245:5000/trading-bot1
sudo sleep 1
sudo docker push 192.168.5.245:5000/trading-bot1
sudo sleep 1
sudo docker build --no-cache -t exchange ../exchange
sudo sleep 1
sudo docker tag exchange 192.168.5.245:5000/exchange
sudo sleep 1
sudo docker push 192.168.5.245:5000/exchange
sudo sleep 1
sudo docker build --no-cache -t database-consumer ../database-consumer
sudo sleep 1
sudo docker tag database-consumer 192.168.5.245:5000/database-consumer
sudo sleep 1
sudo docker push 192.168.5.245:5000/database-consumer
sudo sleep 1
sudo docker build --no-cache -t order-fetcher ../profit-analyzer
sudo sleep 1
sudo docker tag order-fetcher 192.168.5.245:5000/order-fetcher
sudo sleep 1
sudo docker push 192.168.5.245:5000/order-fetcher
sudo sleep 1
sudo kubectl apply -f ../Deployment/zookeeper-deployment.yaml
sudo sleep 1
sudo kubectl apply -f ../Deployment/kafka-deployment.yaml
sudo sleep 1
sudo kubectl apply -f ../Deployment/database-deployment.yaml
sudo sleep 1
sudo kubectl apply -f ../Deployment/database-consumer-deployment.yaml
sudo sleep 1
sudo kubectl apply -f ../Service/zookeeper-service.yaml
sudo sleep 1
sudo kubectl apply -f ../Service/kafka-service.yaml
sudo sleep 1
sudo kubectl apply -f ../Service/database-service.yaml
sudo sleep 1
sudo kubectl apply -f ../Job/exchange-job.yaml
sudo sleep 1
sudo kubectl apply -f ../Job/trading-bot1-job.yaml
sudo sleep 1
sudo echo "All services deployed successfully!"
sudo sleep 20
sudo kubectl get pods -A -o wide