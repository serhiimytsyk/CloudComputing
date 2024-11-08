cd PA/PA3

Show pods: kubectl get pods -A -o wide
Check logs: kubectl logs -f <pod-name>
Remove job: kubectl delete job iot-producer1
Deploy everything: bash deploy.sh



Experiment 1
sudo nano deploy.sh
comment last 4 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_one_1

kubectl delete job iot-producer1
bash deploy.sh
wait 500 seconds
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_one_1.json ./iot_producer/target/iot_producer_one_1.json

Experiment 2
sudo nano deploy.sh
comment last 3 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_two_1

kubectl delete job iot-producer1
kubectl delete job iot-producer2
bash deploy.sh
wait 500 seconds
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_two_1.json ./iot_producer/target/iot_producer_two_1.json

Experiment 3
sudo nano deploy.sh
comment last 2 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_three_1

kubectl delete job iot-producer1
kubectl delete job iot-producer2
kubectl delete job iot-producer3
bash deploy.sh
wait 500 seconds
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_three_1.json ./iot_producer/target/iot_producer_three_1.json

Experiment 4
sudo nano deploy.sh
comment last 1 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_four_1

kubectl delete job iot-producer1
kubectl delete job iot-producer2
kubectl delete job iot-producer3
kubectl delete job iot-producer4
bash deploy.sh
wait 1000 seconds
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_four_1.json ./iot_producer/target/iot_producer_four_1.json

Experiment 5
sudo nano deploy.sh
comment last 0 jobs
sudo nano Job/iot-producer1-job.yaml
Edit id to iot_producer_five_1

kubectl delete job iot-producer1
kubectl delete job iot-producer2
kubectl delete job iot-producer3
kubectl delete job iot-producer4
kubectl delete job iot-producer5
bash deploy.sh
wait 500 seconds
kubectl get pods -A -o wide
kubectl cp default/<pod-name>:/app/output/iot_producer_five_1.json ./iot_producer/target/iot_producer_five_1.json

cd iot_producer/target
git add iot_producer_one_1.json
git add iot_producer_two_1.json
git add iot_producer_three_1.json
git add iot_producer_four_1.json
git add iot_producer_five_1.json
git commit -m "latencies to plot"
git push