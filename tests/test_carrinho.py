from http import HTTPStatus

import pytest
from sqlalchemy import select

from models.usuarios import User
from models.carrinho import Carrinho, CarrinhoItens
from schemas.schema_carrinho import s_Create_carrinho_out, s_Produtos_response_carrinho, s_Produto_Output_carrinho


@pytest.mark.asyncio
async def test_create_carrinho(client, async_session, usuario_teste, filial_teste):

    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id
    }

    response = client.post('/carrinho', json=dados)

    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    stmt = select(Carrinho).where(Carrinho.usuario_id == usuario_teste.id)
    carrinho_bd = await async_session.scalar(stmt)

    model_carrinho = s_Create_carrinho_out.model_validate(carrinho_bd).model_dump(mode='json')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == model_carrinho


@pytest.mark.asyncio
async def test_filial_inexistente(client, async_session, usuario_teste, filial_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': 9999,
        'usuario_id': usuario_teste.id
    }

    response = client.post('/carrinho', json=dados)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Filial inexistente'}


@pytest.mark.asyncio
async def test_usuario_inexistente(client, async_session, usuario_teste, filial_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 

    dados = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id + 1
    }

    response = client.post('/carrinho', json=dados)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário inexistente'}


@pytest.mark.asyncio
async def test_adicionar_produto_carrinho(client, async_session, usuario_teste, filial_teste, produto_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 
    await async_session.refresh(produto_teste)

    dados_carrinho = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id
    }
    
    response_carrinho = client.post('/carrinho', json=dados_carrinho)
    
    carrinho_id = response_carrinho.json()['id']

    await async_session.refresh(produto_teste)

    dados_produto = {
        'produto_id': produto_teste.id,
        'quantidade': 2
    }
  
    response_produto = client.post(f'/carrinho/{carrinho_id}/produtos', json=dados_produto)

    stmt = select(CarrinhoItens).where(CarrinhoItens.carrinho_id == carrinho_id)
    carrinho_item_bd = await async_session.scalar(stmt)
    
    assert carrinho_item_bd.carrinho_id == carrinho_id
    assert carrinho_item_bd.produto_id == dados_produto['produto_id']
    assert carrinho_item_bd.quantidade == dados_produto['quantidade']
    assert response_produto.status_code == HTTPStatus.OK

@pytest.mark.asyncio
async def test_add_produto_duas_vezes(client, async_session, usuario_teste, filial_teste, produto_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 
    await async_session.refresh(produto_teste)

    dados_carrinho = {
        'filial_id': filial_teste.id,
        'usuario_id': usuario_teste.id
    }
    
    response_carrinho = client.post('/carrinho', json=dados_carrinho)
    
    carrinho_id = response_carrinho.json()['id']

    await async_session.refresh(produto_teste)

    dados_produto = {
        'produto_id': produto_teste.id,
        'quantidade': 2
    }
  
    response_produto_1 = client.post(f'/carrinho/{carrinho_id}/produtos', json=dados_produto)
    response_produto_2 = client.post(f'/carrinho/{carrinho_id}/produtos', json=dados_produto)

    stmt = select(CarrinhoItens).where(CarrinhoItens.carrinho_id == carrinho_id)

    carrinho_item_bd = await async_session.scalars(stmt)
    carrinho_item_bd = carrinho_item_bd.all()
   
    assert carrinho_item_bd[0].carrinho_id == carrinho_id
    assert carrinho_item_bd[0].produto_id == dados_produto['produto_id']
    assert carrinho_item_bd[0].quantidade == dados_produto['quantidade'] * 2
    assert len(carrinho_item_bd) == 1
    assert response_produto_1.status_code == HTTPStatus.OK 
    assert response_produto_2.status_code == HTTPStatus.OK

@pytest.mark.asyncio
async def test_adicionar_produto_com_carrinhoID_inexistente(client, async_session, usuario_teste, filial_teste, produto_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 
    await async_session.refresh(produto_teste)

    carrinho_id_inexistente = 9999

    dados_produto = {
        'produto_id': produto_teste.id,
        'quantidade': 2
    }
  
    response_produto = client.post(f'/carrinho/{carrinho_id_inexistente}/produtos', json=dados_produto)

    assert response_produto.status_code == HTTPStatus.NOT_FOUND
    assert response_produto.json() == {'detail': 'Carrinho inexistente'}


@pytest.mark.asyncio
async def test_adicionar_produto_com_produtoID_inexistente(client, async_session, filial_teste ,usuario_teste, produto_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 
    await async_session.refresh(produto_teste)

    carrinho_id = client.post('/carrinho', json={'filial_id': filial_teste.id, 'usuario_id': usuario_teste.id}).json()['id']

    dados_produto = {
        'produto_id': 9999,
        'quantidade': 2
    }
  
    response_produto = client.post(f'/carrinho/{carrinho_id}/produtos', json=dados_produto)

    assert response_produto.status_code == HTTPStatus.NOT_FOUND
    assert response_produto.json() == {'detail': 'Produto inexistente'}


@pytest.mark.asyncio
async def test_adicionar_produto_quantidade_zero(client, async_session, usuario_teste, filial_teste, produto_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 
    await async_session.refresh(produto_teste)

    carrinho_id = client.post('/carrinho', json={'filial_id': filial_teste.id, 'usuario_id': usuario_teste.id}).json()['id']

    await async_session.refresh(produto_teste)

    dados_produto = {
        'produto_id': produto_teste.id,
        'quantidade': 0
    }
  
    response_produto = client.post(f'/carrinho/{carrinho_id}/produtos', json=dados_produto)

    assert response_produto.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_remover_produto_carrinho(client, async_session, usuario_teste, filial_teste, produto_teste):
    
    await async_session.refresh(usuario_teste)
    await async_session.refresh(filial_teste) 
    await async_session.refresh(produto_teste)

    carrinho_id = client.post('/carrinho', json={'filial_id': filial_teste.id, 'usuario_id': usuario_teste.id}).json()['id']

    await async_session.refresh(produto_teste)

    dados_produto = {
        'produto_id': produto_teste.id,
        'quantidade': 2
    }
  
    response_produto_adicionado = client.post(f'/carrinho/{carrinho_id}/produtos', json=dados_produto)

    await async_session.refresh(produto_teste)
    response_produto_removido = client.delete(f'/carrinho/{carrinho_id}/produtos/{produto_teste.id}', params={'quantidade': 2})

    stmt = select(CarrinhoItens).where(CarrinhoItens.carrinho_id == carrinho_id)
    carrinho_item_bd = await async_session.scalar(stmt)

    print(response_produto_removido.json())
    # assert response_produto_removido.status_code == HTTPStatus.OK