import time
import datetime
import json
import random
from configparser import ConfigParser
from azure.eventhub import EventHubProducerClient, EventData


def countdown(t, m):
    # Set End Time for Batch Data Load
    seconds_added = datetime.timedelta(seconds=int(t))
    ct = datetime.datetime.now()
    print("Start Time =>", str(ct))
    et = ct + seconds_added
    count = 0
    
    # Send Messages if Current Time is less than End Time
    while ct < et:
        # Display pending duration
        d = (et - ct)
        mins, secs = divmod(d.seconds, 60)
        timer = "{:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        ct = datetime.datetime.now()
        # Send Messages
        eventcount = send_messages(m)
        count += eventcount
    return count


def send_messages(m):
    try:
        # Create Event Hub Producer Client for Batch Data Load
        producer = EventHubProducerClient.from_connection_string(
                        conn_str=CONNECTION_STRING,
                        eventhub_name=EVENTHUB_NAME
                    )
        
        # Create Event Batch
        event_data_batch = producer.create_batch()
        tmp = 0
        
        # Set Random Count of Events for Batch Data Load
        eventcount = random.randrange(1, 9) * m
        while tmp < eventcount:
            try:
                # Add Events to Batch based on random count
                event_data_batch.add(EventData(json.dumps(data)))
                tmp += 1
            except ValueError:
                # Send Event Batch
                producer.send_batch(event_data_batch)

        print("\t %s messages sent" % (eventcount))

    finally:
        # Terminate Event Hub Producer Client
        producer.close()
        return eventcount


if __name__ == "__main__":
    # Read Config File parameters
    config = ConfigParser()
    config.read('eh_data_loader.ini')
    DATA_FILE_PATH = config.get('COMMON', 'DATA_FILE_PATH')
    EVENTHUB_NAME = config.get('EH', 'EVENTHUB_NAME')
    CONNECTION_STRING = config.get('EH', 'CONNECTION_STRING')

    # Create Batch from data file
    with open(DATA_FILE_PATH) as f:
        data = json.load(f)

    # Initialize Countdown
    t = input("Enter time in seconds: ")
    m = input("Enter message multiplier: ")
    count = countdown(int(t), int(m))
    ct = datetime.datetime.now()
    print("End Time =>", str(ct))
    print("Total %s messages were published in %s seconds" % (count, t))
