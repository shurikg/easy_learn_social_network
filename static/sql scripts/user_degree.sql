DROP TABLE IF EXISTS user_degree;
CREATE table user_degree(
	CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES user_profile(user_id),
	CONSTRAINT fk_degree_id FOREIGN KEY (degree_id) REFERENCES degree(degree_id),
	PRIMARY KEY (user_id, degree_id)
);