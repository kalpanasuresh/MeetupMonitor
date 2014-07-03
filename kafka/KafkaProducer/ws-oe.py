import websocket
try:
  import thread
except ImportError:
  import _thread as thread
import time

from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from kafka.producer import SimpleProducer, KeyedProducer
from websocket import create_connection


def on_message(wsoe, message):  
    producer.send_messages("openevents", message)
    

def on_error(wsoe, error):
    print error

def on_close(wsoe):
    wsoe.on_open = on_open
    wsoe.run_forever()

def on_open(wsoe):
    def run(*args):
        time.sleep(1)
        wsoe.close()
        thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    kafka = KafkaClient("host:9092,host:9093,host:9094")
    producer = SimpleProducer(kafka, async=True)
    wsoe = websocket.WebSocketApp("ws://stream.meetup.com/2/open_events",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    wsoe.on_open = on_open
    wsoe.run_forever()

