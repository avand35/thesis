-- View: public.c

DROP MATERIALIZED VIEW IF EXISTS public.c;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c
TABLESPACE pg_default
AS
 SELECT c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    c_acctbal,
    c_mktsegment,
    c_comment
   FROM customer
WITH DATA;

ALTER TABLE IF EXISTS public.c
    OWNER TO postgres;

GRANT ALL ON TABLE public.c TO PUBLIC;
GRANT ALL ON TABLE public.c TO postgres;

-- View: public.c_p1

DROP MATERIALIZED VIEW IF EXISTS public.c_p1;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p1
TABLESPACE pg_default
AS
 SELECT c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    c_acctbal,
    suppress(c_mktsegment) AS c_mktsegment,
    c_comment
   FROM customer
WITH DATA;

ALTER TABLE IF EXISTS public.c_p1
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p1 TO PUBLIC;
GRANT ALL ON TABLE public.c_p1 TO postgres;

-- c_p2

DROP MATERIALIZED VIEW IF EXISTS public.c_p2;


CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p2
TABLESPACE pg_default
AS
 SELECT c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    generalize_number(c_acctbal, 250) as c_acctbal,
    c_mktsegment,
    c_comment
   FROM customer
WITH DATA;

ALTER TABLE IF EXISTS public.c_p2
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p2 TO PUBLIC;
GRANT ALL ON TABLE public.c_p2 TO postgres;

-- View: public.c_p3

DROP MATERIALIZED VIEW IF EXISTS public.c_p3;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p3
TABLESPACE pg_default
AS
 SELECT c_custkey,
    c_name,
    c_address,
    c_nationkey,
    c_phone,
    generalize_number(c_acctbal, 100) AS c_acctbal,
    c_mktsegment,
    c_comment
   FROM customer
WITH DATA;

ALTER TABLE IF EXISTS public.c_p3
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p3 TO PUBLIC;
GRANT ALL ON TABLE public.c_p3 TO postgres;

-- View: public.c_p4

DROP MATERIALIZED VIEW IF EXISTS public.c_p4;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p4
TABLESPACE pg_default
AS
 SELECT c_custkey,
    c_name,
    c_address,
    c_nationkey,
    blur_phone(c_phone::text) AS c_phone,
    c_acctbal,
    c_mktsegment,
    c_comment
   FROM customer
WITH DATA;

ALTER TABLE IF EXISTS public.c_p4
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p4 TO PUBLIC;
GRANT ALL ON TABLE public.c_p4 TO postgres;