#!/usr/bin/env python3

import datetime

tp00 = datetime.datetime.now()
import os
import sys
import pandas as pd
tp01 = datetime.datetime.now()

def loadAndQueryPandas(queryNo, pathCustomer, pathOrders, pathLineitem, mktSegUpper, orderDateLower):
    tp0 = datetime.datetime.now()
    
    dfCustomer = pd.read_csv(pathCustomer, sep=",", header=None, engine="c")
    dfOrders = pd.read_csv(pathOrders, sep=",", header=None, engine="c")
    if queryNo == "b":
        dfLineitem = pd.read_csv(pathLineitem, sep=",", header=None, engine="c")
    
    tp1 = datetime.datetime.now()

    dfCustomer.columns = [
        "C_CUSTKEY",
        "C_NAME",
        "C_ADDRESS",
        "C_NATIONKEY",
        "C_PHONE",
        "C_ACCTBAL",
        "C_MKTSEGMENT",
        "C_COMMENT"
    ]
    dfOrders.columns = [
        "O_ORDERKEY",
        "O_CUSTKEY",
        "O_ORDERSTATUS",
        "O_TOTALPRICE",
        "O_ORDERDATE",
        "O_ORDERPRIORITY",
        "O_CLERK",
        "O_SHIPPRIORITY",
        "O_COMMENT"
    ]
    if queryNo == "b":
        dfLineitem.columns = [
            "L_ORDERKEY",
            "L_PARTKEY",
            "L_SUPPKEY",
            "L_LINENUMBER",
            "L_QUANTITY",
            "L_EXTENDEDPRICE",
            "L_DISCOUNT",
            "L_TAX",
            "L_RETURNFLAG",
            "L_LINESTATUS",
            "L_SHIPDATE",
            "L_COMMITDATE",
            "L_RECEIPTDATE",
            "L_SHIPINSTRUCT",
            "L_SHIPMODE",
            "L_COMMENT"
        ]

    if queryNo == "a":
        dfCustomer = dfCustomer[dfCustomer["C_MKTSEGMENT"] <= mktSegUpper]
        dfOrders = dfOrders[["O_CUSTKEY", "O_TOTALPRICE"]][dfOrders["O_ORDERDATE"] >= orderDateLower]
        dfJoined = dfCustomer.merge(dfOrders, left_on="C_CUSTKEY", right_on="O_CUSTKEY", copy=False)
        dfGrouped = dfJoined[[*list(dfCustomer.columns), "O_TOTALPRICE"]].groupby(list(dfCustomer.columns), as_index=False).sum()
    elif queryNo == "b":
        dfCustomer = dfCustomer[["C_CUSTKEY"]][dfCustomer["C_MKTSEGMENT"] <= mktSegUpper]
        dfOrders = dfOrders[dfOrders["O_ORDERDATE"] >= orderDateLower]
        dfJoined1 = dfOrders.merge(dfCustomer, left_on="O_CUSTKEY", right_on="C_CUSTKEY", copy=False)
        dfLineitem = dfLineitem[["L_ORDERKEY", "L_EXTENDEDPRICE"]]
        dfJoined2 = dfJoined1.merge(dfLineitem, left_on="O_ORDERKEY", right_on="L_ORDERKEY", copy=False)
        dfGrouped = dfJoined2[[*list(dfOrders.columns), "L_EXTENDEDPRICE"]].groupby(list(dfOrders.columns), as_index=False).sum()
    
    tp2 = datetime.datetime.now()

    print("\t{}\t{}".format((tp1 - tp0).total_seconds(), (tp2 - tp1).total_seconds()) , file=sys.stderr, end="")
    
    return dfGrouped
    
