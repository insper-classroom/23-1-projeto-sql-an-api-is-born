from typing import Annotated
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

#cria alguns dados fictícios
filmes = [
    {
        "id": 1,
        "nome": "O Poderoso Chefão",
        "diretor": "Francis Ford Coppola",
        "ano_lancamento": 1972,
        "genero": "Drama"
    },
    {
        "id": 2,
        "nome": "O Poderoso Chefão II",
        "diretor": "Francis Ford Coppola",
        "ano_lancamento": 1974,
        "genero": "Drama"
    },
    {
        "id": 3,
        "nome": "O Poderoso Chefão III",
        "diretor": "Francis Ford Coppola",
        "ano_lancamento": 1990,
        "genero": "Drama"
    }
]
#cria alguns dados fictícios de classificações
classificacoes = [
    {
        "id": 1,
        "classificacao": 8.5,
        "comentario": "Excelente filme",
        "filme_id": 1
    },
    {
        "id": 2,
        "classificacao": 9.0,
        "comentario": "Ótimo filme",
        "filme_id": 2
    },
    {
        "id": 3,
        "classificacao": 7.5,
        "comentario": "Bom filme",
        "filme_id": 3
    },
    {
        "id": 4,
        "classificacao": 8.0,
        "comentario": "Bom filme",
        "filme_id": 1
    }
]

class Filme(BaseModel):
    nome: str = Field(
        description="O nome do filme", max_length=100
    )
    diretor: str | None = Field(
        default=None, description="O nome do diretor do filme", max_length=100
    )
    ano_lancamento : int = Field(
        description="Ano de lançamento"
    )
    genero: str = Field(
        description="O gênero do filme", max_length=60
    )

#cria uma classe de classificações de filmes de 0.0 a 10.0, um campo de texto livre e o id do filme
class Classificacao(BaseModel):
    classificacao: Annotated[float, Field(gt=0, lt=10)]
    comentario: str | None = Field(
        default=None, description="Comentário sobre o filme", max_length=300
    )
    filme_id: int = Field(
        description="O id do filme"
    )
   
class User(BaseModel):
    username: str
    full_name: str | None = None

@app.post("/filmes/{filme_id}")
async def create_filme(filme_id: int, filme: Filme, user: User):
    results = {"filme_id": filme_id, "filme": filme, "user": user}
    return results

@app.get("/filmes/{filme_id}")
async def read_filme(filme_id: int):
    #retorna o filme com o id especificado com todos os dados 
    return filmes[filme_id-1]

# o usuario pode alterar os dados de um filme
@app.put("/filmes/{filme_id}")
async def update_filme(filme_id: int, filme: Filme, user: User):
    results = {"filme_id": filme_id, "filme": filme, "user": user}
    return results

# usuário pode gerenciar cadastro de avaliações de filmes
@app.post("/filmes/{filme_id}/classificacao")
async def create_classificacao(filme_id: int, classificacao: Classificacao):
    results = {"filme_id": filme_id, "classificacao": classificacao}
    return results

# o usuario pode listar as avaliações de filmes
@app.get("/filmes/{filme_id}/classificacao")
async def read_classificacao(filme_id: int):
    #retorna todas as classificações do filme com o id especificado (pode ter mais de uma)
    return [classificacao for classificacao in classificacoes if classificacao["filme_id"] == filme_id]