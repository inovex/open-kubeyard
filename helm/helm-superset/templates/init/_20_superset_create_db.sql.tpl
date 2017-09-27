CREATE DATABASE IF NOT EXISTS `superset` CHARACTER SET utf8;
CREATE USER 'superset'@'%' IDENTIFIED BY 'superset' ;
GRANT ALL ON `superset`.* TO 'superset'@'%';

FLUSH PRIVILEGES;
