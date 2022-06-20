CREATE DATABASE IF NOT EXISTS Project1;
USE Project1;

DROP TABLE users;
DROP TABLE scales;
DROP TABLE tunings;

CREATE TABLE IF NOT EXISTS users (
	user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS scales (
	scale_id INT NOT NULL AUTO_INCREMENT,
    scale_name VARCHAR(255),
    user_id INT,
    steps VARCHAR(255),
    likes INT,
    PRIMARY KEY (scale_id)
);

CREATE TABLE IF NOT EXISTS tunings (
	tuning_id INT NOT NULL AUTO_INCREMENT,
    tuning_name VARCHAR(255),
    user_id INT,
    tuning VARCHAR(255),
    likes INT,
    strings INT,
    PRIMARY KEY (tuning_id)
);

TRUNCATE TABLE users;
TRUNCATE TABLE scales;
TRUNCATE TABLE tunings;

INSERT INTO users (user_name, password) 
VALUES ("Tim Henson", "123"), ("Yvette Young", "123"), ("Eric Johnson", "123"), ("Alex Sutherland", "123");

INSERT INTO scales (scale_name, user_id, steps, likes) 
VALUES ("Mixolydian", 1, "2,2,1,2,2,1", 3), 
	   ("Minor", 1, "2,1,2,2,1,2", 2),
	   ("Dorian", 2, "2,1,2,2,1", 5), 
       ("Major", 3, "2,2,1,2,2,2", 1), 
       ("Minor Pentatonic", 4, "3,2,2,3", 2),
       ("Major Pentatonic", 4, "2,2,3,2", 2);

INSERT INTO tunings (tuning_name, user_id, tuning, likes, strings) 
VALUES ("Drop D", 1, "6,1,6,11,3,8", 5, 6), 
	   ("Drop C", 1, "4,1,6,11,3,8", 4, 6),
	   ("Open A Add 4", 2, "6,1,8,1,5,8", 7, 6), 
       ("Dadgad", 2, "6,1,6,11,1,6", 4, 6),
       ("Open D", 2, "6,1,6,10,1,6", 3, 6),
       ("Standard 9 string", 3, "5,10,3,8,1,6,11,3,8", 2, 9),
       ("Standard 8 string", 3, "10,3,8,1,6,11,3,8", 3, 8),
       ("Standard 7 string", 3, "3,8,1,6,11,3,8", 3, 7),
       ("Standard", 4, "8,1,6,11,3,8", 4, 6),
       ("Lots of E", 4, "8,8,8,8,8,8", 0, 6); 

SELECT * FROM users;
SELECT * FROM scales;
SELECT * FROM tunings;

SELECT users.user_name AS name, SUM(like_table.likes) AS likes
FROM
	(SELECT scales.user_id AS user, scales.likes AS likes
	FROM scales
	UNION ALL
	SELECT tunings.user_id, tunings.likes
	FROM tunings) AS like_table
RIGHT JOIN users
ON users.user_id = like_table.user
GROUP BY like_table.user;

SELECT users.user_id 
FROM users
WHERE users.user_name="Alex Sutherland"
AND users.password="123"; 