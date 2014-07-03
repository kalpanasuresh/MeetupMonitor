Meetup Monitor
=============

Meetup streaming data is extracted through an Kafka-Python producer API using the websocket client. The RSVPs are streamed through kafka, camus then collects the topics on an hourly bucket and creates a folder structure in HDFS to load the data.
MapReduce job written in Pig aggregates the data and loads to HBase, which can be consumed later by an API call.


  
![Meetup Datapipeline](/Images/MeetupDataPipeline.png)


Refer to the [wiki page] (https://github.com/kalpanasuresh/MeetupMonitor/wiki) to setup and run Meetup Monitor
