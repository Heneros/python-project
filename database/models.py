
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy import String, Integer, BigInteger

class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)
    settings: Mapped[dict] = mapped_column(JSONB, default={})
    roles: Mapped[list[str]] = mapped_column(ARRAY(String), default=[])

    

