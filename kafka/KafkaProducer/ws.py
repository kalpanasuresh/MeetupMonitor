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


def on_message(ws, message):  
    producer.send_messages("meetupRSVP", message)
   
def on_error(ws, error):
    print error

def on_close(ws):
    ws.on_open = on_open
    ws.run_forever()

def on_open(ws):
    def run(*args):
        time.sleep(1)
        ws.close()
       
        thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    kafka = KafkaClient("host:9092,host:9093,host:9094")
    producer = SimpleProducer(kafka, async=True)
    ws = websocket.WebSocketApp("ws://stream.meetup.com/2/rsvps",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

