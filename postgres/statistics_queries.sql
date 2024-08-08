-- -- main statistics query

-- SELECT attname, n_distinct, most_common_vals::text::text[] as most_common_vals, most_common_freqs, histogram_bounds::text::text[] as histogram_bounds FROM pg_stats WHERE tablename=""

-- View: public.c_stat

DROP MATERIALIZED VIEW IF EXISTS public.c_stat;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_stat
TABLESPACE pg_default
AS
 SELECT attname,
    n_distinct,
    most_common_vals::text::text[] AS most_common_vals,
    most_common_freqs,
    histogram_bounds::text::text[] AS histogram_bounds
   FROM pg_stats
  WHERE tablename = 'c'::name
WITH DATA;

ALTER TABLE IF EXISTS public.c_stat
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_stat TO PUBLIC;
GRANT ALL ON TABLE public.c_stat TO postgres;

-- View: public.c_p1_stat

DROP MATERIALIZED VIEW IF EXISTS public.c_p1_stat;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p1_stat
TABLESPACE pg_default
AS
 SELECT attname,
    n_distinct,
    most_common_vals::text::text[] AS most_common_vals,
    most_common_freqs,
    histogram_bounds::text::text[] AS histogram_bounds
   FROM pg_stats
  WHERE tablename = 'c_p1'::name
WITH DATA;

ALTER TABLE IF EXISTS public.c_p1_stat
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p1_stat TO PUBLIC;
GRANT ALL ON TABLE public.c_p1_stat TO postgres;

-- View: public.c_p2_stat

DROP MATERIALIZED VIEW IF EXISTS public.c_p2_stat;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p2_stat
TABLESPACE pg_default
AS
 SELECT attname,
    n_distinct,
    most_common_vals::text::text[] AS most_common_vals,
    most_common_freqs,
    histogram_bounds::text::text[] AS histogram_bounds
   FROM pg_stats
  WHERE tablename = 'c_p2'::name
WITH DATA;

ALTER TABLE IF EXISTS public.c_p2_stat
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p2_stat TO PUBLIC;
GRANT ALL ON TABLE public.c_p2_stat TO postgres;

-- View: public.c_p3_stat

DROP MATERIALIZED VIEW IF EXISTS public.c_p3_stat;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p3_stat
TABLESPACE pg_default
AS
 SELECT attname,
    n_distinct,
    most_common_vals::text::text[] AS most_common_vals,
    most_common_freqs,
    histogram_bounds::text::text[] AS histogram_bounds
   FROM pg_stats
  WHERE tablename = 'c_p3'::name
WITH DATA;

ALTER TABLE IF EXISTS public.c_p3_stat
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p3_stat TO PUBLIC;
GRANT ALL ON TABLE public.c_p3_stat TO postgres;

-- View: public.c_p4_stat

-- DROP MATERIALIZED VIEW IF EXISTS public.c_p4_stat;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.c_p4_stat
TABLESPACE pg_default
AS
 SELECT attname,
    n_distinct,
    most_common_vals::text::text[] AS most_common_vals,
    most_common_freqs,
    histogram_bounds::text::text[] AS histogram_bounds
   FROM pg_stats
  WHERE tablename = 'c_p4'::name
WITH DATA;

ALTER TABLE IF EXISTS public.c_p4_stat
    OWNER TO postgres;

GRANT ALL ON TABLE public.c_p4_stat TO PUBLIC;
GRANT ALL ON TABLE public.c_p4_stat TO postgres;