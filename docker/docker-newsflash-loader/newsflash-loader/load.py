import os.path

from kafka import KafkaProducer
from kafka.errors import KafkaError


def loadToKafka(json_list, topic, server_list):

    producer = KafkaProducer(bootstrap_servers=server_list)
    for json in json_list:
        producer.send(topic, json)

    producer.flush()

    return

def loadToFile(json_list, filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    filepath = filepath + "output.txt"

    f = open(filepath, 'a')

    for json in json_list:
        f.write(json)

    f.close()
    return