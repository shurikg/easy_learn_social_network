DROP table userDetails;
CREATE table userDetails(
    userId  VARCHAR(50) PRIMARY KEY,
    collegeName VARCHAR(50) NOT NULL,
    yearOfStudy VARCHAR(50) NOT NULL,
    aboutMe VARCHAR(100) NOT NULL
);
