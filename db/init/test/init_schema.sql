CREATE SCHEMA IF NOT EXISTS app_schema_test AUTHORIZATION app_user;
GRANT USAGE ON SCHEMA app_schema_test TO app_user;
ALTER USER app_user SET search_path TO app_schema_test;
