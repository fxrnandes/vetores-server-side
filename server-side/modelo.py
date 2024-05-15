from sqlalchemy import create_engine

# Substituir por credenciais reais do banco de dados
URL_BANCO_DE_DADOS = "mysql+mysqlconnector://usuario:senha@host:porta/nome_do_banco"

engine = create_engine(URL_BANCO_DE_DADOS)

Base = declarativebase()

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class VetorOrdenado(Base):
    __tablename__ = 'VetorOrdenado'  # Nome da tabela

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    numeros = Column(String)

class VetorAleatorio(Base):
    __tablename__ = 'VetorAleatorio'  # Nome da tabela

    id = Column(Integer, primary_key=True)
    descricao = Column(String)
    numeros = Column(String)


Base.metadata.create_all(engine)

# Criando um novo objeto VetorOrdenado
vetor_ordenado = VetorOrdenado(descricao="Meu vetor ordenado", numeros="1,2,3,4,5")

# Adicionando o objeto à sessão e confirmando as alterações
sessao = Session(bind=engine)
sessao.add(vetor_ordenado)
sessao.commit()

# Buscando todos os objetos VetorOrdenado do banco de dados
vetores_ordenados = sessao.query(VetorOrdenado).all()
for vetor in vetores_ordenados:
    print(f"Vetor Ordenado: {vetor.descricao}")

# Excluindo um objeto VetorOrdenado
vetor_a_apagar = sessao.query(VetorOrdenado).filter(VetorOrdenado.id == 10).first()
sessao.delete(vetor_a_apagar)
sessao.commit()
