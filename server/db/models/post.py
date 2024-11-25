from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from  .. import Base


class Post(Base):
    __tablename__ = "posts"

    user_id: Mapped[int]
    content: Mapped[str]
    timestamp: Mapped[datetime] = mapped_column(default = datetime.now())
    