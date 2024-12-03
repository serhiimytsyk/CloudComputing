sudo docker build -t order-fetcher ../profit-analyzer
sudo docker tag order-fetcher 192.168.5.245:5000/order-fetcher
sudo docker push 192.168.5.245:5000/order-fetcher

kubectl apply -f ../Job/order-fetcher-job.yaml

echo "Order fetcher deployed successfully!"