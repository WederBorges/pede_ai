from db.base import Base

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import TIMESTAMP
from sqlalchemy import Boolean
from sqlalchemy import func
from sqlalchemy import CheckConstraint
from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column 

## produtos
# id
# empresa_id
# nome
# descricao
# preco
# imagem_url
# ativo
# created_at

class Produtos(Base):

    __tablename__ = "produtos"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    preco: Mapped[float] = mapped_column(Float, nullable=False)
    imagem_url: Mapped[str] = mapped_column(String(255), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
