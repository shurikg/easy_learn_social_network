DROP table userCourses;
CREATE table userCourses(
    CONSTRAINT fk_userId FOREIGN KEY (userId) REFERENCES userDetails(userId),
    CONSTRAINT fk_courseId FOREIGN KEY (courseId) REFERENCES courses(courseId),
    PRIMARY KEY (userId, courseId )
);
