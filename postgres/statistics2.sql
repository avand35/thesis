-- STATISTICS LEVEL 10000
ALTER TABLE lineitem ALTER column l_orderkey SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_suppkey SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_quantity SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_extendedprice SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_discount SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_tax SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_returnflag SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_linestatus SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_shipdate SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_commitdate SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_receiptdate SET STATISTICS 10000;
ALTER TABLE lineitem ALTER column l_shipmode SET STATISTICS 10000;
ANALYZE lineitem;

ALTER TABLE l_p1 ALTER column l_orderkey SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_suppkey SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_quantity SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_extendedprice SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_discount SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_tax SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_returnflag SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_linestatus SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_shipdate SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_commitdate SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_receiptdate SET STATISTICS 10000;
ALTER TABLE l_p1 ALTER column l_shipmode SET STATISTICS 10000;

ALTER TABLE l_p1 ALTER column l_extendedprice_stat SET STATISTICS 10000;
ANALYZE l_p1;

ALTER TABLE l_p2 ALTER column l_orderkey SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_suppkey SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_quantity SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_extendedprice SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_discount SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_tax SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_returnflag SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_linestatus SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_shipdate SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_commitdate SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_receiptdate SET STATISTICS 10000;
ALTER TABLE l_p2 ALTER column l_shipmode SET STATISTICS 10000;
ANALYZE l_p2;

ALTER TABLE l_p3 ALTER column l_orderkey SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_suppkey SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_quantity SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_extendedprice SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_discount SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_tax SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_returnflag SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_linestatus SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_shipdate SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_commitdate SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_receiptdate SET STATISTICS 10000;
ALTER TABLE l_p3 ALTER column l_shipmode SET STATISTICS 10000;

ALTER TABLE l_p3 ALTER column l_discount_stat SET STATISTICS 10000;
ANALYZE l_p3;


ALTER TABLE customer ALTER column c_custkey SET STATISTICS 10000;
ALTER TABLE customer ALTER column c_nationkey SET STATISTICS 10000;
ALTER TABLE customer ALTER column c_phone SET STATISTICS 10000;
ALTER TABLE customer ALTER column c_acctbal SET STATISTICS 10000;
ALTER TABLE customer ALTER column c_mktsegment SET STATISTICS 10000;
ALTER TABLE customer ALTER column c_comment SET STATISTICS 10000;
ANALYZE customer;

ALTER TABLE c_p1 ALTER column c_custkey SET STATISTICS 10000;
ALTER TABLE c_p1 ALTER column c_nationkey SET STATISTICS 10000;
ALTER TABLE c_p1 ALTER column c_phone SET STATISTICS 10000;
ALTER TABLE c_p1 ALTER column c_acctbal SET STATISTICS 10000;
ALTER TABLE c_p1 ALTER column c_mktsegment SET STATISTICS 10000;
ALTER TABLE c_p1 ALTER column c_comment SET STATISTICS 10000;

ALTER TABLE c_p1 ALTER column c_acctbal_stat SET STATISTICS 10000;
ANALYZE c_p1;

ALTER TABLE c_p2 ALTER column c_custkey SET STATISTICS 10000;
ALTER TABLE c_p2 ALTER column c_nationkey SET STATISTICS 10000;
ALTER TABLE c_p2 ALTER column c_phone SET STATISTICS 10000;
ALTER TABLE c_p2 ALTER column c_acctbal SET STATISTICS 10000;
ALTER TABLE c_p2 ALTER column c_mktsegment SET STATISTICS 10000;
ALTER TABLE c_p2 ALTER column c_comment SET STATISTICS 10000;

ALTER TABLE c_p2 ALTER column c_acctbal_stat SET STATISTICS 10000;
ANALYZE c_p2;

ALTER TABLE orders ALTER column o_orderkey SET STATISTICS 10000;
ALTER TABLE orders ALTER column o_custkey SET STATISTICS 10000;
ALTER TABLE orders ALTER column o_orderdate SET STATISTICS 10000;
ALTER TABLE orders ALTER column o_orderpriority SET STATISTICS 10000;
ALTER TABLE orders ALTER column o_shippriority SET STATISTICS 10000;
ALTER TABLE orders ALTER column o_comment SET STATISTICS 10000;
ANALYZE orders;

ALTER TABLE o_p1 ALTER column o_orderkey SET STATISTICS 10000;
ALTER TABLE o_p1 ALTER column o_custkey SET STATISTICS 10000;
ALTER TABLE o_p1 ALTER column o_orderdate SET STATISTICS 10000;
ALTER TABLE o_p1 ALTER column o_orderpriority SET STATISTICS 10000;
ALTER TABLE o_p1 ALTER column o_shippriority SET STATISTICS 10000;
ALTER TABLE o_p1 ALTER column o_comment SET STATISTICS 10000;
ANALYZE o_p1;

ALTER TABLE o_p2 ALTER column o_orderkey SET STATISTICS 10000;
ALTER TABLE o_p2 ALTER column o_custkey SET STATISTICS 10000;
ALTER TABLE o_p2 ALTER column o_orderdate SET STATISTICS 10000;
ALTER TABLE o_p2 ALTER column o_orderpriority SET STATISTICS 10000;
ALTER TABLE o_p2 ALTER column o_shippriority SET STATISTICS 10000;
ALTER TABLE o_p2 ALTER column o_comment SET STATISTICS 10000;
ANALYZE o_p2;

DO $$ 
DECLARE 
    col_name TEXT;
BEGIN 
    FOR col_name IN (SELECT column_name FROM information_schema.columns WHERE table_name = 'l_p1') 
    LOOP 
        EXECUTE 'ALTER TABLE l_p1 ALTER COLUMN ' || col_name || ' SET STATISTICS 10000;';
    END LOOP; 
END $$;
ANALYZE l_p1;

DO $$ 
DECLARE 
    col_name TEXT;
BEGIN 
    FOR col_name IN (SELECT column_name FROM information_schema.columns WHERE table_name = 'nation') 
    LOOP 
        EXECUTE 'ALTER TABLE nation ALTER COLUMN ' || col_name || ' SET STATISTICS 10000;';
    END LOOP; 
END $$;
ANALYZE nation;

DO $$ 
DECLARE 
    col_name TEXT;
BEGIN 
    FOR col_name IN (SELECT column_name FROM information_schema.columns WHERE table_name = 'region') 
    LOOP 
        EXECUTE 'ALTER TABLE region ALTER COLUMN ' || col_name || ' SET STATISTICS 10000;';
    END LOOP; 
END $$;
ANALYZE region;

DO $$ 
DECLARE 
    col_name TEXT;
BEGIN 
    FOR col_name IN (SELECT column_name FROM information_schema.columns WHERE table_name = 'supplier') 
    LOOP 
        EXECUTE 'ALTER TABLE supplier ALTER COLUMN ' || col_name || ' SET STATISTICS 10000;';
    END LOOP; 
END $$;
ANALYZE supplier;