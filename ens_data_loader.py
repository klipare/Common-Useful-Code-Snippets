import os
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import time
import datetime
import json
import random
from azure.eventhub import EventHubProducerClient, EventData
from azure.storage.blob import ContainerClient


def countdown(t, m):
    seconds_added = datetime.timedelta(seconds=int(t))
    ct = datetime.datetime.now()
    print("Start Time =>", str(ct))
    et = ct + seconds_added
    count = 0
    while ct < et:
        d = (et - ct)
        mins, secs = divmod(d.seconds, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        ct = datetime.datetime.now()
        eventcount = send_messages(m)
        count += eventcount
    return count


def send_messages(m):
    try:
        producer = EventHubProducerClient.from_connection_string(
                        conn_str=CONNECTION_STRING,
                        eventhub_name=EVENTHUB_NAME
                    )
        event_data_batch = producer.create_batch()
        tmp = 0
        eventcount = random.randrange(1, 9) * m
        while tmp < eventcount:
            try:
                event_data_batch.add(EventData(json.dumps(data)))
                tmp += 1
            except ValueError:
                producer.send_batch(event_data_batch)
                event_data_batch = producer.create_batch()
        print("\t %s messages sent" % (eventcount))
    finally:
        producer.close()
        return eventcount


if __name__ == "__main__":
    CONNECTION_STRING = "Endpoint=sb://evhn-fxs-daw-hrmz-primary-easx-001.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=m4Iz1yDCFDrMeaFuczbBqS/LBCC6M/NIypvEnDyB5jc="
    EVENTHUB_NAME = "fxs.daw.raw.ens.dev"

    # container = ContainerClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=samlopspkgdly;AccountKey=WwlpY2s5CqmJwyN45njmX6WJ6u33KnGRskFkT4VDrV8YUodgGLNddn5n0rCO+rNo/DHJflyVTCh4SCHBIVp67A==;EndpointSuffix=core.windows.net", container_name = "rawdata")
    with open("ens.json") as f:
        data = json.load(f)
    t = input("Enter time in seconds: ")
    m = input("Enter message multiplier: ")
    count = countdown(int(t), int(m))
    
    ct = datetime.datetime.now()
    print("End Time =>", str(ct))
    print("Total %s messages were published in %s seconds" % (count, t))
