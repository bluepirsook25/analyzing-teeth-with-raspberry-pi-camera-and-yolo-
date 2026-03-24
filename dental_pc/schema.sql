-- database/schema.sql
-- Run once to create the database and table.
-- mysql -u root -p < database/schema.sql

CREATE DATABASE IF NOT EXISTS dental_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE dental_db;

CREATE TABLE IF NOT EXISTS appointments (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    dentist_name     VARCHAR(100)  NOT NULL,
    appointment_time DATETIME      NOT NULL,
    created_at       TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);
