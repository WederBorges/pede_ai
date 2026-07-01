from decimal import Decimal
from datetime import datetime

from db.base import Base
from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

# ## pedidos
# id
# empresa_id
# filial_id
# usuario_id
# status
# valor_total
# previsao_entrega
# created_at

class Pedidos(Base):

    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)
    filial_id: Mapped[int] = mapped_column(ForeignKey("filiais.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    previsao_entrega: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)

    __table_args__ = (
        CheckConstraint("valor_total >= 0", name="ck_valor_positivo_total_pedidos"),
    )

# ## pedido_itens
# id
# pedido_id
# produto_id
# nome_produto
# preco_unitario
# quantidade
# subtotal

class PedidoItens(Base):

    __tablename__ = "pedido_itens"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    produto_id: Mapped[int] = mapped_column(ForeignKey("produtos.id"), nullable=False)
    nome_produto: Mapped[str] = mapped_column(String(100), nullable=False)
    preco_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("quantidade > 0", name="ck_pedido_itens_quantidade_positiva"),
        CheckConstraint("preco_unitario > 0", name="ck_pedido_itens_preco_positivo"),
    )

# ## pedido_status_historico
# id
# pedido_id
# status
# observacao
# created_at
# alterado_por

class PedidoStatusHistorico(Base):

    __tablename__ = "pedido_status_historico"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    observacao: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    alterado_por: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
