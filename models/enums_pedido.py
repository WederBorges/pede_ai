from enum import Enum


class Status_Pedidos(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    EM_SEPARACAO = "EM_SEPARACAO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

TRANSICOES_VALIDAS = { #MAQUINA DE ESTADOS

        Status_Pedidos.PENDENTE: [Status_Pedidos.APROVADO, Status_Pedidos.CANCELADO],
        Status_Pedidos.APROVADO: [Status_Pedidos.EM_SEPARACAO, Status_Pedidos.CANCELADO],
        Status_Pedidos.EM_SEPARACAO: [Status_Pedidos.ENVIADO, Status_Pedidos.CANCELADO],
        Status_Pedidos.ENVIADO: [Status_Pedidos.ENTREGUE],
        Status_Pedidos.ENTREGUE: [],
        Status_Pedidos.CANCELADO: []
    }



PREVISOES_ENTREGAS_VALIDAS = ["APROVADO", "EM_SEPARACAO", "ENVIADO",]