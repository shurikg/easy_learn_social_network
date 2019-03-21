DROP table userDetails;
CREATE table userDetails(
    userId VARCHAR(9) PRIMARY KEY,
   collegeName VARCHAR(50) NOT NULL,
    yearOfStudy  Number(1) NOT NULL,
    aboutMe VARCHAR(50)
);
