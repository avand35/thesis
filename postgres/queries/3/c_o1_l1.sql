select
	l_orderkey,
	sum(get_range_midpoint(NUMRANGE(l_extendedprice)) * (1 - l_discount)) as revenue,
	o_orderdate,
	o_shippriority
from
	customer,
	o_p1,
	l_p1
where
	c_mktsegment = 'FURNITURE'
	and c_custkey = o_custkey
	and l_orderkey = o_orderkey
	and o_orderdate < date '1995-03-25'
	and l_shipdate > date '1995-03-01'
group by
	l_orderkey,
	o_orderdate,
	o_shippriority
order by
	revenue desc,
	o_orderdate