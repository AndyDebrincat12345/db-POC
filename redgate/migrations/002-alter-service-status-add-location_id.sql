ALTER TABLE service_status
ADD COLUMN location_id INT NULL;

ALTER TABLE service_status
ADD CONSTRAINT fk_service_status_location
FOREIGN KEY (location_id) REFERENCES locations(id);
