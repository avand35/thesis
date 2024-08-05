-- POLICIES FOR ORDERS TABLE
CREATE MATERIALIZED VIEW o_p1 AS 
SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice, add_noise_date(o_orderdate, 'DAYS', 10) as o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment 
FROM orders;

CREATE MATERIALIZED VIEW o_p2 AS 
SELECT o_orderkey, o_custkey, o_orderstatus, o_totalprice, generalize_date(o_orderdate, 'MONTH') as o_orderdate, o_orderpriority, o_clerk, o_shippriority, o_comment 
FROM orders;

-- POLICIES FOR CUSTOMER TABLE
CREATE MATERIALIZED VIEW c AS 
SELECT *
FROM customer;

CREATE MATERIALIZED VIEW c_p1 AS 
SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, c_acctbal, suppress(c_mktsegment) as c_mktsegment, c_comment 
FROM customer;

CREATE MATERIALIZED VIEW c_p2 AS 
SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, bucketize(c_acctbal, 500.0) as c_acctbal, c_mktsegment, c_comment 
FROM customer;

CREATE MATERIALIZED VIEW c_p3 AS 
SELECT c_custkey, c_name, c_address, c_nationkey, c_phone, generalize_number(c_acctbal, 100.0) as c_acctbal, c_mktsegment, c_comment 
FROM customer;

-- POLICIES FOR LINEITEM TABLE
CREATE MATERIALIZED VIEW l_p1 AS 
SELECT l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, bucketize(l_extendedprice, 250.0) as l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, generalize_date(l_shipdate, 'MONTH') as l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment
FROM lineitem;

CREATE MATERIALIZED VIEW l_p2 AS 
SELECT l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, bucketize_low(l_extendedprice, 250.0) as l_extendedprice_stat, bucketize(l_extendedprice, 250.0) as l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, generalize_date(l_shipdate, 'MONTH') as l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment
FROM lineitem;


CREATE MATERIALIZED VIEW l_p3 AS 
SELECT l_orderkey, l_partkey, l_suppkey, l_linenumber, l_quantity, add_relative_noise(l_extendedprice, 0.05) as l_extendedprice, l_discount, l_tax, l_returnflag, l_linestatus, add_noise_date(l_shipdate, 'DAYS', 10) as l_shipdate, l_commitdate, l_receiptdate, l_shipinstruct, l_shipmode, l_comment
FROM lineitem;