CREATE DATABASE bilibili_spider;

USE bilibilil_spider;

CREATE TABLE rank ( crwal_time DATE, video_name VARCHAR ( 100 ), video_link VARCHAR ( 1000 ), video_play_num INTEGER, video_danmu_num INTEGER, video_id VARCHAR ( 20 ), author_name VARCHAR ( 100 ), author_link VARCHAR ( 100 ), author_id VARCHAR ( 100 )) default charset=utf8;

-- update mysql.user set authentication_string=PASSWORD('spider123...'), plugin='mysql_native_password' where user='root';