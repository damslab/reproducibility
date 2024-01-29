COPY lineorder TO 'PATHVAR/data/ssb/lineorder.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY customer TO 'PATHVAR/data/ssb/customer.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY part TO 'PATHVAR/data/ssb/part.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY supplier TO 'PATHVAR/data/ssb/supplier.tbl' ( FORMAT CSV, DELIMITER '|' );
COPY date TO 'PATHVAR/data/ssb/date.tbl' ( FORMAT CSV, DELIMITER '|' );
