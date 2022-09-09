#!/bin/bash

source parameters.sh

echo "SYSTEMDS"

systemds code/test/test.dml -config code/conf/ula.xml

echo "SYSTEMML"

source loadSysMLSettings.sh

java ${SYSTEMML_STANDALONE_OPTS} \
    -cp ${sysmlClassPath} \
    -Dlog4j.configuration=file:${LOG4JPROP_SYSML} \
    org.apache.sysml.api.DMLScript \
    -f code/test/test.dml \
    -config code/conf/ula-sysml.xml \

