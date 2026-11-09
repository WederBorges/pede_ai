from models.usuarios import User

u = User(nome='x', email='x@x.com', perfil='a', senha_hash='antiga', empresa_id=1)
setattr(u, 'senha', 'nova123')

print(u.senha)
print(u.senha_hash)