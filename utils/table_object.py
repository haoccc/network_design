from sqlalchemy import Column, String, create_engine, Integer, Text, SmallInteger, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:

Base = declarative_base()


# 定义author_info对象:
class AuthorInfo(Base):
    # 表的名字:
    __tablename__ = 'author_info'

    # 表的结构:
    author_id = Column(String(12), primary_key=True)  # 用户id
    name = Column(String(20))  # 用户昵称
    unique_id = Column(String(30))  # 抖音号
    cover_path = Column(Text)  # 头像保存路径
    gender = Column(Integer)  # 性别
    birthday = Column(DateTime)  # 出生年月日
    signature = Column(Text)  # 简介
    total_favorited = Column(Integer)  # 获赞数
    follower_count = Column(Integer)  # 粉丝数
    following_count = Column(Integer)  # 关注数
    aweme_count = Column(Integer)  # 作品数


# 定义video_info对象:
class VideoInfo(Base):
    # 表的名字:
    __tablename__ = 'video_info'

    # 表的结构:
    aweme_id = Column(String(20), primary_key=True)  # 视频id
    save_path = Column(String)  # 保存路径
    data_size = Column(Integer)  # 视频大小
    create_time = Column(DateTime)  # 发布时间
    digg_count = Column(Integer)  # 点赞数
    comment_count = Column(Integer)  # 评论数
    download_count = Column(Integer)  # 下载数
    share_count = Column(Integer)  # 分享数
    author_id = Column(String(16))  # 作者id
    description = Column(Text)  # 视频简介
    city = Column(Integer)  # 城市编码
    duration = Column(Integer)  # 城市编码
