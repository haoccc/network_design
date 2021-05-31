/*
Navicat MySQL Data Transfer

Source Server         : DB5.7
Source Server Version : 50726
Source Host           : localhost:3306
Source Database       : douyin

Target Server Type    : MYSQL
Target Server Version : 50726
File Encoding         : 65001

Date: 2021-05-25 21:07:50
*/

-- 创建“抖音”数据库
create database douyin；

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `author_info`
-- ----------------------------
DROP TABLE IF EXISTS `author_info`;
-- 用户信息
CREATE TABLE `author_info` (
  `author_id` char(12) COLLATE utf8_unicode_ci NOT NULL,	-- 用户id
  `name` char(30) COLLATE utf8_unicode_ci DEFAULT NULL,	-- 名字
  `unique_id` char(30) COLLATE utf8_unicode_ci DEFAULT NULL,	-- 抖音号
  `cover_path` text COLLATE utf8_unicode_ci,	-- 头像保存路径
  `gender` int(11) DEFAULT NULL,	-- 性别 1 男 2 女
  `birthday` date DEFAULT NULL,	-- 出生年月日
  `signature` text COLLATE utf8_unicode_ci,	-- 简介
  `total_favorited` bigint(20) DEFAULT NULL,	-- 获赞数
  `follower_count` int(11) DEFAULT NULL,	-- 粉丝数
  `followed_count` int(11) DEFAULT NULL,	-- 关注数
  `aweme_count` int(11) DEFAULT NULL,		-- 作品数
  `city` int(11) DEFAULT NULL,		-- 城市编码
  PRIMARY KEY (`author_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of author_info
-- ----------------------------


-- ----------------------------
-- Table structure for `video_info`
-- ----------------------------
DROP TABLE IF EXISTS `video_info`;
CREATE TABLE `video_info` (
  `aweme_id` char(20) COLLATE utf8_unicode_ci NOT NULL,	-- 视频id
  `save_path` text COLLATE utf8_unicode_ci,	-- 保存路径
  `data_size` int(11) DEFAULT NULL,	-- 视频大小
  `create_time` datetime DEFAULT NULL,		-- 发表时间
  `digg_count` int(11) DEFAULT NULL,	-- 点赞数
  `comment_count` int(11) DEFAULT NULL,	-- 评论数
  `download_count` int(11) DEFAULT NULL,	-- 下载数
  `share_count` int(11) DEFAULT NULL,		-- 分享数
  `author_id` char(12) COLLATE utf8_unicode_ci DEFAULT NULL,	-- 作者id
  `description` text COLLATE utf8_unicode_ci,	-- 视频描述
  PRIMARY KEY (`aweme_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of video_info
-- ----------------------------