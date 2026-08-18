from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, String, func
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Categoria(Base):
    __tablename__ = 'categorias'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
