#!/usr/bin/env sh

sh /wasabi/create_keyspace.sh
sh /wasabi/schema_migration.sh
mysql -h${MYSQL_HOST} -P3306 -uroot -p${MYSQL_ROOT_PASSWORD} -e "create database if not exists wasabi;
    grant all privileges on wasabi.* to 'readwrite'@'localhost' identified by 'readwrite';
    grant all on *.* to 'readwrite'@'%' identified by 'readwrite';
    flush privileges;"