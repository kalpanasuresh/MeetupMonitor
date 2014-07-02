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
    #producer = SimpleProducer(kafka, batch_send=True,
    #                     batch_send_every_n=20,
    #                    batch_send_every_t=60)

# To consume messages
   # consumer = SimpleConsumer(kafka, "my-group", "meetupRSVP")
    #for message in consumer:
     # print(message)

def on_error(wsoe, error):
    print error

def on_close(wsoe):
    wsoe.on_open = on_open
    wsoe.run_forever()

def on_open(wsoe):
    def run(*args):
#        for i in range(3):
#	     producer = SimpleProducer(kafka, async=True)
#            producer.send_messages("meetupRSVP", ws.recv())
#            time.sleep(1)
#           ws.send("Hello %d" % i)
        time.sleep(1)
        wsoe.close()
        print "thread terminating..."
        #producer = SimpleProducer(kafka, async=True)
        #producer.send_messages("meetupRSVP", ws.recv())
        thread.start_new_thread(run, ())


if __name__ == "__main__":
    websocket.enableTrace(True)
    kafka = KafkaClient("ip-172-31-2-26:9092,ip-172-31-2-26:9093,ip-172-31-2-26:9094")
    producer = SimpleProducer(kafka, async=True)
    wsoe = websocket.WebSocketApp("ws://stream.meetup.com/2/open_events",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    wsoe.on_open = on_open
    wsoe.run_forever()


# To send messages synchronously
#producer = SimpleProducer(kafka)
#producer.send_messages("test", ws.recv())
#producer.send_messages("test", "this method", "is variadic")

# To send messages asynchronously
#producer = SimpleProducer(kafka, async=True)
#producer.send_messages("test", ws.recv())
#ws.run_forever()
# To wait for acknowledgements
# ACK_AFTER_LOCAL_WRITE : server will wait till the data is written to
#                         a local log before sending response
# ACK_AFTER_CLUSTER_COMMIT : server will block until the message is committed
#                            by all in sync replicas before sending a response
#producer = SimpleProducer(kafka, async=False,
 #                         req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
#                          ack_timeout=2000)

#response = producer.send_messages("test",ws.recv() )

#if response:
 #   print(response[0].error)
  #  print(response[0].offset)

# To send messages in batch. You can use any of the available
# producers for doing this. The following producer will collect
# messages in batch and send them to Kafka after 20 messages are
# collected or every 60 seconds
# Notes:
# * If the producer dies before the messages are sent, there will be losses
# * Call producer.stop() to send the messages and cleanup
#producer = SimpleProducer(kafka, batch_send=True,
 #                         batch_send_every_n=20,
  #                        batch_send_every_t=60)

# To consume messages
#consumer = SimpleConsumer(kafka, "my-group", "test")
#for message in consumer:
#    print(message)

#kafka.close()
