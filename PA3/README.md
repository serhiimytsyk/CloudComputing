```bash
cd PA/PA3 
kubectl get pods -A -o wide # show pods 
kubectl logs -f <pod-name>  # check logs
kubectl delete job iot-producer1 # remove job
bash deploy.sh # deploy everything
```


## Experiment 1
```bash
sudo nano deploy.sh
comment last 4 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_one_1

```bash
kubectl delete job iot-producer1
kubectl delete job iot-producer2
bash deploy.sh
```
wait 500 seconds  
```bash
kubectl get pods -A -o wide 
kubectl cp default/<pod-name>:/app/output/iot_producer_one_1.json ./iot_producer/target/iot_producer_one_1.json
``` 

## Experiment 2
```bash
sudo nano deploy.sh
comment last 3 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_two_1

```bash
kubectl delete job iot-producer1
kubectl delete job iot-producer2
bash deploy.sh
``` 
wait 500 seconds  
```bash
kubectl get pods -A -o wide  
kubectl cp default/<pod-name>:/app/output/iot_producer_two_1.json ./iot_producer/target/iot_producer_two_1.json 
``` 
## Experiment 3  
```bash
sudo nano deploy.sh
comment last 2 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_three_1

```bash
kubectl delete job iot-producer1
kubectl delete job iot-producer2
kubectl delete job iot-producer3
bash deploy.sh
``` 
wait 500 seconds  
```bash
kubectl get pods -A -o wide  
kubectl cp default/<pod-name>:/app/output/iot_producer_three_1.json ./iot_producer/target/iot_producer_three_1. json   
```
## Experiment 4   
```bash
sudo nano deploy.sh
comment last 1 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_four_1

```bash
kubectl delete job iot-producer1
kubectl delete job iot-producer2
kubectl delete job iot-producer3
kubectl delete job iot-producer4 
bash deploy.sh
wait 1000 seconds
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_four_1.json ./iot_producer/target/iot_producer_four_1.json

## Experiment 5  
```bash
sudo nano deploy.sh
comment last 0 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_five_1

```bash
kubectl delete job iot-producer1
kubectl delete job iot-producer2
kubectl delete job iot-producer3
kubectl delete job iot-producer4 
kubectl delete job iot-producer5 
bash deploy.sh
```
wait 500 seconds  
```bash
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_five_1.json ./iot_producer/target/iot_producer_five_1.json
```

# Git commands 
```bash
cd iot_producer/target 
git add iot_producer_one_1.json 
git add iot_producer_two_1.json 
git add iot_producer_three_1.json
git add iot_producer_four_1.json  
git add iot_producer_five_1.json 
git commit -m "latencies to plot" 
git push
```