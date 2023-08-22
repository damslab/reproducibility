COPY lineorder FROM 'PATHVAR/data/ssb-skew/lineorder.tbl' (DELIMITER '|');
COPY customer FROM 'PATHVAR/data/ssb-skew/customer.tbl' (DELIMITER '|');
COPY part FROM 'PATHVAR/data/ssb-skew/part.tbl' (DELIMITER '|');
COPY supplier FROM 'PATHVAR/data/ssb-skew/supplier.tbl' (DELIMITER '|');
COPY date FROM 'PATHVAR/data/ssb-skew/date.tbl' (DELIMITER '|');
COPY lopart FROM 'PATHVAR/data/ssb-skew/lopart.tbl' (DELIMITER '|');
COPY locust FROM 'PATHVAR/data/ssb-skew/locust.tbl' (DELIMITER '|');
