#!/bin/bash


cd /home/ec2-user/Kalpana/camus/camus-example/target; hadoop jar camus-example-0.1.0-SNAPSHOT-shaded.jar com.linkedin.camus.etl.kafka.CamusJob -P /home/ec2-user/Kalpana/camus/camus-example/src/main/resources/camus.properties


