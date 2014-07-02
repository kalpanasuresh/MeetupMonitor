REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-pig-4.5-SNAPSHOT.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-core-4.5-SNAPSHOT.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-hadoop-compat-4.5-SNAPSHOT.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/guava-16.0.1.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/json-simple-1.1.jar';
REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/piggybank.jar';

rsvp = LOAD '/user/hdfs/meetup/data/meetupRSVP/hourly/2014/*/*/*/meetupRSVP*' using com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') as (json:map[]);

--#describe rsvp;
x = foreach rsvp generate (chararray)json#'member'#'member_name' as memberName, (chararray)json#'member'#'photo' as photo, (chararray)json#'member'#'member_id' as memberId,(chararray)json#'response' as response,(chararray)json#'visibility' as visibility ,(chararray)json#'event'#'time' as eventTime, (chararray)json#'event'#'event_url' as eventURL,(chararray)json#'event'#'event_id'as eventId,(chararray)json#'event'#'event_name'as eventName,(chararray)json#'mtime' as mtime,(chararray)json#'guest' as guest , json#'rsvp_id'as rsvpID:chararray,(chararray)json#'venue'#'lon' as venueLon,(chararray)json#'venue'#'venue_name' as venueName,(chararray)json#'venue'#'venue_id' as venueId,(chararray)json#'venue'#'lat' as venueLat, (chararray)json#'group'#'group_name' as groupName,(chararray)json#'group'#'group_city' as groupCity,(chararray)json#'group'#'group_lat' as groupLat,(chararray)json#'group'#'group_urlname' as groupURL, (chararray)json#'group'#'group_country' as groupCntry,(chararray)json#'group'#'group_id' as groupId, json#'group'#'group_topics' as groupTopics:bag{t1:tuple(topic_name:chararray, urlkey:chararray)} ,(chararray)json#'group'#'group_lon' as groupLon;

--#x = foreach x generate rsvpID,Mname, FLATTEN(gt) as gtts;
--#x = foreach x generate rsvpID, Mname,gtts.$0, gtts.$1;
--#DESCRIBE x;
--#dump x;


--#y = foreach x generate groupCity, groupTopics as cgroupTopics:bag{t1:tuple(topicname:chararray, urlkey:chararray)};


--#describe y;

--#m = foreach x generate groupCity, groupTopics;
m = foreach x generate groupCity,groupCntry, groupURL;
--#, org.apache.pig.builtin.BagToTuple(groupTopics) as cgroupTopicsTuple;

--#m = foreach m generate groupCity,groupCntry,groupURL;
--#, cgroupTopicsTuple.urlkey as urlkey:chararray;


--dump m;
--#DESCRIBE m;

by_city = GROUP m By (groupCity,groupCntry);
--#dump by_city;

--DESCRIBE by_city;

group_city= foreach by_city generate group, groupURL;
--#$1 as topic;

group_city = foreach by_city { 
    unique_topics = DISTINCT m.groupURL;
        generate group, unique_topics as segment_cnt;
        };


store group_city into 'hbase://topicBycity'
 using org.apache.pig.backend.hadoop.hbase.HBaseStorage(
  'topics:topic');



--#dump group_city;

--by_topic = Group m by urlkey;


--#describe by_topic;
--group_topic = foreach by_topic generate group, COUNT(m.urlkey);


--#dump group_topic;
--describe group_topic;

