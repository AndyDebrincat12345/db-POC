-- Disable foreign key checks to avoid dependency errors
SET FOREIGN_KEY_CHECKS = 0;

-- Drop tables if they exist, drop child tables before parents
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS service_status;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS users;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;
