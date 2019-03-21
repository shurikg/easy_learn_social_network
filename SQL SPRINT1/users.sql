alter session set nls_date_format='DD/MM/YYYY';
DROP table users;
CREATE table users(
    userName VARCHAR(50) PRIMARY KEY,
    password  VARCHAR(50) NOT NULL,
    firstName VARCHAR(50) NOT NULL,
    lastName VARCHAR(50) NOT NULL,
    birthDay Date NOT NULL,
    email VARCHAR(50) NOT NULL,
    gender  VARCHAR(6) NOT NULL
);
