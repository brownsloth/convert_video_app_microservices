# DATABASE USER, not the end user
# CREATE USER username@<host from which user will connect> IDENTIFIED BY password
CREATE USER "auth_user"@"localhost" IDENTIFIED BY "Aauth123";

CREATE DATABASE auth;

# grant all privileges on all tables in auth database
grant all privileges ON auth.* TO "auth_user"@"localhost";

# from here on, refer auth as db
USE auth;

CREATE TABLE user (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	password VARCHAR(255) NOT NULL
);

# This user will have access to our "api Gateway"
INSERT INTO USER(email, password) VALUES ("starun@gmail.com", "Admin123");
