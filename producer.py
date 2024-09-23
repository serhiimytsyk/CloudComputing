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
import time # for sleep
import json # for json conversion

import random # for random
import cv2 # for blur

import tensorflow as tf 
import pandas as pd 
import numpy as np

from kafka import KafkaProducer  # producer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="192.168.5.97:9092", 
                                          acks=1,
                                          api_version=(0,11,5))  # wait for leader to write to log

# acquire the CIFAR10 dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

x_train, x_test = x_train / 255.0, x_test / 255.0

def blur_image(image):
    image = np.uint8(image * 255)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred_image / 255.0

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range (100):
    
    # get the output of the top command
    process = os.popen ("top -n 1 -b")

    # read the contents that we wish to send as topic content
    contents = process.read ()

    # get ground truth and data variables in JSON serializable formats
    ground_truth = int(y_train[i][0])

    # blur image
    #blurred_image = blur_image(x_train[i]).tolist()
    blurred_image = x_train[i].tolist()

    # create json
    image = { ############################### make sure the DB can read this data
        "ID": i,
        "GroundTruth": ground_truth,
        "Data": blurred_image
    }

    # create unique jsons
    #out_file = open(f"images/file {i}.json", "w")
    #new_image = json.dump(image, out_file, indent=6)
    #out_file.close()

    new_image = json.dumps(image)

    # send the contents under topic "images". Note that it expects
    # the contents in bytes so we convert it to bytes.
    #

    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #   
    producer.send ("images", value=new_image.encode('utf-8'))
    producer.flush ()   # try to empty the sending buffer

    #print image.json
    #check logs on broker

    # sleep a second
    time.sleep (1)

# we are done
producer.close ()