v][]
-- create and initialize the database 
CREATE DATABASE IF NOT EXISTS tiriji_database;
USE tiriji_database;


-- create table program add with fields: program_id, title, description, image_url, created_at
CREATE TABLE program (
    program_id INT PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    program_description VARCHAR(255),
    created_at TIMESTAMP
);


-- create table volunteer with fields: first_name, last_name, email, phone_number, created_at, occupation, program_id, id_pass_no, start_date, end_date, emergency_contact_name, emergency_contact_phone, statement_of_intent
CREATE TABLE volunteer (
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    created_at TIMESTAMP,
    occupation VARCHAR(100),
    program_id INT,
    id_pass_no VARCHAR(20) NOT NULL INDEX,
    starting_date DATE,
    end_date DATE,
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    statement_of_intent TEXT,
    FOREIGN KEY (program_id) REFERENCES program(program_id)
);

-- create table events with fields: event_id, title, event_description, event_date, event_location, created_at, program_id
CREATE TABLE events(
    event_id INT PRIMARY KEY ,
    title VARCHAR(50),
    event_description VARCHAR(255),
    event_date DATE NOT NULL,
    event_location VARCHAR(50),
    created_at TIMESTAMP,
    program_id INT,
    FOREIGN KEY(program_id) REFERENCES program(program_id)
);

-- create table news with fields: news_id, news_description, image_url, published_at, updated_at, event_id
CREATE TABLE news(
    news_id INT PRIMARY KEY,
    news_description TEXT,
    image_url VARCHAR(255),
    published_at TIMESTAMP,
    updated_at TIMESTAMP,
    event_id INT,
    program_id INT,
    FOREIGN KEY(event_id)REFERENCES events(event_id)
    FOREIGN KEY (program_id) REFERENCES program(program_id)
);

-- create table resources with fields: resource_id, title, file_url, image_url, created_at, updated_at, program_id, event_id 
CREATE TABLE resources(
    resource_id INT PRIMARY KEY,
    title VARCHAR(50),
    file_url VARCHAR(255),
    image_url VARCHAR(255),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    program_id INT,
    event_id INT,
    FOREIGN KEY(program_id)REFERENCES program(program_id),
    FOREIGN KEY(event_id)REFERENCES events(event_id)
);

-- create table employees with fields: first_name, last_name, email, employee_role, phone, id_pass_no, starting_date,date_of_birth, residence, emergency_contact_name, emergency_contact_phone, mergency_contact_email
CREATE TABLE employees(
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) PRIMARY KEY,
    employee_role VARCHAR(50,)
    phone VARCHAR(20),
    id_pass_no VARCHAR(20)
    starting_date DATE,
    date_of_birth DATE,
    residence VARCHAR(50),
    emergency_contact_name VARCHAR(50),
    emergency_contact_phone VARCHAR(20),
    emergency_contact_email VARCHAR(100),
    bio VARCHAR(255)
    
);

-- create table patners with fields : patner_id, name_org, patners_description, image_url, website_url, assigned_member_email
CREATE TABLE patners(
    patner_id INT PRIMARY KEY,
    name_org VARCHAR(50),
    patners_description VARCHAR(250),
    image_url VARCHAR(255),
    website_url VARCHAR(255),
    assigned_member_email VARCHAR(100),
    program_id INT,
    FOREIGN KEY(email_id) REFERENCES email(email_id),
    FOREIGN KEY(program_id)REFERENCES program(program_id)
);

-- create table gallery with fields: image_id, title, gallery_description, created_at, program_id, event_id
CREATE TABLE gallery(
    image_id INT PRIMARY KEY,
    title VARCHAR(50),
    gallery_description VARCHAR(250),
    created_at TIMESTAMP,
    program_id INT,
    event_id INT,
    FOREIGN KEY(program_id) REFERENCES program(program_id),
    FOREIGN KEY(event_id) REFERENCES events(event_id)
);

-- create table donations with fields: donations_id, merchant_reference_id, pesapal_trasaction_id, amount, currency, donation_reason, payment_status, payment_method, donor_email, donor_phone, created_at, updated_at
CREATE TABLE donations(
    donations_id VARCHAR(100) PRIMARY KEY,
    merchant_reference_id VARCHAR(100),
    pesapal_trasaction_id VARCHAR(100),
    amount DECIMAL(10,2),
    currency VARCHAR(5),
    donation_reason VARCHAR(255),
    payment_status VARCHAR(20),
    payment_method VARCHAR(20),
    donor_email VARCHAR(50),
    donor_phone VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,

);

-- create table feedback with fields: feedback_id, first_name, last_name, email, feed_subject, feedback_message, created_at
CREATE TABLE feedback(
    feedback_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    feed_subject VARCHAR(100),
    feedback_message VARCHAR(255),
    created_at TIMESTAMP
);
