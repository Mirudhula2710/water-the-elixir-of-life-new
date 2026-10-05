-- Seed Zones
INSERT INTO zone (name, zone_type, valve_state) VALUES 
('Hostel Blocks', 'Residential', 'OPEN'),
('Laboratories', 'Academic', 'OPEN'),
('Administration Building', 'Office', 'OPEN'),
('Canteen', 'Dining', 'OPEN');

-- Seed Readings (~5 per zone)
INSERT INTO reading (zone_id, water_level, flow_rate, recorded_at) VALUES 
(1, 99.5, 0.5, '2023-10-01 08:00:00'),
(1, 99.0, 0.5, '2023-10-01 08:05:00'),
(1, 98.5, 0.5, '2023-10-01 08:10:00'),
(1, 98.0, 0.5, '2023-10-01 08:15:00'),
(1, 80.0, 18.0, '2023-10-01 08:20:00'),

(2, 95.0, 0.2, '2023-10-01 08:00:00'),
(2, 94.8, 0.2, '2023-10-01 08:05:00'),
(2, 94.6, 0.2, '2023-10-01 08:10:00'),
(2, 89.0, 5.6, '2023-10-01 08:15:00'),
(2, 88.8, 0.2, '2023-10-01 08:20:00'),

(3, 100.0, 0.0, '2023-10-01 08:00:00'),
(3, 99.9, 0.1, '2023-10-01 08:05:00'),
(3, 99.8, 0.1, '2023-10-01 08:10:00'),
(3, 99.7, 0.1, '2023-10-01 08:15:00'),
(3, 99.6, 0.1, '2023-10-01 08:20:00'),

(4, 90.0, 1.0, '2023-10-01 08:00:00'),
(4, 89.0, 1.0, '2023-10-01 08:05:00'),
(4, 88.0, 1.0, '2023-10-01 08:10:00'),
(4, 77.0, 11.0, '2023-10-01 08:15:00'),
(4, 76.0, 1.0, '2023-10-01 08:20:00');

-- Seed Alerts covering all severities (using new severities per D4: LOW, MEDIUM, HIGH, CRITICAL)
-- Normal -> LOW, Warning -> MEDIUM, Suspected Leak -> HIGH, Critical -> CRITICAL.
INSERT INTO alert (zone_id, reading_id, severity, expected_level, deviation, message, gemini_explanation, status, created_at) VALUES 
(3, 15, 'LOW', 99.6, 0.0, 'Normal operational levels.', 'Levels match the physics model perfectly.', 'RESOLVED', '2023-10-01 08:20:00'),
(2, 9, 'MEDIUM', 94.4, 5.4, 'Warning: Unusually high drain detected.', 'This deviation suggests a minor irregularity such as an unclosed tap.', 'OPEN', '2023-10-01 08:15:00'),
(4, 19, 'HIGH', 87.0, 10.0, 'Suspected Leak: High deviation from expected model.', 'A loss of this volume generally indicates a stuck flush valve or small leak.', 'OPEN', '2023-10-01 08:15:00'),
(1, 5, 'CRITICAL', 97.5, 17.5, 'Critical: Severe water loss detected.', 'This critical deviation points directly to a large pipe rupture. Simulated valve shutoff executed.', 'OPEN', '2023-10-01 08:20:00');

-- Seed Complaints
INSERT INTO complaint (zone_id, description, category, priority, triage_note, status, created_at) VALUES 
(1, 'Water pooling outside the block.', 'Leakage', 'HIGH', 'Triage: Severe water accumulation reported.', 'NEW', '2023-10-01 08:25:00'),
(2, 'Tap in lab 3 is dripping continuously.', 'Maintenance', 'LOW', 'Triage: Minor drip, schedule routine maintenance.', 'NEW', '2023-10-01 08:30:00');

-- Seed Tickets
INSERT INTO ticket (alert_id, status, notes, created_at) VALUES 
(4, 'OPEN', 'Generated automatically by simulated valve shutoff.', '2023-10-01 08:20:00'),
(3, 'OPEN', 'Pending investigation by maintenance staff.', '2023-10-01 08:35:00');
