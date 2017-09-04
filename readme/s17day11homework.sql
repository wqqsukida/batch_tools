/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50716
Source Host           : localhost:3306
Source Database       : s17day11homework

Target Server Type    : MYSQL
Target Server Version : 50716
File Encoding         : 65001

Date: 2017-07-13 15:11:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for g2h
-- ----------------------------
DROP TABLE IF EXISTS `g2h`;
CREATE TABLE `g2h` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_d11_4` (`group_id`),
  KEY `fk_d11_5` (`host_id`),
  CONSTRAINT `fk_d11_4` FOREIGN KEY (`group_id`) REFERENCES `group_info` (`gid`),
  CONSTRAINT `fk_d11_5` FOREIGN KEY (`host_id`) REFERENCES `host_info` (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of g2h
-- ----------------------------
INSERT INTO `g2h` VALUES ('1', '1', '1');
INSERT INTO `g2h` VALUES ('2', '1', '2');
INSERT INTO `g2h` VALUES ('3', '1', '3');
INSERT INTO `g2h` VALUES ('4', '1', '4');
INSERT INTO `g2h` VALUES ('5', '1', '5');
INSERT INTO `g2h` VALUES ('6', '2', '1');
INSERT INTO `g2h` VALUES ('7', '2', '2');
INSERT INTO `g2h` VALUES ('8', '2', '3');
INSERT INTO `g2h` VALUES ('9', '2', '6');
INSERT INTO `g2h` VALUES ('10', '2', '7');
INSERT INTO `g2h` VALUES ('11', '3', '1');
INSERT INTO `g2h` VALUES ('12', '3', '2');
INSERT INTO `g2h` VALUES ('13', '3', '3');
INSERT INTO `g2h` VALUES ('14', '3', '4');
INSERT INTO `g2h` VALUES ('15', '3', '5');
INSERT INTO `g2h` VALUES ('16', '3', '6');
INSERT INTO `g2h` VALUES ('17', '3', '7');

-- ----------------------------
-- Table structure for group_info
-- ----------------------------
DROP TABLE IF EXISTS `group_info`;
CREATE TABLE `group_info` (
  `gid` int(11) NOT NULL AUTO_INCREMENT,
  `gname` char(32) NOT NULL,
  PRIMARY KEY (`gid`,`gname`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of group_info
-- ----------------------------
INSERT INTO `group_info` VALUES ('1', 'IT');
INSERT INTO `group_info` VALUES ('2', 'DEV');
INSERT INTO `group_info` VALUES ('3', 'ADMIN');
INSERT INTO `group_info` VALUES ('4', 'SUPER');

-- ----------------------------
-- Table structure for host_info
-- ----------------------------
DROP TABLE IF EXISTS `host_info`;
CREATE TABLE `host_info` (
  `hid` int(11) NOT NULL AUTO_INCREMENT,
  `host` char(32) DEFAULT NULL,
  `ip` char(32) DEFAULT NULL,
  `user` char(32) DEFAULT NULL,
  `pwd` char(64) DEFAULT NULL,
  PRIMARY KEY (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of host_info
-- ----------------------------
INSERT INTO `host_info` VALUES ('1', 'host1', '192.168.35.128', 'root', '123456');
INSERT INTO `host_info` VALUES ('2', 'host2', '192.168.35.129', 'root', '123456');
INSERT INTO `host_info` VALUES ('3', 'host3', '192.168.35.130', 'root', '123456');
INSERT INTO `host_info` VALUES ('4', 'host4', '192.168.35.131', 'root', '123456');
INSERT INTO `host_info` VALUES ('5', 'host5', '192.168.35.132', 'root', '123456');
INSERT INTO `host_info` VALUES ('6', 'host6', '192.168.35.133', 'root', '123456');
INSERT INTO `host_info` VALUES ('7', 'host7', '192.168.35.134', 'root', '123456');

-- ----------------------------
-- Table structure for u2h
-- ----------------------------
DROP TABLE IF EXISTS `u2h`;
CREATE TABLE `u2h` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `host_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_d11_2` (`user_id`),
  KEY `fk_d11_3` (`host_id`),
  CONSTRAINT `fk_d11_2` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`uid`),
  CONSTRAINT `fk_d11_3` FOREIGN KEY (`host_id`) REFERENCES `host_info` (`hid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of u2h
-- ----------------------------
INSERT INTO `u2h` VALUES ('1', '1', '1');
INSERT INTO `u2h` VALUES ('2', '1', '2');
INSERT INTO `u2h` VALUES ('3', '1', '3');
INSERT INTO `u2h` VALUES ('4', '1', '4');
INSERT INTO `u2h` VALUES ('5', '1', '5');
INSERT INTO `u2h` VALUES ('6', '2', '1');
INSERT INTO `u2h` VALUES ('7', '2', '2');
INSERT INTO `u2h` VALUES ('8', '2', '3');
INSERT INTO `u2h` VALUES ('9', '1', '6');
INSERT INTO `u2h` VALUES ('10', '2', '7');

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `uname` char(32) NOT NULL DEFAULT '',
  `pwd` char(64) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`uid`),
  UNIQUE KEY `uname_index` (`uname`) USING BTREE,
  KEY `fk_d11_1` (`group_id`),
  CONSTRAINT `fk_d11_1` FOREIGN KEY (`group_id`) REFERENCES `group_info` (`gid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of user_info
-- ----------------------------
INSERT INTO `user_info` VALUES ('1', 'user1', '123', '1');
INSERT INTO `user_info` VALUES ('2', 'user2', '456', '2');
INSERT INTO `user_info` VALUES ('3', 'admin', '123456', '3');
