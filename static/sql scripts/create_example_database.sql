DROP TABLE IF EXISTS chat_message;
DROP TABLE IF EXISTS posts_comments;
DROP TABLE IF EXISTS posts_post;
DROP TABLE IF EXISTS files_file_related_degrees;
DROP TABLE IF EXISTS files_file;
DROP TABLE IF EXISTS users_rules;
DROP TABLE IF EXISTS users_friendrequest;
DROP TABLE IF EXISTS users_privacy;
DROP TABLE IF EXISTS users_profile_friends;
DROP TABLE IF EXISTS users_usercourses_course_id;
DROP TABLE IF EXISTS users_usercourses;
DROP TABLE IF EXISTS users_userdegrees;
DROP TABLE IF EXISTS users_profile;
DROP TABLE IF EXISTS users_course;
DROP TABLE IF EXISTS users_degree;
DROP TABLE IF EXISTS auth_user;

CREATE TABLE auth_user (
    id           INTEGER       NOT NULL
                               PRIMARY KEY AUTOINCREMENT,
    password     VARCHAR (128) NOT NULL,
    last_login   DATETIME,
    is_superuser BOOL          NOT NULL,
    username     VARCHAR (150) NOT NULL
                               UNIQUE,
    first_name   VARCHAR (30)  NOT NULL,
    email        VARCHAR (254) NOT NULL,
    is_staff     BOOL          NOT NULL,
    is_active    BOOL          NOT NULL,
    date_joined  DATETIME      NOT NULL,
    last_name    VARCHAR (150) NOT NULL
);

CREATE TABLE users_degree (
    degree_id   INTEGER      NOT NULL
                             PRIMARY KEY AUTOINCREMENT,
    degree_name VARCHAR (50) NOT NULL
                             UNIQUE
);

CREATE TABLE users_course (
    course_id   INTEGER      NOT NULL
                             PRIMARY KEY AUTOINCREMENT,
    course_name VARCHAR (50) NOT NULL
                             UNIQUE
);

CREATE TABLE users_profile (
    user_id       INTEGER            NOT NULL
                                     PRIMARY KEY
                                     REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    birth_date    DATE               NOT NULL,
    gender        VARCHAR (10)       NOT NULL,
    college_name  VARCHAR (50)       NOT NULL,
    year_of_study [INTEGER UNSIGNED] NOT NULL,
    about_me      TEXT,
    profile_pic   VARCHAR (100)
);

