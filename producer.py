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

x_train, x_test = x_train / 255.0, x_test / 255.0

def blur_image(image):
    image = np.uint8(image * 255)
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    return blurred_image / 255.0

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range (10): ##################TODO#################################TODO##################################change back to 100
    
    # get the output of the top command
    process = os.popen ("top -n 1 -b")

    # read the contents that we wish to send as topic content
    contents = process.read ()

    # randomize image
    index = random.randint(0, 49999)

    # get ground truth and data variables in JSON serializable formats
    ground_truth = int(y_train[index][0])

    # blur image
    blurred_image = (x_train[index]).tolist()

    sharpness_original = cv2.Laplacian(np.uint8(x_train[index] * 255), cv2.CV_64F).var()
    sharpness_blurred = cv2.Laplacian(np.uint8(blurred_image * 255), cv2.CV_64F).var()

    print(f"Sharpness of original image: {sharpness_original}")
    print(f"Sharpness of blurred image: {sharpness_blurred}")
       
    # Check if the blurred image is less sharp
    if sharpness_blurred < sharpness_original:
        print("The image has been blurred successfully.")
    else:
        print("The image does not appear to be blurred.")

    # create json
    image = {
        "ID": index,
        "GroundTruth": ground_truth,
        "Data": blurred_image
    }

    # create unique jsons
    out_file = open(f"file {i}.json", "w")
    new_image = json.dump(image, out_file, indent=6)
    out_file.close()

    # send the contents under topic "images". Note that it expects
    # the contents in bytes so we convert it to bytes.
    #

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