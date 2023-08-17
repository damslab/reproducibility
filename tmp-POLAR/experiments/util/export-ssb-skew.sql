COPY lineorder TO 'PATHVAR/data/ssb-skew/lineorder.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY customer TO 'PATHVAR/data/ssb-skew/customer.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY part TO 'PATHVAR/data/ssb-skew/part.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY supplier TO 'PATHVAR/data/ssb-skew/supplier.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY date TO 'PATHVAR/data/ssb-skew/date.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY locust 'PATHVAR/data/ssb-skew/locust.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY lopart 'PATHVAR/data/ssb-skew/lopart.tbl' ( FORMAT CSV, DELIMITER '|' );
