DROP table userDegree;
CREATE table userDegree(
    degreeId  VARCHAR(50),
    degreeName  VARCHAR(50) ,
    PRIMARY KEY (userId, degreeId)
);
