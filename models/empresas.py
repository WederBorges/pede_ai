from db.base import Base

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import Boolean
from sqlalchemy import func
from sqlalchemy import CheckConstraint
from datetime import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column 

## empresas
# id
# nome
# centro_de_custo
# created_at

class Empresas(Base):
    
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    nome: Mapped[int] = mapped_column(String(100), nullable=False)
    centro_de_custo = Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        
        CheckConstraint("centro_de_custo => 0 and codigo <= 999", name="ck_centro_de_custo_3dig")
    )


## filiais
# id
# empresa_id
# nome
# cidade
# estado
# created_at

class Filiais(Base):

    __tablename__ = "filiais"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresa.id"), nullable=False)
    nome = Mapped[int] = mapped_column(String(100), nullable=False)
    cidade: Mapped[datetime] = mapped_column(String(50), nullable=False)
    estado: Mapped[datetime] = mapped_column(String(50), nullable=False) 
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False)
    

