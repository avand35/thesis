SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid <> pg_backend_pid();

SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'thesis'
  AND pid <> pg_backend_pid();

SELECT pg_cancel_backend(pid)
FROM pg_stat_activity
WHERE state = 'active'
  AND pid <> pg_backend_pid();