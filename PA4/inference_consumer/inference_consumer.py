import json
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
import numpy as np
import time
import sys
if sys.version_info >= (3, 12, 0):
    import six
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
from kafka import KafkaProducer
(x_train, y_train), (x_test, y_test) = cifar10.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
y_train = y_train.flatten()
y_test = y_test.flatten()
y_train = to_categorical(y_train, num_classes=10)
y_test = to_categorical(y_test, num_classes=10)


def create_cifar10_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(10, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


model = create_cifar10_model()
model.fit(x_train, y_train, epochs=3, batch_size=64,
          validation_data=(x_test, y_test))
model.save_weights('cifar10_model.weights.h5')
test_loss, test_accuracy = model.evaluate(x_test, y_test)
print(f"Test accuracy: {test_accuracy:.4f}")

import gc
del x_train
del x_test
del y_train
del y_test
gc.collect()
x_train = []
x_test = []
y_train = []
y_test = []


consumer = KafkaConsumer(bootstrap_servers="kafka:9092")
consumer.subscribe(topics=["images"])

producer = KafkaProducer(
    bootstrap_servers="kafka:9092", acks=0, api_version=(0, 11, 5))

for msg in consumer:
    req = json.loads(msg.value.decode('utf-8'))
    data = np.array(req['Data'], dtype=np.float32)
    data = np.expand_dims(data, axis=0)
    outputs = model.predict(data)
    prediction = int(np.argmax(outputs, axis=1)[0])
    is_correct = int(prediction == req['GroundTruth'])
    print('predicted:', prediction, '    actual:', req['GroundTruth'], '    correct:', is_correct)
    doc = {'ID': req['ID'], 'prediction': prediction, 'IsCorrect': is_correct}
    producer.send("prediction", value=json.dumps(doc).encode('utf-8'))
    producer.flush()
    time.sleep(0.001)

producer.close()
consumer.close()
