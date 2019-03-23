DROP TABLE IF EXISTS user_courses;
CREATE TABLE user_courses(
	CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
	CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES courses(course_id),
	PRIMARY KEY (user_id, course_id)
);