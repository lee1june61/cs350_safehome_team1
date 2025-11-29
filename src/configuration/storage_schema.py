"""Database schema definitions for SafeHome configuration."""

SCHEMA_SQL = """
-- Login interfaces table
CREATE TABLE IF NOT EXISTS login_interfaces (
    username TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    interface TEXT NOT NULL,
    access_level INTEGER NOT NULL,
    login_attempts INTEGER DEFAULT 0,
    is_locked BOOLEAN DEFAULT 0,
    password_min_length INTEGER DEFAULT 8,
    password_requires_digit BOOLEAN DEFAULT 1,
    password_requires_special BOOLEAN DEFAULT 0,
    created_at TEXT,
    last_login TEXT,
    PRIMARY KEY (username, interface)
);

-- System settings table
CREATE TABLE IF NOT EXISTS system_settings (
    setting_key TEXT PRIMARY KEY,
    setting_value TEXT
);

-- SafeHome modes table
CREATE TABLE IF NOT EXISTS safehome_modes (
    mode_id INTEGER PRIMARY KEY,
    mode_name TEXT NOT NULL,
    sensor_ids TEXT,
    is_active BOOLEAN DEFAULT 1,
    description TEXT
);

-- Safety zones table
CREATE TABLE IF NOT EXISTS safety_zones (
    zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT NOT NULL,
    sensor_ids TEXT,
    is_armed BOOLEAN DEFAULT 0,
    description TEXT
);

-- Logs table
CREATE TABLE IF NOT EXISTS logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    description TEXT,
    severity TEXT DEFAULT 'INFO',
    user TEXT
);
"""
