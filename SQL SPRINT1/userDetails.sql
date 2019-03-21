alter session set nls_date_format='DD/MM/YYYY';
DROP table  user_profile;
CREATE table user_profile(
    userId  VARCHAR(50) PRIMARY KEY,
    birthDay Date NOT NULL,
    gender  VARCHAR(6) NOT NULL,
    collegeName VARCHAR(50) NOT NULL,
    yearOfStudy VARCHAR(50) NOT NULL,
    aboutMe VARCHAR(100) NOT NULL
);