CREATE TABLE users_userdegrees (
    id           INTEGER NOT NULL
                         PRIMARY KEY AUTOINCREMENT,
    degree_id_id INTEGER NOT NULL
                         REFERENCES users_degree (degree_id) DEFERRABLE INITIALLY DEFERRED,
    user_id_id   INTEGER NOT NULL
                         UNIQUE
                         REFERENCES users_profile (user_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE users_usercourses (
    id         INTEGER NOT NULL
                       PRIMARY KEY AUTOINCREMENT,
    user_id_id INTEGER NOT NULL
                       UNIQUE
                       REFERENCES users_profile (user_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE users_usercourses_course_id (
    id             INTEGER NOT NULL
                           PRIMARY KEY AUTOINCREMENT,
    usercourses_id INTEGER NOT NULL
                           REFERENCES users_usercourses (id) DEFERRABLE INITIALLY DEFERRED,
    course_id      INTEGER NOT NULL
                           REFERENCES users_course (course_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE users_profile_friends (
    id              INTEGER NOT NULL
                            PRIMARY KEY AUTOINCREMENT,
    from_profile_id INTEGER NOT NULL
                            REFERENCES users_profile (user_id) DEFERRABLE INITIALLY DEFERRED,
    to_profile_id   INTEGER NOT NULL
                            REFERENCES users_profile (user_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE users_privacy (
    user_id               INTEGER NOT NULL
                                  PRIMARY KEY
                                  REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    privacy_first_name    BOOL    NOT NULL,
    privacy_last_name     BOOL    NOT NULL,
    privacy_email         BOOL    NOT NULL,
    privacy_birth_date    BOOL    NOT NULL,
    privacy_gender        BOOL    NOT NULL,
    privacy_college_name  BOOL    NOT NULL,
    privacy_year_of_study BOOL    NOT NULL,
    privacy_about_me      BOOL    NOT NULL
);

CREATE TABLE users_friendrequest (
    id           INTEGER NOT NULL
                         PRIMARY KEY AUTOINCREMENT,
    from_user_id INTEGER NOT NULL
                         REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    to_user_id   INTEGER NOT NULL
                         REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE users_rules (
    id         INTEGER NOT NULL
                       PRIMARY KEY AUTOINCREMENT,
    text_rules TEXT    NOT NULL
);

CREATE TABLE files_file (
    id          INTEGER       NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    file_name   VARCHAR (30),
    file_type   VARCHAR (10),
    file_url    VARCHAR (100) NOT NULL,
    create_at   DATE,
    upload_at   DATETIME      NOT NULL,
    file_size   VARCHAR (10),
    category_id INTEGER       REFERENCES users_course (course_id) DEFERRABLE INITIALLY DEFERRED,
    owner_id    INTEGER       REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE files_file_related_degrees (
    id        INTEGER NOT NULL
                      PRIMARY KEY AUTOINCREMENT,
    file_id   INTEGER NOT NULL
                      REFERENCES files_file (id) DEFERRABLE INITIALLY DEFERRED,
    degree_id INTEGER NOT NULL
                      REFERENCES users_degree (degree_id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE posts_post (
    id        INTEGER      NOT NULL
                           PRIMARY KEY AUTOINCREMENT,
    category  VARCHAR (50) NOT NULL,
    body      TEXT         NOT NULL,
    date      DATETIME     NOT NULL,
    author_id INTEGER      NOT NULL
                           REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    file_id   INTEGER      UNIQUE
                           REFERENCES files_file (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE posts_comments (
    id           INTEGER  NOT NULL
                          PRIMARY KEY AUTOINCREMENT,
    comment      TEXT     NOT NULL,
    publish_date DATETIME NOT NULL,
    author_id    INTEGER  NOT NULL
                          REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    postId_id    INTEGER  NOT NULL
                          REFERENCES posts_post (id) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE chat_message (
    id                   INTEGER      NOT NULL
                                      PRIMARY KEY AUTOINCREMENT,
    subject              VARCHAR (50) NOT NULL,
    body                 TEXT         NOT NULL,
    sent_at              DATETIME     NOT NULL,
    read_at              DATETIME,
    replied_at           DATETIME,
    sender_deleted_at    DATETIME,
    recipient_deleted_at DATETIME,
    parent_msg_id        INTEGER      REFERENCES chat_message (id) DEFERRABLE INITIALLY DEFERRED,
    recipient_id         INTEGER      NOT NULL
                                      REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED,
    sender_id            INTEGER      NOT NULL
                                      REFERENCES auth_user (id) DEFERRABLE INITIALLY DEFERRED
);

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 1, 'yonicohen', 'Yoni', 'jonbir2@gmail.com', 1, 1, '2019-04-01 07:00:00.000000', 'Cohen');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 1, 'shlomto', 'Shlomi', 'shlomitofahi@gmail.com', 1, 1, '2019-04-01 07:00:00.000000', 'Tofahi');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 1, 'mayha', 'May', 'mayhagbi@gmail.com', 1, 1, '2019-04-01 07:00:00.000000', 'Hagbi');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 1, 'elishalmon', 'Elisha', 'elishalmon@gmail.com', 1, 1, '2019-04-01 07:00:00.000000', 'Shalmon');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'shirsolo', 'Shir', 'shirsolo@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Solomonov');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'matanha', 'Matan', 'matanha@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Hatuel');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'sapirsho', 'Sapir', 'sapirsho@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Shohat');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'danagros', 'Dana', 'danagros@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Gros');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'yoavgo', 'Yoav', 'yoavgon@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Gonen');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'adaml', 'Adam', 'adamlev@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Lev');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'koralbi', 'Koral', 'koralbi@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Bismut');

INSERT INTO auth_user(password, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name)
VALUES ('pbkdf2_sha256$120000$uTLeQHaub8pD$HHm6149thfjKZUHG+A6ohEA8qvIuuuHW6uJiI93/0+I=', 0, 'yarmarom', 'Yarden', 'yarmarom@gmail.com', 0, 1, '2019-04-01 07:00:00.000000', 'Marom');

INSERT INTO users_degree(degree_name)
VALUES ('Software Engineering');

INSERT INTO users_degree(degree_name)
VALUES ('Social Work');

INSERT INTO users_degree(degree_name)
VALUES ('Anthropology');

INSERT INTO users_degree(degree_name)
VALUES ('Art');

INSERT INTO users_degree(degree_name)
VALUES ('Biological Engineering');

INSERT INTO users_degree(degree_name)
VALUES ('Civil Engineering');

INSERT INTO users_degree(degree_name)
VALUES ('Electrical Engineering');

INSERT INTO users_degree(degree_name)
VALUES ('History');

INSERT INTO users_degree(degree_name)
VALUES ('Mathematics');

INSERT INTO users_degree(degree_name)
VALUES ('Psychology');

INSERT INTO users_degree(degree_name)
VALUES ('Data Analytics');

INSERT INTO users_degree(degree_name)
VALUES ('English');

INSERT INTO users_degree(degree_name)
VALUES ('Geology');

INSERT INTO users_degree(degree_name)
VALUES ('Human Resources');

INSERT INTO users_degree(degree_name)
VALUES ('Music');

INSERT INTO users_degree(degree_name)
VALUES ('Physics');

INSERT INTO users_degree(degree_name)
VALUES ('Statistics');

INSERT INTO users_course(course_name)
VALUES ('OOP');

INSERT INTO users_course(course_name)
    VALUES ('Statistic');

INSERT INTO users_course(course_name)
VALUES ('C');

INSERT INTO users_course(course_name)
VALUES ('Java');

INSERT INTO users_course(course_name)
VALUES ('Linear Algebra');

INSERT INTO users_course(course_name)
VALUES ('Infinitesimal and Integral Calculus 1');

INSERT INTO users_course(course_name)
VALUES ('Infinitesimal and Integral Calculus 2');

INSERT INTO users_course(course_name)
VALUES ('Discrete Mathematics');

INSERT INTO users_course(course_name)
VALUES ('Concrete');

INSERT INTO users_course(course_name)
VALUES ('Software Management');

INSERT INTO users_course(course_name)
VALUES ('Physics 1');

INSERT INTO users_course(course_name)
VALUES ('Physics 2');

INSERT INTO users_course(course_name)
VALUES ('Physics 3');

INSERT INTO users_course(course_name)
VALUES ('Computational and Complexity');

INSERT INTO users_course(course_name)
VALUES ('Compilation');

INSERT INTO users_course(course_name)
VALUES ('Automata and Formal Languages');

INSERT INTO users_course(course_name)
VALUES ('Web Programming');

INSERT INTO users_course(course_name)
VALUES ('Computer Communication');

INSERT INTO users_course(course_name)
VALUES ('Linux Programming');

INSERT INTO users_course(course_name)
VALUES ('Operating Systems');

INSERT INTO users_course(course_name)
VALUES ('Accounting');

INSERT INTO users_course(course_name)
VALUES ('Economy');

INSERT INTO users_course(course_name)
VALUES ('Basic Principles of Entrepreneurship');

INSERT INTO users_course(course_name)
VALUES ('Innovation Engineers for Companies and Organizations');

INSERT INTO users_course(course_name)
VALUES ('Business');

INSERT INTO users_course(course_name)
VALUES ('Marketing');

INSERT INTO users_course(course_name)
VALUES ('Graphic design');

INSERT INTO users_course(course_name)
VALUES ('Politics');

INSERT INTO users_course(course_name)
VALUES ('Environment');

INSERT INTO users_course(course_name)
VALUES ('History of Islam');

INSERT INTO users_course(course_name)
VALUES ('Education Systems');

INSERT INTO users_course(course_name)
VALUES ('Regenerative agriculture');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (1, '1992-01-01', 'M', 'SCE', 3, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (2, '1992-01-01', 'M', 'SCE', 3, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (3, '1992-01-01', 'F', 'SCE', 3, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (4, '1990-01-01', 'M', 'SCE', 3, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (5, '1993-01-01', 'F', 'Sapir', 3, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (6, '1990-01-01', 'M', 'SCE', 3, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (7, '1994-01-01', 'F', 'Ben Gurion', 1, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (8, '1991-01-01', 'F', 'Hebrew University', 2, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (9, '1996-01-01', 'M', 'Azrieli', 1, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (10, '1985-01-01', 'M', 'Afeka', 4, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (11, '1990-01-01', 'F', 'Ben Gurion', 5, '');

INSERT INTO users_profile(user_id, birth_date, gender, college_name, year_of_study, about_me)
VALUES (12, '1982-01-01', 'F', 'Ben Gurion', 7, '');

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (1, 1);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (1, 2);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (1, 3);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (1, 4);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (2, 5);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (7, 6);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (9, 7);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (5, 8);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (12, 9);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (15, 10);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (9, 11);

INSERT INTO users_userdegrees(degree_id_id, user_id_id)
VALUES (13, 12);

INSERT INTO users_usercourses(user_id_id)
VALUES (1);

INSERT INTO users_usercourses(user_id_id)
VALUES (2);

INSERT INTO users_usercourses(user_id_id)
VALUES (3);

INSERT INTO users_usercourses(user_id_id)
VALUES (4);

INSERT INTO users_usercourses(user_id_id)
VALUES (5);

INSERT INTO users_usercourses(user_id_id)
VALUES (6);

INSERT INTO users_usercourses(user_id_id)
VALUES (7);

INSERT INTO users_usercourses(user_id_id)
VALUES (8);

INSERT INTO users_usercourses(user_id_id)
VALUES (9);

INSERT INTO users_usercourses(user_id_id)
VALUES (10);

INSERT INTO users_usercourses(user_id_id)
VALUES (11);

INSERT INTO users_usercourses(user_id_id)
VALUES (12);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (1, 1);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (1, 2);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (1, 3);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (1, 4);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (2, 1);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (2, 2);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (2, 3);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (2, 4);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (3, 1);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (3, 2);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (3, 3);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (3, 4);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (4, 1);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (4, 2);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (4, 3);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (4, 4);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (5, 23);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (5, 29);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (6, 12);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (6, 21);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (7, 25);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (7, 11);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (8, 14);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (8, 17);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (9, 17);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (9, 19);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (10, 5);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (10, 7);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (11, 8);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (11, 15);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (12, 19);

INSERT INTO users_usercourses_course_id(usercourses_id, course_id)
VALUES (12, 28);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (1, 2);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (2, 1);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (1, 3);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (3, 1);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (1, 4);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (4, 1);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (1, 5);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (5, 1);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (2, 3);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (3, 2);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (2, 4);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (4, 2);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (3, 4);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (4, 3);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (5, 7);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (7, 5);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (5, 9);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (9, 5);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (6, 9);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (9, 6);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (6, 11);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (11, 6);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (7, 12);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (12, 7);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (7, 3);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (3, 7);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (8, 9);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (9, 8);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (8, 10);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (10, 8);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (9, 1);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (1, 9);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (9, 4);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (4, 9);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (10, 12);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (12, 10);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (10, 2);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (2, 10);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (11, 6);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (6, 11);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (11, 5);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (5, 11);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (12, 4);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (4, 12);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (12, 2);

INSERT INTO users_profile_friends(from_profile_id, to_profile_id)
VALUES (2, 12);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (1, 1, 1, 1, 0, 1, 0, 0, 0);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (2, 1, 1, 1, 0, 0, 1, 1, 1);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (3, 0, 1, 1, 0, 1, 1, 1, 1);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (4, 1, 1, 0, 1, 1, 1, 1, 1);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (5, 1, 1, 1, 1, 1, 0, 0, 0);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (6, 1, 1, 0, 1, 0, 0, 0, 1);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (7, 1, 1, 0, 0, 0, 0, 1, 0);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (8, 1, 1, 1, 1, 1, 1, 1, 1);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (9, 1, 1, 1, 1, 1, 1, 0, 0);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (10, 1, 1, 1, 1, 0, 0, 1, 1);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (11, 1, 1, 1, 0, 1, 1, 0, 0);

INSERT INTO users_privacy(user_id, privacy_first_name, privacy_last_name, privacy_email, privacy_birth_date, privacy_gender, privacy_college_name, privacy_year_of_study, privacy_about_me)
VALUES (12, 1, 1, 1, 0, 0, 1, 1, 0);

INSERT INTO users_rules(text_rules)
VALUES ('1. Do not post a file that is not yours out of the site.');

INSERT INTO users_rules(text_rules)
VALUES ('2. Do not post inappropriate content on the site.');

INSERT INTO users_rules(text_rules)
VALUES ('3. Keep copyright.');

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('OOP', 'Has anyone been to Marina today? I want to complete what I missed', '2019-06-01 09:40:14.440293', 3);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Statistic', 'I am free to help at work 4 for those who want to...', '2019-04-12 09:40:14.440293', 1);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('C', 'Can someone help me with pointers?', '2019-05-17 09:40:14.440293', 4);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Java', 'Publication No. 2 was published', '2019-05-19 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Linear Algebra', 'I have solution for question 1', '2019-05-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Infinitesimal and Integral Calculus 2', 'Does anyone solve the integral?', '2019-05-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Discrete Mathematics', 'I need help with the last exam', '2019-05-12 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Physics 1', 'Who passed the lesson today?', '2019-05-01 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Physics 2', 'What topics will be included in the exam?', '2019-05-29 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Computational and Complexity', '', '2019-05-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Compilation', 'Wow was a tough lesson today!', '2018-12-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Web Programming', 'I need some help with HTML!', '2019-01-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Linux Programming', 'Anyone knows what command ''chmod'' does?', '2019-02-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Accounting', 'There is a date for the last exam, 10/07/2019!', '2018-12-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Basic Principles of Entrepreneurship', '', '2018-11-11 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Business', 'What the date of presentation?', '2018-11-25 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('Politics', 'An important lesson from today''s lecture, do not be politicians!', '2019-05-20 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'Who''s coming to Natalia''s lesson tomorrow?', '2019-05-01 09:40:14.440293', 1);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'I want to go to the beach', '2018-05-12 09:40:14.440293', 2);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'When is Passover vacation?', '2019-02-20 09:40:14.440293', 3);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'Congratulations!', '2019-03-20 09:40:14.440293', 4);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'Do not forget to come to the event tomorrow!', '2019-04-20 09:40:14.440293', 5);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'I''m tired', '2019-05-20 09:40:14.440293', 6);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'Who''s coming to the movies now?', '2019-05-14 09:40:14.440293', 7);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'This week I''m celebrating my birthday, everyone is invited', '2019-05-15 09:40:14.440293', 8);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'Will it be interesting tomorrow at the event?', '2018-09-17 09:40:14.440293', 9);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'I leave at 3 PM from Herzliya to Tel Aviv', '2018-08-20 09:40:14.440293', 10);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'I finished my degree !!!', '2018-06-20 09:40:14.440293', 11);

INSERT INTO posts_post(category, body, date, author_id)
VALUES ('private', 'Who is coming today?', '2019-05-01 09:40:14.440293', 12);
