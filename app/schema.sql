CREATE DATABASE IF NOT EXISTS lfadmin;
USE lfadmin;

DROP TABLE IF EXISTS soc.user;

CREATE USER IF NOT EXISTS lfadminUser;
GRANT CREATE ON DATABASE lfadmin TO lfadminUser;
CREATE SCHEMA soc AUTHORIZATION lfadminUser;

CREATE TABLE soc.user (
  id UUID PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
  username STRING NOT NULL UNIQUE,
  password STRING NOT NULL
);
