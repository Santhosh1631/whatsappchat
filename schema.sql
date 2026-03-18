CREATE DATABASE IF NOT EXISTS chat_importer;
USE chat_importer;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL UNIQUE,
    INDEX idx_users_name (name)
);

CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    type VARCHAR(20) NOT NULL DEFAULT 'text',
    is_imported BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_messages_timestamp (timestamp),
    INDEX idx_messages_sender_id (sender_id),
    INDEX idx_messages_type (type),
    CONSTRAINT fk_messages_sender
        FOREIGN KEY (sender_id) REFERENCES users(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);
