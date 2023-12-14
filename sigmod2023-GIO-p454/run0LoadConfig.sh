#!/bin/bash

export LOG4JPROP='explocal/log4j.properties' 
export CMD="java -Xms120g -Xmx120g -Dlog4j.configuration=file:$LOG4JPROP"

source load-had3.3-java11.sh