#!/bin/bash

java -Xmx14g -Xms110g -Xmn11g \
    -cp "$SYSTEMDS_REPO"/libraries/SystemDS.jar:"$SYSTEMDS_REPO"/libraries/lib/* \
    -Dlog4j.configuration=file:"$SYSTEMDS_REPO"/libraries/log4j-silent.properties \
    org.apache.sysds.api.DMLScript \
    -exec singlenode \
    -debug \
    -config "$SYSTEMDS_REPO"/libraries/SystemDS-config.xml \
    "$@"
