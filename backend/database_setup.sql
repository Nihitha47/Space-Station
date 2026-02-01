-- Space Station Management System Database Setup
-- Run this script to create the database schema and sample data

-- Create database
CREATE DATABASE IF NOT EXISTS space_station_db;
USE space_station_db;

-- =====================================================
-- Table: crew
-- =====================================================
CREATE TABLE IF NOT EXISTS crew (
    crew_id INT PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100) NOT NULL,
    nationality VARCHAR(100) NOT NULL
);

-- =====================================================
-- Table: mission
-- =====================================================
CREATE TABLE IF NOT EXISTS mission (
    mission_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    purpose VARCHAR(500) NOT NULL,
    crew_id INT NOT NULL,
    FOREIGN KEY (crew_id) REFERENCES crew(crew_id) ON DELETE CASCADE
);

-- =====================================================
-- Table: experiment
-- =====================================================
CREATE TABLE IF NOT EXISTS experiment (
    experiment_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(100) NOT NULL,
    crew_id INT NOT NULL,
    FOREIGN KEY (crew_id) REFERENCES crew(crew_id) ON DELETE CASCADE
);

-- =====================================================
-- Sample Data: crew
-- =====================================================
INSERT INTO crew (crew_id, password, name, role, nationality) VALUES
(1, 'password123', 'John Mitchell', 'Commander', 'USA'),
(2, 'password123', 'Sarah Chen', 'Flight Engineer', 'China'),
(3, 'password123', 'Alexei Volkov', 'Mission Specialist', 'Russia'),
(4, 'password123', 'Maria Santos', 'Scientist', 'Brazil'),
(5, 'password123', 'Yuki Tanaka', 'Pilot', 'Japan');

-- =====================================================
-- Sample Data: mission
-- =====================================================
INSERT INTO mission (name, purpose, crew_id) VALUES
('ISS Maintenance Alpha', 'Routine maintenance and inspection of ISS solar panels', 1),
('Mars Sample Analysis', 'Analyze soil samples from Mars returned by previous missions', 4),
('Spacewalk Training', 'EVA training exercises for new crew members', 3),
('Satellite Repair', 'Repair communication satellite in geostationary orbit', 2),
('Moon Base Preparation', 'Survey and prepare landing site for lunar base construction', 5);

-- =====================================================
-- Sample Data: experiment
-- =====================================================
INSERT INTO experiment (title, status, crew_id) VALUES
('Plant Growth in Microgravity', 'In Progress', 4),
('Protein Crystal Formation', 'Completed', 4),
('Fluid Dynamics Study', 'Planned', 2),
('Bone Density Monitoring', 'In Progress', 4),
('Solar Panel Efficiency Test', 'Completed', 1),
('Water Recycling System', 'In Progress', 2),
('3D Printing in Zero-G', 'Planned', 3);

-- =====================================================
-- Verification Queries
-- =====================================================

-- View all crew members
SELECT * FROM crew;

-- View all missions with crew names
SELECT 
    m.mission_id,
    m.name,
    m.purpose,
    m.crew_id,
    c.name as crew_name
FROM mission m
INNER JOIN crew c ON m.crew_id = c.crew_id;

-- View all experiments with crew names
SELECT 
    e.experiment_id,
    e.title,
    e.status,
    e.crew_id,
    c.name as crew_name
FROM experiment e
INNER JOIN crew c ON e.crew_id = c.crew_id;

-- Count statistics
SELECT 
    'Total Crew Members' as metric, 
    COUNT(*) as count 
FROM crew
UNION ALL
SELECT 
    'Total Missions', 
    COUNT(*) 
FROM mission
UNION ALL
SELECT 
    'Total Experiments', 
    COUNT(*) 
FROM experiment;
