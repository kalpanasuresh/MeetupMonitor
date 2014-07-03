Meetup Monitor
=============

Meetup streaming data is extracted through an Kafka-Python producer API using the websocket client. The RSVPs are streamed through kafka, camus then collects the topics on an hourly bucket and creates a folder structure in HDFS to load the data.
MapReduce job written in Pig aggregates the data and loads to HBase, which can be consumed later by an API call.


  
![Meetup Datapipeline](/Images/MeetupDataPipeline.png)

Here are some sample outputs from the analysis:

# Top 100 Cities:

![Top 100 Cities](/Screenshots/top100City.PNG)

# Top 20 Topics with most RSVP Count:

![Top 20 Topics](/Screenshots/top20Topics.PNG)

# Top 10 grous with most members:

![Top 10 groups](/Screenshots/top10groups.PNG)


Please note: The anlaysis is based on the streaming data collected on and off over the last couple of weeks.


Refer to the [wiki page] (https://github.com/kalpanasuresh/MeetupMonitor/wiki) to setup and run Meetup Monitor



