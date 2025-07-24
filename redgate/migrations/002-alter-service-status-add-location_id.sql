ALTER TABLE service_status
ADD COLUMN location_id INT NULL,
ADD CONSTRAINT fk_location FOREIGN KEY (location_id) REFERENCES location(id);
