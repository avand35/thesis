select
	l_orderkey,
	l_extendedprice,
	o_orderdate,
	l_discount,
	o_shippriority
from
	c_p1,
	o_p2,
	l_p1
where
	c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < date '1995-03-01'
	and l_shipdate > date '1995-03-01'