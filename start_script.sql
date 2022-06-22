DROP DATABASE Project1;
CREATE DATABASE IF NOT EXISTS Project1;
USE Project1;

CREATE TABLE IF NOT EXISTS users (
	user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(255),
    password VARCHAR(255),
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS scales (
	scale_id INT NOT NULL AUTO_INCREMENT,
    scale_name VARCHAR(255),
    user_id INT NOT NULL,
    steps VARCHAR(255),
    PRIMARY KEY (scale_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tunings (
	tuning_id INT NOT NULL AUTO_INCREMENT,
    tuning_name VARCHAR(255),
    user_id INT NOT NULL,
    tuning VARCHAR(255),
    strings INT,
    PRIMARY KEY (tuning_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tuning_likes (
	like_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    uploader_id INT NOT NULL,
    tuning_id INT NOT NULL,
    PRIMARY KEY (like_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(uploader_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(tuning_id) REFERENCES tunings(tuning_id) ON DELETE CASCADE 
);

CREATE TABLE IF NOT EXISTS scale_likes (
	like_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    uploader_id INT NOT NULL,
    scale_id INT NOT NULL,
    PRIMARY KEY (like_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(uploader_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(scale_id) REFERENCES scales(scale_id) ON DELETE CASCADE
);


INSERT INTO users (user_name, password) 
VALUES ("Tim Henson", "123"), ("Yvette Young", "123"), ("Eric Johnson", "123"), ("Alex Sutherland", "123");

INSERT INTO scales (scale_name, user_id, steps) 
VALUES ("Mixolydian", 1, "2,2,1,2,2,1"), 
	   ("Minor", 1, "2,1,2,2,1,2"),
	   ("Dorian", 2, "2,1,2,2,1"), 
       ("Major", 3, "2,2,1,2,2,2"), 
       ("Minor Pentatonic", 4, "3,2,2,3"),
       ("Major Pentatonic", 4, "2,2,3,2");

INSERT INTO tunings (tuning_name, user_id, tuning, strings) 
VALUES ("Drop D", 1, "6,1,6,11,3,8", 6), 
	   ("Drop C", 1, "4,1,6,11,3,8", 6),
	   ("Open A Add 4", 2, "6,1,8,1,5,8", 6), 
       ("Dadgad", 2, "6,1,6,11,1,6", 6),
       ("Open D", 2, "6,1,6,10,1,6", 6),
       ("Standard 9 string", 3, "5,10,3,8,1,6,11,3,8", 9),
       ("Standard 8 string", 3, "10,3,8,1,6,11,3,8", 8),
       ("Standard 7 string", 3, "3,8,1,6,11,3,8", 7),
       ("Standard", 4, "8,1,6,11,3,8", 6),
       ("Lots of E", 4, "8,8,8,8,8,8", 6); 
       
INSERT INTO tuning_likes (user_id, uploader_id, tuning_id)
VALUES (1, 2, 3),
	   (1, 2, 5),
       (2, 1, 1),
       (2, 3, 8),
       (3, 1, 2),
       (3, 4, 9),
       (4, 2, 3),
       (4, 1, 1);
       
INSERT INTO scale_likes (user_id, uploader_id, scale_id)
VALUES (1, 4, 6),
	   (1, 2, 3),
	   (2, 3, 4),
       (2, 1, 1),
       (3, 1, 1),
       (3, 4, 5),
       (4, 1, 2),
       (4, 3, 4);
       
# for show user data
# returns username and total likes
SELECT users.user_name AS name, COUNT(uploader_id) AS likes 
FROM users
JOIN (SELECT uploader_id
	  FROM tuning_likes
      UNION ALL
      SELECT uploader_id
      FROM scale_likes) AS like_table
ON like_table.uploader_id=users.user_id
GROUP BY uploader_id;

# for show available tunings
# returns tuning name, string, tuning, uploader, num of likes
SELECT tunings.tuning_name, tunings.strings, tunings.tuning, users.user_name, COUNT(tuning_likes.like_id)
FROM tunings
LEFT JOIN users 
	ON tunings.user_id = users.user_id
LEFT JOIN tuning_likes
	ON tuning_likes.tuning_id = tunings.tuning_id
GROUP BY tunings.tuning_id;

# for show available scales
# returns scale name, steps, uploader, num of likes
SELECT scales.scale_name, scales.steps, users.user_name, COUNT(scale_likes.like_id)
FROM scales
LEFT JOIN users
	ON scales.user_id = users.user_id
LEFT JOIN scale_likes
	ON scale_likes.scale_id = scales.scale_id
GROUP BY scales.scale_id;

# returns tuning name and likes on a user id
SELECT tunings.tuning_name, COUNT(tuning_likes.like_id)
FROM tunings
LEFT JOIN tuning_likes
	ON tuning_likes.tuning_id = tunings.tuning_id
WHERE tunings.user_id=4
GROUP BY tunings.tuning_id;

# returns scale names and likes based on user id
SELECT scales.scale_name, COUNT(scale_likes.like_id)
FROM scales
LEFT JOIN scale_likes
	ON scale_likes.scale_id = scales.scale_id
WHERE scales.user_id=1
GROUP BY scales.scale_id;


SELECT * FROM users;
SELECT * FROM scales;
SELECT * FROM tunings;
SELECT * FROM tuning_likes;
SELECT * FROM scale_likes;

