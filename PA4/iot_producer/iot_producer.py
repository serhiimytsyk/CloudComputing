#
#
# Author: Aniruddha Gokhale
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, we use the "top" command and use it as producer of events for
#    Kafka. The consumer can be another Python program that reads and dumps the
#    information into a database OR just keeps displaying the incoming events on the
#    command line consumer (or consumers)
#

import os   # need this for popen
import time  # for sleep
import json  # for json conversion
import sys  # For command line arguments

if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

import random  # for random
import cv2  # for blur
import threading  # for two threads

import tensorflow as tf
import pandas as pd
import numpy as np

from kafka import KafkaProducer  # producer of events
from kafka import KafkaConsumer  # consumer of events

producer_id = sys.argv[1]
total_images = 1000
latencies = {}

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer(bootstrap_servers="kafka:9092",
                         acks=0,
                         api_version=(0, 11, 5))  # wait for leader to write to log

consumer = KafkaConsumer(bootstrap_servers="kafka:9092",
                         api_version=(0, 11, 5), consumer_timeout_ms = 15000)

time.sleep(300)

# acquire the CIFAR10 dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

x_train, x_test = x_train / 255.0, x_test / 255.0

x_train = x_train[:total_images]
x_test = x_test[:total_images]
y_train = y_train[:total_images]
y_test = y_test[:total_images]
import gc
gc.collect()

def blur_image(image):
    image = np.uint8(image * 255)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred_image / 255.0


def produce():
    for i in range(total_images):
        # get ground truth and data variables in JSON serializable formats
        ground_truth = int(y_train[i][0])

        # blur image
        blurred_image = blur_image(x_train[i]).tolist()

        # create json
        id = producer_id + "_" + str(i)
        image = {
            "ID": id,
            "GroundTruth": ground_truth,
            "Data": blurred_image
        }
        new_image = json.dumps(image)

        # send the contents under topic "images". Note that it expects
        # the contents in bytes so we convert it to bytes.
        producer.send("images", value=new_image.encode('utf-8'))
        producer.flush()   # try to empty the sending buffer

        # measure request start time in ms with minus sign
        latencies[id] = -int(time.time() * 1000)

        # sleep 500ms
        time.sleep(0.5)

        print("produced", i)
    # we are done
    print("producer is done")
    producer.close()


def consume():
    consumer.subscribe(topics=["prediction"])
    images_left = total_images
    for msg in consumer:
        prediction = json.loads(msg.value.decode('utf-8'))
        prediction_id = str(prediction["ID"])
        print("received a message", msg)
        # Check if it is our image
        if prediction_id.startswith(producer_id + "_"):
            images_left -= 1
            print("consumed", total_images - images_left)
            # measure request end time in ms with plus sign
            latencies[prediction_id] += int(time.time() * 1000)
            if images_left == 0:  # There are no images left
                break
        time.sleep(0.001)
    print("consumer is done")
    consumer.close()


# say we send the contents 100 times after a sleep of 1 sec in between
if __name__ == "__main__":
    # Create two threads
    producer_thread = threading.Thread(target=produce)
    consumer_thread = threading.Thread(target=consume)

    # Start two threads
    producer_thread.start()
    consumer_thread.start()

    # Wait for two threads to complete
    producer_thread.join()
    consumer_thread.join()

    print("completed two threads")

    # Print the results to the file
    with open("/app/output/" + producer_id + ".json", "w") as file:
        json.dump(latencies, file)
    print("done")