def loadAndQueryDuckDB(queryNo, pathCustomer, pathOrders, pathLineitem, mktSegUpper, orderDateLower):
    # TODO Explore how to best load data (natively or via pandas).
    # TODO Explore how to best handover data (pandas, numpy) or store it
    # (natively, pandas).

    tp0 = datetime.datetime.now()
    
    sqlCreate = """
        CREATE TABLE ontime(FlightDate DATE, UniqueCarrier VARCHAR, OriginCityName VARCHAR, DestCityName VARCHAR);
        
        CREATE TABLE customer (
            C_CUSTKEY    BIGINT PRIMARY KEY,
            C_NAME       BIGINT,
            C_ADDRESS    BIGINT,
            C_NATIONKEY  BIGINT,
            C_PHONE      BIGINT,
            C_ACCTBAL    DOUBLE,
            C_MKTSEGMENT BIGINT,
            C_COMMENT    BIGINT
        );
        CREATE TABLE orders (
            O_ORDERKEY      BIGINT PRIMARY KEY,
            O_CUSTKEY       BIGINT,
            O_ORDERSTATUS   BIGINT,
            O_TOTALPRICE    DOUBLE,
            O_ORDERDATE     BIGINT,
            O_ORDERPRIORITY BIGINT,
            O_CLERK         BIGINT,
            O_SHIPPRIORITY  BIGINT,
            O_COMMENT       BIGINT
        );
        COPY customer FROM '{}' (AUTO_DETECT TRUE);
        COPY orders FROM '{}' (AUTO_DETECT TRUE);
    """.format(pathCustomer, pathOrders)
    
    if queryNo == "b":
        sqlCreate += """
            CREATE TABLE lineitem (
                L_ORDERKEY      BIGINT,
                L_PARTKEY       BIGINT,
                L_SUPPKEY       BIGINT,
                L_LINENUMBER    BIGINT,
                L_QUANTITY      BIGINT,
                L_EXTENDEDPRICE DOUBLE,
                L_DISCOUNT      DOUBLE,
                L_TAX           DOUBLE,
                L_RETURNFLAG    BIGINT,
                L_LINESTATUS    BIGINT,
                L_SHIPDATE      BIGINT,
                L_COMMITDATE    BIGINT,
                L_RECEIPTDATE   BIGINT,
                L_SHIPINSTRUCT  BIGINT,
                L_SHIPMODE      BIGINT,
                L_COMMENT       BIGINT
            );
            COPY lineitem FROM '{}' (AUTO_DETECT TRUE);
        """.format(pathLineitem)
    
    conDuckDB.execute(sqlCreate)
    
    tp1 = datetime.datetime.now()

    if False:
        if queryNo == "a":
            sqlQuery = """
                COPY(
                    SELECT c.*, SUM(O_TOTALPRICE)
                    FROM customer c, orders
                    WHERE C_CUSTKEY = O_CUSTKEY
                      AND C_MKTSEGMENT <= {}
                      AND O_ORDERDATE >= {}
                    GROUP BY
                      C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL,
                      C_MKTSEGMENT, C_COMMENT
                ) TO '{}' WITH (HEADER 0, DELIMITER ',');
            """.format(mktSegUpper, orderDateLower, pathRes)
        elif queryNo == "b":
            sqlQuery = """
                COPY(
                    SELECT o.*, SUM(L_EXTENDEDPRICE)
                    FROM orders o, lineitem, customer
                    WHERE O_ORDERKEY = L_ORDERKEY
                      AND C_CUSTKEY = O_CUSTKEY
                      AND C_MKTSEGMENT <= {}
                      AND O_ORDERDATE >= {}
                    GROUP BY O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE,
                      O_ORDERDATE, O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY,
                      O_COMMENT
                ) TO '{}' WITH (HEADER 0, DELIMITER ',');
            """.format(mkSegUpper, orderDateLower, pathRes)
            
    if queryNo == "a":
        sqlQuery = """
            SELECT c.*, SUM(O_TOTALPRICE)
            FROM customer c, orders
            WHERE C_CUSTKEY = O_CUSTKEY
              AND C_MKTSEGMENT <= {}
              AND O_ORDERDATE >= {}
            GROUP BY
              C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL,
              C_MKTSEGMENT, C_COMMENT;
        """.format(mktSegUpper, orderDateLower)
    elif queryNo == "b":
        sqlQuery = """
            SELECT o.*, SUM(L_EXTENDEDPRICE)
            FROM orders o, lineitem, customer
            WHERE O_ORDERKEY = L_ORDERKEY
              AND C_CUSTKEY = O_CUSTKEY
              AND C_MKTSEGMENT <= {}
              AND O_ORDERDATE >= {}
            GROUP BY O_ORDERKEY, O_CUSTKEY, O_ORDERSTATUS, O_TOTALPRICE,
              O_ORDERDATE, O_ORDERPRIORITY, O_CLERK, O_SHIPPRIORITY,
              O_COMMENT
        """.format(mktSegUpper, orderDateLower)
        
    dfGrouped = conDuckDB.execute(sqlQuery).fetchdf()
    
    tp2 = datetime.datetime.now()

    print("\t{}\t{}".format((tp1 - tp0).total_seconds(), (tp2 - tp1).total_seconds()) , file=sys.stderr, end="")
    
    return dfGrouped

