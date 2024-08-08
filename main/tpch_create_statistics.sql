-- DROP MATERIALIZED VIEW c_stat;
-- DROP MATERIALIZED VIEW c_p1_stat;
-- DROP MATERIALIZED VIEW c_p3_stat;
-- DROP MATERIALIZED VIEW l_p3_stat;


CREATE MATERIALIZED VIEW c_stat AS
(SELECT attname, n_distinct, most_common_vals::text::text[] as most_common_vals, most_common_freqs, histogram_bounds::text::text[] as histogram_bounds FROM pg_stats WHERE tablename='customer');

CREATE MATERIALIZED VIEW c_p1_stat AS
(SELECT attname, n_distinct, most_common_vals::text::text[] as most_common_vals, most_common_freqs, histogram_bounds::text::text[] as histogram_bounds FROM pg_stats WHERE tablename='c_1');

CREATE MATERIALIZED VIEW c_p3_stat AS
(SELECT attname, n_distinct, most_common_vals::text::text[] as most_common_vals, most_common_freqs, histogram_bounds::text::text[] as histogram_bounds FROM pg_stats WHERE tablename='c_3');

CREATE MATERIALIZED VIEW l_p3_stat AS
(SELECT attname, n_distinct, most_common_vals::text::text[] as most_common_vals, most_common_freqs, histogram_bounds::text::text[] as histogram_bounds FROM pg_stats WHERE tablename='l_3');
