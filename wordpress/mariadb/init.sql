CREATE DATABASE IF NOT EXISTS `wordpress`;

CREATE USER IF NOT EXISTS `wordpress`@'%' IDENTIFIED BY 'wordpresspass';

GRANT ALL PRIVILEGES ON wordpress.* TO 'wordpress'@'%';
