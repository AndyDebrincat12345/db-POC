CREATE DATABASE IF NOT EXISTS status_poc;

USE status_poc;
 
CREATE TABLE IF NOT EXISTS service_status (

    id INT AUTO_INCREMENT PRIMARY KEY,

    service_name VARCHAR(100) NOT NULL,

    status ENUM('UP', 'DOWN', 'MAINTENANCE') NOT NULL DEFAULT 'UP',

    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    notes TEXT

);
 
INSERT INTO service_status (service_name, status, notes)

VALUES ('API Gateway', 'UP', 'Running normally');

 