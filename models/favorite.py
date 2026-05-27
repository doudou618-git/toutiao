from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from models import Base
from models.news import News
from models.users import User


class Favorite(Base):
    """
    收藏表ORM模型
    """
    __tablename__ = 'favorite'

    __table_args__ = (
        UniqueConstraint('user_id', 'news_id', name='user_news_unique'),
        Index('fk_favorite_user_idx', 'user_id'),
        Index('fk_favorite_news_idx', 'news_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey(News.id), nullable=False, comment="新闻ID")

    def __repr__(self):
        return f"<Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
