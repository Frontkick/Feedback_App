-- ENUM types
CREATE TYPE user_roles AS ENUM ('manager','employee');
CREATE TYPE sentiments AS ENUM ('positive','neutral','negative');

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(128) UNIQUE NOT NULL,           
    password_hash VARCHAR(256) NOT NULL,
    role user_roles NOT NULL
);

-- Feedbacks table
CREATE TABLE feedbacks (
    id SERIAL PRIMARY KEY,
    manager_id INT NOT NULL REFERENCES users(id),
    employee_id INT NOT NULL REFERENCES users(id),
    strengths TEXT NOT NULL,
    improvements TEXT NOT NULL,
    sentiment sentiments NOT NULL,
    tags TEXT[],                                   -- ARRAY of TEXT
    anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    acknowledged BOOLEAN DEFAULT FALSE,
    employee_comments TEXT                         
);
