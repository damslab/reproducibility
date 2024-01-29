COPY lineorder FROM 'PATHVAR/data/ssb/lineorder.tbl' (DELIMITER '|');
COPY customer FROM 'PATHVAR/data/ssb/customer.tbl' (DELIMITER '|');
COPY part FROM 'PATHVAR/data/ssb/part.tbl' (DELIMITER '|');
COPY supplier FROM 'PATHVAR/data/ssb/supplier.tbl' (DELIMITER '|');
COPY date FROM 'PATHVAR/data/ssb/date.tbl' (DELIMITER '|');
