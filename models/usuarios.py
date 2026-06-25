# id
# empresa_id
# filial_id
# nome
# email
# senha_hash
# perfil
# created_at

from db.base import Base

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column 


class User(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(primary_key=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey)
    filial_id: Mapped[int] = mapped_column(ForeignKey)
    nome: Mapped[str] = mapped_column(String(45))
    email: Mapped[str] = mapped_column(String(100))
    senha_hash: Mapped[str] = mapped_column(String(100))
    perfil: Mapped[str] = mapped_column(String(12))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())