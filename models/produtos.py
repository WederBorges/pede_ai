from decimal import Decimal
from datetime import datetime

from db.base import Base
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

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
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    imagem_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)

    __table_args__ = (
        CheckConstraint("preco >= 0", name="ck_preco_uni_positivo"),
    )
