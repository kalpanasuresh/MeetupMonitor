	REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-pig-4.5-SNAPSHOT.jar';
	REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-core-4.5-SNAPSHOT.jar';
	REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/elephant-bird-hadoop-compat-4.5-SNAPSHOT.jar';
	REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/guava-16.0.1.jar';
	REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/json-simple-1.1.jar';
	REGISTER '/home/ec2-user/Kalpana/HI-labs/hadoop-dev/lib/piggybank.jar';

	rsvp = LOAD '/user/hdfs/meetup/data/meetupRSVP/hourly/2014/*/*/*/meetupRSVP*' using com.twitter.elephantbird.pig.load.JsonLoader('-nestedLoad') as (json:map[]);

	x = foreach rsvp generate (chararray)json#'member'#'member_name' as memberName, (chararray)json#'member'#'photo' as photo, (chararray)json#'member'#'member_id' as 
	memberId,(chararray)json#'response' as response,(chararray)json#'visibility' as visibility ,(chararray)json#'event'#'time' as eventTime, (chararray)json#'event'#'event_url' as 
	eventURL,(chararray)json#'event'#'event_id'as eventId,(chararray)json#'event'#'event_name'as eventName,(chararray)json#'mtime' as mtime,(chararray)json#'guest' as guest , json#'rsvp_id'as 
	rsvpID:chararray,(chararray)json#'venue'#'lon' as venueLon,(chararray)json#'venue'#'venue_name' as venueName,(chararray)json#'venue'#'venue_id' as venueId,(chararray)json#'venue'#'lat' as 
	venueLat, (chararray)json#'group'#'group_name' as groupName,(chararray)json#'group'#'group_city' as groupCity,(chararray)json#'group'#'group_lat' as 
	groupLat,(chararray)json#'group'#'group_urlname' as groupURL, (chararray)json#'group'#'group_country' as groupCntry,(chararray)json#'group'#'group_id' as groupId, 
	json#'group'#'group_topics' as groupTopics:bag{t1:tuple(topic_name:chararray, urlkey:chararray)} ,(chararray)json#'group'#'group_lon' as groupLon;


	m = foreach x generate groupURL,memberId;


	group_member= Group m by (groupURL);

    --count total members by group
	count_members = foreach group_member { 
					unique_memberId = DISTINCT m.memberId;
					generate group, COUNT(unique_memberId) as segment_cnt;
					};

	count_member_filter = FILTER count_members BY segment_cnt > 10;


	B =  ORDER count_member_filter BY $1 DESC;
	lim = LIMIT B 20;

	store lim into 'hbase://top10groups'
	 using org.apache.pig.backend.hadoop.hbase.HBaseStorage('cf:$1');





