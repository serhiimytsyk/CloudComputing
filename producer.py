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

import tensorflow as tf 
import pandas as pd 
import numpy as np
from tensorflow.keras import layers, models

#from kafka import KafkaProducer  # producer of events

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
#producer = KafkaProducer (bootstrap_servers="192.168.5.97:9092", 
                                          #acks=1,
                                          #api_version=(0, 10, 1))  # wait for leader to write to log

# acquire the CIFAR10 dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range (1): ##################TODO#################################TODO##################################change back to 100
    
    # get the output of the top command
    process = os.popen ("top -n 1 -b")

    # read the contents that we wish to send as topic content
    contents = process.read ()

    ground_truth = y_train[i][0]
    #print('ground truth {}'.format(ground_truth.shape))
    data = x_train[i].tolist()
    #print('data {}'.format(data.shape))

    # send the contents under topic "images". Note that it expects
    # the contents in bytes so we convert it to bytes.
    #

    image = {
        "ID": i,
        "GroundTruth": ground_truth,
        "Data": data
    }

    array_image = list(image.items())
    out_file = open(f"file {i}.json", "w", encoding='utf-8')
    new_image = json.dump(array_image, out_file, indent=6)
    out_file.close()


    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #   
    #producer.send ("images", value=new_image)
    #producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep (1)

# we are done
#producer.close ()