DROP TABLE IF EXISTS lineorder;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS date;

CREATE TABLE lineorder (
                           LO_ORDERKEY             integer NOT NULL,
                           LO_LINENUMBER           integer NOT NULL,
                           LO_CUSTKEY              integer NOT NULL,
                           LO_PARTKEY              integer NOT NULL,
                           LO_SUPPKEY              integer NOT NULL,
                           LO_ORDERDATE            integer NOT NULL,
                           LO_ORDERPRIORITY        text,
                           LO_SHIPPRIORITY         integer,
                           LO_QUANTITY             integer,
                           LO_EXTENDEDPRICE        integer,
                           LO_ORDTOTALPRICE        integer,
                           LO_DISCOUNT             integer,
                           LO_REVENUE              integer,
                           LO_SUPPLYCOST           integer,
                           LO_TAX                  integer,
                           LO_COMMITDATE           integer NOT NULL,
                           LO_SHIPMODE             text
);

CREATE TABLE customer (
                          C_CUSTKEY       integer NOT NULL PRIMARY KEY,
                          C_NAME	    text,
                          C_ADDRESS       text,
                          C_CITY          text,
                          C_NATION        text,
                          C_REGION        text,
                          C_PHONE         text,
                          C_MKTSEGMENT    text
);

CREATE TABLE part (
                      P_PARTKEY       integer NOT NULL PRIMARY KEY,
                      P_NAME          text,
                      P_MFGR          text,
                      P_CATEGORY      text,
                      P_BRAND         text,
                      P_COLOR         text,
                      P_TYPE          text,
                      P_SIZE          integer,
                      P_CONTAINER     text
);

CREATE TABLE supplier (
                          S_SUPPKEY    integer NOT NULL PRIMARY KEY,
                          S_NAME	text,
                          S_ADDRESS text,
                          S_CITY text,
                          S_NATION text,
                          S_REGION text,
                          S_PHONE text
);

CREATE TABLE date (
                      D_DATEKEY integer NOT NULL PRIMARY KEY,
                      D_DATE text,
                      D_DAYOFWEEK text,
                      D_MONTH text,
                      D_YEAR integer,
                      D_YEARMONTHNUM integer,
                      D_YEARMONTH text,
                      D_DAYNUMINWEEK integer,
                      D_DAYNUMINMONTH integer,
                      D_DAYNUMINYEAR integer,
                      D_MONTHNUMINYEAR integer,
                      D_WEEKNUMINYEAR integer,
                      D_SELLINGSEASON text,
                      D_LASTDAYINWEEKFL integer,
                      D_LASTDAYINMONTHFL integer,
                      D_HOLIDAYFL integer,
                      D_WEEKDAYFL integer
);

COPY lineorder FROM 'PATHVAR/data/ssb/lineorder.tbl' (DELIMITER '|');
COPY customer FROM 'PATHVAR/data/ssb/customer.tbl' (DELIMITER '|');
COPY part FROM 'PATHVAR/data/ssb/part.tbl' (DELIMITER '|');
COPY supplier FROM 'PATHVAR/data/ssb/supplier.tbl' (DELIMITER '|');
COPY date FROM 'PATHVAR/data/ssb/date.tbl' (DELIMITER '|');
