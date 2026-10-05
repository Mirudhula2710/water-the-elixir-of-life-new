CREATE DATABASE IF NOT EXISTS water_elixir;
USE water_elixir;

-- Create least-privilege user
-- Replace 'CHANGE_ME' with your secure password when running
CREATE USER IF NOT EXISTS 'water_app_user'@'localhost' IDENTIFIED BY 'CHANGE_ME';

-- Grant required permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON water_elixir.* TO 'water_app_user'@'localhost';

FLUSH PRIVILEGES;