def loadAndQuery(queryNo, queryEngine, pathCustomer, pathOrders, pathLineitem, mktSegUpper, orderDateLower):
    if queryEngine == "pandas":
        return loadAndQueryPandas(queryNo, pathCustomer, pathOrders, pathLineitem, mktSegUpper, orderDateLower)
    elif queryEngine == "duckdb":
        return loadAndQueryDuckDB(queryNo, pathCustomer, pathOrders, pathLineitem, mktSegUpper, orderDateLower)
    
def trainAndSave(queryNo, dfQueryRes, pathFinalRes):
    df = dfQueryRes

    # -------------------------------------------------------------------------
    # Create tensor
    # -------------------------------------------------------------------------
    
    tp0 = datetime.datetime.now()
    XY = tf.convert_to_tensor(df.values, dtype=tf.float64)
    tp1 = datetime.datetime.now()
    
    # -------------------------------------------------------------------------
    # One-hot encoding
    # -------------------------------------------------------------------------
    # Depending on the query.
    
    if queryNo == "a":
        # Ignore column 0 (C_CUSTKEY).
        # TODO We could save some cbinding by a clever col order.
        X = tf.concat(
            [
                # C_NAME, C_ADDRESS
                tf.gather(XY, [1, 2], axis=1),
                # C_NATIONKEY
                tf.one_hot(tf.gather(XY, 3, axis=1).numpy(), 25, dtype=tf.float64),
                # C_PHONE, C_ACCTBAL
                tf.gather(XY, [4, 5], axis=1),
                # C_MKTSEGMENT
                tf.one_hot(tf.gather(XY, 6, axis=1).numpy(), 5, dtype=tf.float64),
                # C_COMMENT
                tf.gather(XY, [7], axis=1),
            ],
            1
        )
    elif queryNo == "b":
        # Ignore the first column (O_ORDERKEY).
        # TODO We could save some cbinding by a clever col order.
        X = tf.concat(
            [
                # O_CUSTKEY
                tf.gather(XY, [1], axis=1),
                # O_ORDERSTATUS
                tf.one_hot(tf.gather(XY, 2, axis=1).numpy(), 3, dtype=tf.float64),
                # O_TOTALPRICE, O_ORDERDATE
                tf.gather(XY, [3, 4], axis=1),
                # O_ORDERPRIORITY
                tf.one_hot(tf.gather(XY, 5, axis=1).numpy(), 5, dtype=tf.float64),
                # O_CLERK
                # TODO Use one-hot here, but currently it goes OOM then.
                #tf.one_hot(tf.gather(XY, 6, axis=1).numpy(), 1000, dtype=tf.float64),
                tf.gather(XY, [6], axis=1),
                # O_SHIPPRIORITY, O_COMMENT
                tf.gather(XY, [7, 8], axis=1),
            ],
            1
        )

    # -------------------------------------------------------------------------
    # Extract y column
    # -------------------------------------------------------------------------
        
    # For query a: SUM(O_TOTALPRICE)
    # For query b: SUM(L_EXTENDEDPRICE)
    y = tf.gather(XY, [len(df.columns) - 1], axis=1)

    # -------------------------------------------------------------------------
    # Normalize and standardize columns
    # -------------------------------------------------------------------------
    
    X = (X - tf.math.reduce_mean(X, 0)) / tf.math.reduce_std(X, 0);

    # -------------------------------------------------------------------------
    # Linear regression
    # -------------------------------------------------------------------------
    
    X = tf.concat([X, np.ones((len(df), 1))], 1)
    
    numCols = X.get_shape()[1]
  
    # TODO Do we need that for algorithmic correctness (also in Daphne)?
    #scale_lambda[m_ext-1,0] = 0
  
    lamda = tf.constant(
        0.001 * np.ones((numCols, 1), dtype=float),
        dtype=tf.float64,
        shape=[numCols]
    )
    
    A = tf.matmul(X, X, transpose_a=True)
    b = tf.matmul(X, y, transpose_a=True)
    A = tf.where(tf.math.is_nan(A), tf.zeros_like(A), A)
    b = tf.where(tf.math.is_nan(b), tf.zeros_like(b), b)
    A = A + tf.linalg.diag(lamda)
    beta = tf.linalg.solve(A, b)
    
    pd.DataFrame(beta.numpy()).to_csv(pathFinalRes, header=None, index=None)
    
    tp2 = datetime.datetime.now()
    
    print("\t{}\t{}".format((tp1 - tp0).total_seconds(), (tp2 - tp1).total_seconds()), file=sys.stderr, end="")

