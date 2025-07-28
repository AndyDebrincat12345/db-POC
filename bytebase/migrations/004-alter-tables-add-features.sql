-- Test schema alterations - add columns, modify constraints
ALTER TABLE emails 
ADD COLUMN email_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN verification_token VARCHAR(255) NULL,
ADD COLUMN verified_at TIMESTAMP NULL;

-- Add index for performance
CREATE INDEX idx_emails_verified ON emails(email_verified);

-- Modify existing table structure
ALTER TABLE service_status 
ADD COLUMN health_score INT DEFAULT 100,
ADD COLUMN last_check_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN error_message TEXT NULL;

-- Create a view for active services
CREATE VIEW active_services AS
SELECT 
    id,
    status,
    health_score,
    updated_at,
    last_check_at,
    CASE 
        WHEN health_score >= 90 THEN 'Excellent'
        WHEN health_score >= 70 THEN 'Good'
        WHEN health_score >= 50 THEN 'Fair'
        ELSE 'Poor'
    END as health_rating
FROM service_status 
WHERE status = 'UP' AND health_score > 0;
