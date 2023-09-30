-- Create the database
CREATE DATABASE agency;

-- Switch to the new database
\c agency;

-- Create the Movie table
CREATE TABLE Movie (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date VARCHAR(10) NOT NULL
);

-- Create the Actor table
CREATE TABLE Actor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT,
    gender VARCHAR(50)
);

-- Insert sample data into Movie table
INSERT INTO Movie (title, release_date) VALUES
    ('Movie 1', '2023-09-30'),
    ('Movie 2', '2023-10-15'),
    ('Movie 3', '2023-11-05');

-- Insert sample data into Actor table
INSERT INTO Actor (name, age, gender) VALUES
    ('Actor 1', 30, 'Male'),
    ('Actor 2', 25, 'Female'),
    ('Actor 3', 35, 'Male');

-- Commit changes
COMMIT;
