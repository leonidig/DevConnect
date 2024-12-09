from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from  .. import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key = True)
    title: Mapped[str]
    content: Mapped[str]
    author: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default = datetime.now())
    