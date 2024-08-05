-- ACS Dataset
CREATE MATERIALIZED VIEW a_p1 AS 
SELECT bucketize_1_low(AGEP, 5.0) as AGEP_stat, bucketize_1(AGEP, 5.0) as AGEP, noise_cow(COW, 0.2) as COW, SCHL, MAR, OCCP, POBP, RELP, WKHP, SEX, RAC1P, PWGTP, PINCP 
FROM acs_income;

CREATE MATERIALIZED VIEW a_p2 AS 
SELECT AGEP, COW, bucketize_1_low(SCHL, 2.0) as SCHL_stat, bucketize_1(SCHL, 2.0) as SCHL, noise_mar(MAR, 0.2) as MAR, OCCP, POBP, RELP, WKHP, SEX, RAC1P, PWGTP, PINCP 
FROM acs_income;

CREATE MATERIALIZED VIEW a_p3 AS
SELECT bucketize_1_low(AGEP, 10.0) as AGEP_stat, bucketize_1(AGEP, 10.0) as AGEP, COW, SCHL, noise_mar(MAR, 0.1) as MAR, OCCP, POBP, RELP, WKHP, SEX, RAC1P, PWGTP, PINCP 
FROM acs_income;

CREATE MATERIALIZED VIEW a_p4 AS
SELECT AGEP, noise_cow(COW, 0.1) as COW, bucketize_1_low(SCHL, 4.0) as SCHL_stat, bucketize_1(SCHL, 4.0) as SCHL, MAR, OCCP, POBP, RELP, WKHP, SEX, RAC1P, PWGTP, PINCP 
FROM acs_income;

CREATE MATERIALIZED VIEW a_p5 AS
SELECT bucketize_1_low(AGEP, 5.0) as AGEP_stat, bucketize_1(AGEP, 5.0) as AGEP, COW, bucketize_1_low(SCHL, 2.0) as SCHL_stat, bucketize_1(SCHL, 2.0) as SCHL, MAR, OCCP, POBP, RELP, WKHP, SEX, RAC1P, PWGTP, PINCP 
FROM acs_income;



ALTER TABLE acs_income ALTER column AGEP SET STATISTICS 10000;
ALTER TABLE acs_income ALTER column COW SET STATISTICS 10000;
ALTER TABLE acs_income ALTER column SCHL SET STATISTICS 10000;
ALTER TABLE acs_income ALTER column MAR SET STATISTICS 10000;
ANALYZE acs_income;

ALTER TABLE a_p1 ALTER column AGEP SET STATISTICS 10000;
ALTER TABLE a_p1 ALTER column COW SET STATISTICS 10000;
ALTER TABLE a_p1 ALTER column SCHL SET STATISTICS 10000;
ALTER TABLE a_p1 ALTER column MAR SET STATISTICS 10000;
ALTER TABLE a_p1 ALTER column AGEP_stat SET STATISTICS 10000;
ANALYZE a_p1;

ALTER TABLE a_p2 ALTER column AGEP SET STATISTICS 10000;
ALTER TABLE a_p2 ALTER column COW SET STATISTICS 10000;
ALTER TABLE a_p2 ALTER column SCHL SET STATISTICS 10000;
ALTER TABLE a_p2 ALTER column MAR SET STATISTICS 10000;
ALTER TABLE a_p2 ALTER column SCHL_stat SET STATISTICS 10000;
ANALYZE a_p2;

ALTER TABLE a_p3 ALTER column AGEP SET STATISTICS 10000;
ALTER TABLE a_p3 ALTER column COW SET STATISTICS 10000;
ALTER TABLE a_p3 ALTER column SCHL SET STATISTICS 10000;
ALTER TABLE a_p3 ALTER column MAR SET STATISTICS 10000;
ALTER TABLE a_p3 ALTER column AGEP_stat SET STATISTICS 10000;
ANALYZE a_p3;

ALTER TABLE a_p4 ALTER column AGEP SET STATISTICS 10000;
ALTER TABLE a_p4 ALTER column COW SET STATISTICS 10000;
ALTER TABLE a_p4 ALTER column SCHL SET STATISTICS 10000;
ALTER TABLE a_p4 ALTER column MAR SET STATISTICS 10000;
ALTER TABLE a_p4 ALTER column SCHL_stat SET STATISTICS 10000;
ANALYZE a_p4;

ALTER TABLE a_p5 ALTER column AGEP SET STATISTICS 10000;
ALTER TABLE a_p5 ALTER column COW SET STATISTICS 10000;
ALTER TABLE a_p5 ALTER column SCHL SET STATISTICS 10000;
ALTER TABLE a_p5 ALTER column MAR SET STATISTICS 10000;
ALTER TABLE a_p5 ALTER column AGEP_stat SET STATISTICS 10000;
ALTER TABLE a_p5 ALTER column SCHL_stat SET STATISTICS 10000;
ANALYZE a_p5;