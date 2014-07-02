REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-pig-4.5-SNAPSHOT.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-core-4.5-SNAPSHOT.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-hadoop-compat-4.5-SNAPSHOT.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/guava-16.0.1.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/json-simple-1.1.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/piggybank.jar';

rsvp = LOAD '/user/hdfs/meetup/data/meetupRSVP/hourly/2014/*/*/*/meetupRSVP*' using com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') as (json:map[]);

--#describe rsvp;
x = foreach rsvp generate (chararray)json#'member'#'member_name' as memberName, (chararray)json#'member'#'photo' as photo, (chararray)json#'member'#'member_id' as memberId,(chararray)json#'response' as response,(chararray)json#'visibility' as visibility ,(chararray)json#'event'#'time' as eventTime, (chararray)json#'event'#'event_url' as eventURL,(chararray)json#'event'#'event_id'as eventId,(chararray)json#'event'#'event_name'as eventName,(chararray)json#'mtime' as mtime,(chararray)json#'guest' as guest , json#'rsvp_id'as rsvpID:chararray,(chararray)json#'venue'#'lon' as venueLon,(chararray)json#'venue'#'venue_name' as venueName,(chararray)json#'venue'#'venue_id' as venueId,(chararray)json#'venue'#'lat' as venueLat, (chararray)json#'group'#'group_name' as groupName,(chararray)json#'group'#'group_city' as groupCity,(chararray)json#'group'#'group_lat' as groupLat,(chararray)json#'group'#'group_urlname' as groupURL, (chararray)json#'group'#'group_country' as groupCntry,(chararray)json#'group'#'group_id' as groupId, json#'group'#'group_topics' as groupTopics:bag{t1:tuple(topic_name:chararray, urlkey:chararray)} ,(chararray)json#'group'#'group_lon' as groupLon;


m = foreach x generate eventName,venueName, rsvpID,response;

m_filter= FILTER m BY response == 'yes';



event_topic= Group m_filter by (eventName,venueName);


--dump group_topic;

count_rsvp = foreach event_topic { 
    unique_rsvpID = DISTINCT m_filter.rsvpID;
        generate group, COUNT(unique_rsvpID) as segment_cnt;
        };

count_rsvp_filter = FILTER count_rsvp BY segment_cnt > 10;
--#dump count_rsvp_filter;
--#DESCRIBE group_city;


B =  ORDER count_rsvp_filter BY $1 DESC;
lim = LIMIT B 20;
--#DESCRIBE lim;

--dump lim;

store lim into 'hbase://top20Topics'
 using org.apache.pig.backend.hadoop.hbase.HBaseStorage(
'cf:$1');





