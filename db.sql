CREATE TABLE user (
    id        INT AUTO_INCREMENT,
    name      VARCHAR(64)  NOT NULL,
    password  VARCHAR(128) NOT NULL,
    session   VARCHAR(32),
    join_time TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id)
);

CREATE TABLE restaurant (
    id       INT AUTO_INCREMENT,
    name     VARCHAR(128) NOT NULL,
    `desc`   TEXT NOT NULL,
    zip      VARCHAR(64) NOT NULL,
    tel      INT NOT NULL,
    website  VARCHAR(256),
    img      VARCHAR(2048) NOT NULL,
    location VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE review (
    id          INT AUTO_INCREMENT,
    user        INT NOT NULL,
    restaurant  INT NOT NULL,
    rating      FLOAT NOT NULL,
    comment     VARCHAR(1024) NOT NULL,
    post_time   TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (id),
    FOREIGN KEY (user) REFERENCES user(id),
    FOREIGN KEY (restaurant) REFERENCES restaurant(id)
);