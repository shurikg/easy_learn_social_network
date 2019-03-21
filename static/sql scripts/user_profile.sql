alter session set nls_date_format='DD/MM/YYYY';
DROP TABLE IF EXISTS  user_profile;
CREATE TABLE user_profile(
    user_id  VARCHAR(50) PRIMARY KEY,
    birth_date Date NOT NULL,
    gender VARCHAR(6) NOT NULL,
    college_name VARCHAR(50) NOT NULL,
    year_of_study VARCHAR(50) NOT NULL,
    about_me VARCHAR(100) NOT NULL
);