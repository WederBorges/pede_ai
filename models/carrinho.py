from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    TIMESTAMP,
    CheckConstraint,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Carrinho(Base):
    __tablename__ = 'carrinho'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), nullable=False)
    filial_id: Mapped[int] = mapped_column(ForeignKey('filiais.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)


class CarrinhoItens(Base):
    __tablename__ = 'carrinho_itens'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    carrinho_id: Mapped[int] = mapped_column(ForeignKey('carrinho.id'), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey('produtos.id'), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('quantidade > 0', name='ck_quantidade_positiva'),
        CheckConstraint('preco > 0', name='ck_preco_positivo'),
        UniqueConstraint('carrinho_id', 'produto_id', name='uq_carrinho_produto'),
    )
