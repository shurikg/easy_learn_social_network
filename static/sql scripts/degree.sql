<<<<<<< HEAD
DROP table degree;
CREATE table degree(
    degreeId  VARCHAR(50) PRIMARY KEY,
    degreeName  VARCHAR(50)  NOT NULL
=======
DROP table userDegree;
CREATE table userDegree(
    degreeId  VARCHAR(50),
    degreeName  VARCHAR(50) ,
    PRIMARY KEY (userId, degreeId)
>>>>>>> f6425e8932fc13e54585820df2216ffdcfc4461e
);
