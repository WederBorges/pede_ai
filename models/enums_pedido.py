from enum import Enum


class Status_Pedidos(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    EM_SEPARACAO = "EM_SEPARACAO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"