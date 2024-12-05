```bash
kubectl logs -f <pod-name>  # check logs
```


## Instructions
```bash
cd PA/FinalProject/scripts
kubectl get pods -A -o wide
kubectl delete job trading-bot1
kubectl delete job exchange
kubectl delete job order-fetcher
kubectl delete deployment database-consumer
bash deploy-trading.sh
kubectl get pods -A -o wide
wait 600 seconds
bash deploy-order-fetcher.sh
kubectl get pods -A -o wide 
kubectl cp default/<pod-name>:/app/bot1.txt ../profit-analyzer/bot1.txt
sudo nano ../profit-analyzer/bot1.txt
git add ../profit-analyzer/bot1.txt
git commit -m "profits" 
git push
```