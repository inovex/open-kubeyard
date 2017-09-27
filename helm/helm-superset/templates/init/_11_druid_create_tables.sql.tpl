-- MySQL dump 10.16  Distrib 10.1.21-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: localhost
-- ------------------------------------------------------
-- Server version	10.1.21-MariaDB-1~jessie

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `druid`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `druid` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `druid`;

--
-- Table structure for table `druid_audit`
--

DROP TABLE IF EXISTS `druid_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_audit` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `audit_key` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `comment` varchar(2048) NOT NULL,
  `created_date` varchar(255) NOT NULL,
  `payload` longblob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_druid_audit_key_time` (`audit_key`,`created_date`),
  KEY `idx_druid_audit_type_time` (`type`,`created_date`),
  KEY `idx_druid_audit_audit_time` (`created_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_config`
--

DROP TABLE IF EXISTS `druid_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_config` (
  `name` varchar(255) NOT NULL,
  `payload` longblob NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_dataSource`
--

DROP TABLE IF EXISTS `druid_dataSource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_dataSource` (
  `dataSource` varchar(255) NOT NULL,
  `created_date` varchar(255) NOT NULL,
  `commit_metadata_payload` longblob NOT NULL,
  `commit_metadata_sha1` varchar(255) NOT NULL,
  PRIMARY KEY (`dataSource`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_pendingSegments`
--

DROP TABLE IF EXISTS `druid_pendingSegments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_pendingSegments` (
  `id` varchar(255) NOT NULL,
  `dataSource` varchar(255) NOT NULL,
  `created_date` varchar(255) NOT NULL,
  `start` varchar(255) NOT NULL,
  `end` varchar(255) NOT NULL,
  `sequence_name` varchar(255) NOT NULL,
  `sequence_prev_id` varchar(255) NOT NULL,
  `sequence_name_prev_id_sha1` varchar(255) NOT NULL,
  `payload` longblob NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sequence_name_prev_id_sha1` (`sequence_name_prev_id_sha1`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_rules`
--

DROP TABLE IF EXISTS `druid_rules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_rules` (
  `id` varchar(255) NOT NULL,
  `dataSource` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  `payload` longblob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_druid_rules_datasource` (`dataSource`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_segments`
--

DROP TABLE IF EXISTS `druid_segments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_segments` (
  `id` varchar(255) NOT NULL,
  `dataSource` varchar(255) NOT NULL,
  `created_date` varchar(255) NOT NULL,
  `start` varchar(255) NOT NULL,
  `end` varchar(255) NOT NULL,
  `partitioned` tinyint(1) NOT NULL,
  `version` varchar(255) NOT NULL,
  `used` tinyint(1) NOT NULL,
  `payload` longblob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_druid_segments_datasource` (`dataSource`),
  KEY `idx_druid_segments_used` (`used`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_supervisors`
--

DROP TABLE IF EXISTS `druid_supervisors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_supervisors` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `spec_id` varchar(255) NOT NULL,
  `created_date` varchar(255) NOT NULL,
  `payload` longblob NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_druid_supervisors_spec_id` (`spec_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_tasklocks`
--

DROP TABLE IF EXISTS `druid_tasklocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_tasklocks` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) DEFAULT NULL,
  `lock_payload` longblob,
  PRIMARY KEY (`id`),
  KEY `idx_druid_tasklocks_task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_tasklogs`
--

DROP TABLE IF EXISTS `druid_tasklogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_tasklogs` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(255) DEFAULT NULL,
  `log_payload` longblob,
  PRIMARY KEY (`id`),
  KEY `idx_druid_tasklogs_task_id` (`task_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `druid_tasks`
--

DROP TABLE IF EXISTS `druid_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `druid_tasks` (
  `id` varchar(255) NOT NULL,
  `created_date` varchar(255) NOT NULL,
  `datasource` varchar(255) NOT NULL,
  `payload` longblob NOT NULL,
  `status_payload` longblob NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_druid_tasks_active_created_date` (`active`,`created_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-02-15 15:00:12
