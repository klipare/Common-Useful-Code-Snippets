import os
import sys
import json
from configparser import ConfigParser
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore


def read_messages(CONNECTION_STRING, CONSUMER_GROUP, EVENTHUB_NAME, STARTING_POSITION):
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STRING,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME,
    )

    with client:
        client.receive_batch(
            on_event_batch=on_event_batch,
            owner_level=110,
            starting_position=STARTING_POSITION,
        )


def on_event_batch(partition_context, events):
    partition_context.update_checkpoint()
    count = 0
    tmp = []
    for e in events:
        if count < READ_COUNT:
            tmp.append(e.body_as_json())
            count += 1
        else:
            with open(DATA_FILE_PATH, "w") as f:
                f.write(json.dumps(tmp))
            sys.exit()


if __name__ == "__main__":
    # Read Config File parameters
    config = ConfigParser()
    config.read("eh_data_parser.ini")
    READ_COUNT = int(config.get("COMMON", "READ_COUNT"))
    DATA_FILE_PATH = config.get("COMMON", "DATA_FILE_PATH")
    EVENTHUB_NAME = config.get("EH", "EVENTHUB_NAME")
    CONNECTION_STRING = config.get("EH", "CONNECTION_STRING")
    CONSUMER_GROUP = config.get("EH", "CONSUMER_GROUP")
    STARTING_POSITION = config.get("EH", "STARTING_POSITION")

    read_messages(CONNECTION_STRING, CONSUMER_GROUP, EVENTHUB_NAME, STARTING_POSITION)