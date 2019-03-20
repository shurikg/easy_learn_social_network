DROP table userDegree;

CREATE table userDegree(
   
 CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES userDetails(userId),
   
 CONSTRAINT fk_degreeId FOREIGN KEY (degreeId) REFERENCES degree(degreeId),
    
PRIMARY KEY(userId, degreeId)
);
