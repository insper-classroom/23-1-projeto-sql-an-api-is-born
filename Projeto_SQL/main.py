from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from json import *

app = FastAPI()

#cria alguns dados fictícios
filmes = load(open('filmes.json', 'r'))

#cria alguns dados fictícios de avaliacoes
avaliacoes = load(open('avaliacoes.json', 'r'))

# quantidade_id = dump(len(filmes), open('id.json', "w"))
quantidade_id = load(open('id.json', "r"))

class Filme(BaseModel):
    nome: str = Field(
        description="O nome do filme", max_length=100
    )
    diretor: str = Field(
        default=None, description="O nome do diretor do filme", max_length=100
    )
    ano_lancamento : int = Field(
        description="Ano de lançamento"
    )
    genero: str = Field(
        description="O gênero do filme", max_length=60
    )

#cria uma classe de avaliacoes de filmes de 0.0 a 10.0, um campo de texto livre e o id do filme
class Avaliacao(BaseModel):
    avaliacao: Annotated[float, Field(gt=0, lt=10)]
    comentario: str = Field(
        default=None, description="Comentário sobre o filme", max_length=300
    )
    filme_id: int = Field(
        description="O id do filme"
    )

    
@app.post("/filmes/{filme_id}")
async def create_filme(filme: Filme):
    filmes = load(open('filmes.json', "r"))    
    filme = filme.dict()
    for film in filmes:
        if film.get('nome') == filme['nome'] and film.get('ano_lancamento') == filme['ano_lancamento']:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O filme já existe!")
    new_filme = {}
    quantidade_id = load(open('id.json', "r"))
    new_filme['id'] = quantidade_id + 1
    new_filme.update(filme)
    filmes.append(new_filme)
    dump(quantidade_id + 1, open('id.json', "w"))
    dump(filmes, open('filmes.json', "w", encoding='utf8'),ensure_ascii = False, indent = 2)
    filmes = load(open('filmes.json', 'r'))
    return filmes

@app.get("/filmes")
async def all_filmes():
    #retorna todos os filmes
    filmes = load(open('filmes.json', "r"))
    return filmes

@app.get("/filmes/{filme_id}")
async def read_filme(filme_id: int):
    #retorna o filme com o id especificado com todos os dados 
    filmes = load(open('filmes.json', "r"))
    for filme in filmes:
        if filme.get('id') == filme_id:
            return filme
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi achado o filme.")

@app.delete("/filmes/{filme_id}")
async def delete_filme(filme_id: int):
    #deleta um filme com o id especificado  
    filmes = load(open('filmes.json', "r"))
    avaliacoes = load(open('avaliacoes.json', 'r')) 
    for filme in filmes:
        if filme.get('id') == filme_id:
            filmes.remove(filme)
            dump(filmes, open('filmes.json', "w", encoding='utf8'), indent = 2)
            for avaliacao in avaliacoes:
                if avaliacao.get('id') == filme_id:
                    avaliacoes.remove(avaliacao)
            return {"STATUS": "OK", "Filmes": filmes, "Avaliações": avaliacoes}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi achado o item para ser deletado.")

# o usuario pode alterar os dados de um filme
@app.put("/filmes/{filme_id}")
async def update_filme(filme_id: int, filme: Filme):
    filmes = load(open('filmes.json', "r"))
    for film in filmes:
        if film.get('id') == filme_id:
            filme = filme.dict()
            film['nome'] = filme['nome']
            film['diretor'] = filme['diretor']
            film['ano_lancamento'] = filme['ano_lancamento']
            film['genero'] = filme['genero']
            dump(filmes, open('filmes.json', "w", encoding='utf8'), indent = 2)
            filmes_alterados = load(open('filmes.json', "r"))
            return filmes_alterados
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi achado o item para ser alterado.")

# usuário pode gerenciar cadastro de avaliações de filmes
@app.post("/filmes/{filme_id}/avaliacao")
async def create_avaliacao(filme_id: int, avaliacao: Avaliacao):
    results = {"filme_id": filme_id, "avaliacao": avaliacao}
    return results

# o usuario pode listar as avaliações de filmes
@app.get("/filmes/{filme_id}/avaliacao")
async def read_avaliacao(filme_id: int):
    #retorna todas as avaliacoes do filme com o id especificado (pode ter mais de uma)
    return [avaliacao for avaliacao in avaliacoes if avaliacao["filme_id"] == filme_id]