from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    CheckConstraint,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

# empresas
# id
# nome
# centro_de_custo
# created_at


class Empresas(Base):
    __tablename__ = 'empresas'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    centro_de_custo: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        CheckConstraint(
            'centro_de_custo >= 0 and centro_de_custo <= 999',
            name='ck_centro_de_custo_3dig',
        ),
    )


# filiais
# id
# empresa_id
# nome
# cidade
# estado
# created_at


class Filiais(Base):
    __tablename__ = 'filiais'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    empresa_id: Mapped[int] = mapped_column(ForeignKey('empresas.id'), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cidade: Mapped[str] = mapped_column(String(50), nullable=False)
    estado: Mapped[str] = mapped_column(String(50), nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )
