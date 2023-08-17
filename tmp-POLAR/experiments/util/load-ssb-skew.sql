DROP TABLE IF EXISTS lineorder;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS part;
DROP TABLE IF EXISTS supplier;
DROP TABLE IF EXISTS date;
DROP TABLE IF EXISTS locust;
DROP TABLE IF EXISTS lopart;

CREATE TABLE lineorder_tmp (
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

COPY lineorder_tmp FROM '/Users/d-justen/Development/duckdb-polr-experiments/data/ssb/lineorder2.tbl' (DELIMITER '|');
COPY customer FROM '/Users/d-justen/Development/duckdb-polr-experiments/data/ssb/customer2.tbl' (DELIMITER '|');
COPY part FROM '/Users/d-justen/Development/duckdb-polr-experiments/data/ssb/part2.tbl' (DELIMITER '|');
COPY supplier FROM '/Users/d-justen/Development/duckdb-polr-experiments/data/ssb/supplier2.tbl' (DELIMITER '|');
COPY date FROM '/Users/d-justen/Development/duckdb-polr-experiments/data/ssb/date2.tbl' (DELIMITER '|');

UPDATE lineorder_tmp SET lo_custkey = 1 FROM date WHERE d_datekey = lo_orderdate AND d_monthnuminyear BETWEEN 1 AND 3;
UPDATE lineorder_tmp SET lo_partkey = 1 FROM date WHERE d_datekey = lo_orderdate AND d_monthnuminyear BETWEEN 7 AND 9;
UPDATE lineorder_tmp SET lo_suppkey = 1 FROM date WHERE d_datekey = lo_orderdate and d_monthnuminyear IN (1, 2, 7, 8);

CREATE TABLE locust AS SELECT DISTINCT lo_custkey AS lc_locustkey, lo_custkey AS lc_custkey FROM lineorder_tmp;

INSERT INTO locust (
    SELECT 1, c_custkey
    FROM customer
    WHERE c_custkey BETWEEN 1 AND 20
);

CREATE TABLE lopart AS SELECT DISTINCT lo_partkey AS lp_lopartkey, lo_partkey AS lp_partkey from lineorder_tmp;

INSERT INTO lopart (
    SELECT 1, p_partkey
    FROM part
    WHERE p_partkey BETWEEN 1 AND 20
);

CREATE TABLE lineorder AS SELECT * FROM lineorder_tmp ORDER BY lo_orderdate;
DROP TABLE lineorder_tmp;