if __name__ == "__main__":
    print("\t{}".format((tp01 - tp00).total_seconds()), file=sys.stderr, end="")

    # -------------------------------------------------------------------------
    # Parse arguments
    # -------------------------------------------------------------------------

    # TODO Use argparse.

    queryNo = sys.argv[1]
    mode = sys.argv[2]
    queryEngine = sys.argv[3]
    pathCustomer = sys.argv[4]
    pathOrders = sys.argv[5]
    pathLineitem = sys.argv[6]
    pathQueryRes = sys.argv[7]
    pathFinalRes = sys.argv[8]
    mktSegUpper = int(sys.argv[9])
    orderDateLower = int(sys.argv[10])
    
    if queryNo not in ["a", "b"]:
        raise RuntimeError("unknown query number: {}".format(queryNo))
    
    # -------------------------------------------------------------------------
    # Import and configure libs for query part
    # -------------------------------------------------------------------------
    
    if mode in ["query", "both"] and queryEngine == "duckdb":
        tp02 = datetime.datetime.now()
        import duckdb
        conDuckDB = duckdb.connect(database=':memory:', read_only=False) # TODO is this good?
        tp03 = datetime.datetime.now()
        print("\t{}".format((tp03 - tp02).total_seconds()), file=sys.stderr, end="")
        
    # -------------------------------------------------------------------------
    # Import and configure libs for training part
    # -------------------------------------------------------------------------
    
    if mode in ["train", "both"]:
        tp02 = datetime.datetime.now()
        # TODO Check what messages it actually prints, maybe some of that is important.
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
        import tensorflow as tf
        tf.get_logger().setLevel("ERROR")
        tf.config.threading.set_inter_op_parallelism_threads(1)
        tf.config.threading.set_intra_op_parallelism_threads(1)
        import numpy as np
        tp03 = datetime.datetime.now()
        print("\t{}".format((tp03 - tp02).total_seconds()), file=sys.stderr, end="")
    
    # -------------------------------------------------------------------------
    # Execute pipeline (or part of it)
    # -------------------------------------------------------------------------

    queryParams = [queryNo, queryEngine, pathCustomer, pathOrders, pathLineitem, mktSegUpper, orderDateLower]
    if mode == "both":
        dfQueryRes = loadAndQuery(*queryParams)
        trainAndSave(queryNo, dfQueryRes, pathFinalRes)
    elif mode == "query":
        dfQueryRes = loadAndQuery(*queryParams)
        tp0 = datetime.datetime.now()
        dfQueryRes.to_csv(pathQueryRes, header=None, index=None)
        tp1 = datetime.datetime.now()
        print("\t{}".format((tp1 - tp0).total_seconds()), file=sys.stderr, end="")
    elif mode == "train":
        tp0 = datetime.datetime.now()
        dfQueryRes = pd.read_csv(pathQueryRes, sep=",", header=None)
        tp1 = datetime.datetime.now()
        print("\t{}".format((tp1 - tp0).total_seconds()), file=sys.stderr, end="")
        trainAndSave(queryNo, dfQueryRes, pathFinalRes)
    else:
        raise RuntimeError("unknown mode: \"{}\", use \"query\", \"train\", or both".format(mode))
