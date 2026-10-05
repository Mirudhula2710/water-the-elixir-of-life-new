-- 3NF Justification:
-- 1. First Normal Form (1NF): All tables have a primary key, and each column contains atomic values (no repeating groups).
-- 2. Second Normal Form (2NF): All tables are in 1NF, and all non-key attributes are fully functionally dependent on the primary key (no partial dependencies).
-- 3. Third Normal Form (3NF): All tables are in 2NF, and there are no transitive dependencies. For example, in the `alert` table, the `severity`, `expected_level`, and `deviation` are dependent on the specific `alert_id`, not on each other or other non-key columns. The `zone_id` is a foreign key, ensuring the zone details are not duplicated in the `alert`, `reading`, or `complaint` tables.

CREATE TABLE zone (
    zone_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) UNIQUE NOT NULL,
    zone_type VARCHAR(50),
    valve_state VARCHAR(20) DEFAULT 'OPEN'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE reading (
    reading_id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id INT NOT NULL,
    water_level DOUBLE NOT NULL,
    flow_rate DOUBLE,
    recorded_at DATETIME NOT NULL,
    FOREIGN KEY (zone_id) REFERENCES zone(zone_id) ON DELETE CASCADE,
    INDEX (zone_id, recorded_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE alert (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id INT NOT NULL,
    reading_id INT NULL,
    severity VARCHAR(20) NOT NULL,
    expected_level DOUBLE,
    deviation DOUBLE,
    message VARCHAR(255),
    gemini_explanation TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    created_at DATETIME NOT NULL,
    resolved_at DATETIME NULL,
    FOREIGN KEY (zone_id) REFERENCES zone(zone_id) ON DELETE CASCADE,
    FOREIGN KEY (reading_id) REFERENCES reading(reading_id) ON DELETE SET NULL,
    INDEX (severity),
    INDEX (zone_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE complaint (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    zone_id INT NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(40) NULL,
    priority VARCHAR(20) NULL,
    triage_note VARCHAR(255) NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'NEW',
    created_at DATETIME NOT NULL,
    FOREIGN KEY (zone_id) REFERENCES zone(zone_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE ticket (
    ticket_id INT AUTO_INCREMENT PRIMARY KEY,
    alert_id INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    notes VARCHAR(255),
    created_at DATETIME NOT NULL,
    resolved_at DATETIME NULL,
    FOREIGN KEY (alert_id) REFERENCES alert(alert_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
