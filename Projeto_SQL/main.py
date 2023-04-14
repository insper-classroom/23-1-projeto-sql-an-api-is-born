from typing import Annotated
from fastapi import Body, FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from json import *

# Inicialização e criação da API
app = FastAPI(title="An API is born",
              description="API criada para guardar filmes e suas avaliações.")

# Primeira abertura  dos json que servem como 'banco de dados'
filmes = load(open('filmes.json', 'r'))
avaliacoes = load(open('avaliacoes.json', 'r'))

# Criação do json que serve para guardar o valor do id e servir como um id auto incremento
quantidade_id = load(open('id.json', "r"))

class Filme(BaseModel):
    """ Criação do modelo Filme que irá guardar os dados obtidos dos usuários."""

    nome: str = Field(
        description = "O nome do filme", max_length = 100
    )
    diretor: str = Field(
        default = None, description = "O nome do diretor do filme", max_length = 100
    )
    ano_lancamento : int = Field(
        description = "Ano de lançamento"
    )
    genero: str = Field(
        description = "O gênero do filme", max_length = 60
    )

class Avaliacao(BaseModel):
    """ Cria uma classe de avaliacoes de filmes de 0.0 a 10.0, um campo de texto livre e o id do filme. """

    avaliacao: Annotated[float, Field(gt=0, lt=10)]
    comentario: str = Field(
        default = None, description = "Comentário sobre o filme", max_length = 300
    )
    filme_id: int = Field(
        description = "O id do filme interligado ao modelo Filme criado anteriormente."
    )

class Avaliacao_Update(BaseModel):
    """ Utilizado para poder fazer o update da avaliação sem alterar os id's dos filmes. """

    avaliacao: Annotated[float, Field(gt=0, lt=10)]
    comentario: str = Field(
        default = None, description = "Comentário sobre o filme", max_length = 300
    )
    
@app.post("/filme")
async def create_filme(filme: Filme):
    """ Criação de novos filmes para adicionar ao banco de dados, não sendo possível a criação de dois filmes com 
mesmo nome e ano de lançamento, cria o id automaticamente, devido ao 'id.json' que guarda o último id criado. A 
função também deve adicionar o filme criado no fim do 'filmes.json'."""
    
    filmes = load(open('filmes.json', "r"))    
    quantidade_id = load(open('id.json', "r"))

    filme = filme.dict()
    for film in filmes:
        if film.get('nome') == filme['nome'] and film.get('ano_lancamento') == filme['ano_lancamento']:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "O filme já existe!")
    
    new_filme = {}
    new_filme['id'] = quantidade_id + 1
    new_filme.update(filme)
    filmes.append(new_filme)

    dump(quantidade_id + 1, open('id.json', "w"))
    dump(filmes, open('filmes.json', "w", encoding = 'utf8'), ensure_ascii = False, indent = 2)
    
    return "O filme foi adicionado ao banco!"

@app.get("/filmes")
async def all_filmes():
    """ Retorna todos os filmes existentes no banco de dados. """

    filmes = load(open('filmes.json', "r"))
    return filmes

@app.get("/filmes/{filme_id}")
async def read_filme(filme_id: int):
    """ Retorna o filme, recebdno o id especificado como argumento, com todos os dados do filme. """

    filmes = load(open('filmes.json', "r"))
    for filme in filmes:
        if filme.get('id') == filme_id:
            return filme
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Não foi achado o filme com esse id.")

@app.delete("/filmes/{filme_id}")
async def delete_filme(filme_id: int):
    """ Deleta um filme com o id especificado, checando se o filme realmente existe no banco de dados, e também
deleta todas as avaliações ligadas a ele no banco de dados. """

    filmes = load(open('filmes.json', "r"))
    avaliacoes = load(open('avaliacoes.json', 'r')) 
    for filme in filmes:
        if filme.get('id') == filme_id:
            filmes.remove(filme)
            dump(filmes, open('filmes.json', "w", encoding = 'utf8'), indent = 2)
            for avaliacao in avaliacoes:
                if avaliacao.get('id') == filme_id:
                    avaliacoes.remove(avaliacao)
    
            return "O filme foi deletado do banco!"
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Não foi achado o item para ser deletado.")

@app.put("/filmes/{filme_id}")
async def update_filme(filme_id: int, filme: Filme):
    """ O usuário pode alterar os dados de um filme, checando se realmente o filme existe para dar o update. """

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
            return "O filme teve seus dados atualizados."
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi achado o item para ser alterado.")

@app.post("/avaliacao")
async def create_avaliacao(avaliacao: Avaliacao):
    """ Usuário pode gerenciar cadastro de avaliações de filmes. """

    avaliacao = avaliacao.dict()
    filmes = load(open('filmes.json', "r")) 
    for filme in filmes: 
        if filme['id'] == avaliacao['filme_id']: 
            avaliacoes = load(open('avaliacoes.json', "r")) 
            quantidade_id = load(open('id_avaliacoes.json', "r"))
            
            nova_avaliacao = {} 
            nova_avaliacao['id'] = quantidade_id + 1 
            nova_avaliacao.update(avaliacao) 
            avaliacoes.append(nova_avaliacao) 
            
            dump(quantidade_id + 1, open('id_avaliacoes.json', "w")) 
            dump(avaliacoes, open('avaliacoes.json', "w", encoding='utf8'),ensure_ascii = False, indent = 2) 
            avaliacoes = load(open('filmes.json', 'r')) 
            return "A avaliação foi adicionada ao banco!"
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O filme não existe na base!") 
    
@app.get("/filmes/{filme_id}/avaliacao")
async def read_avaliacao(filme_id: int):
    """ Retorna todas as avaliacoes de um filme com o id especificado (pode ter mais de uma avaliação). """ 

    filmes = load(open('filmes.json', "r")) 
    for filme in filmes: 
        if filme.get('id') == filme_id: 
            avaliacoes = load(open('avaliacoes.json', "r")) 
            avaliacoes_filme = [] 

            for avaliacao in avaliacoes: 
                if avaliacao.get('filme_id') == filme_id: 
                    avaliacoes_filme.append(avaliacao) 
            
            return avaliacoes_filme 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="O filme não existe na base!") 

@app.put("/avaliacao/{avaliacao_id}")
async def update_avaliacao(avaliacao_id: int, avaliacao: Avaliacao_Update):
    """ Permite ao usuário alterar a nota e o comentário feito em alguma avaliação. """

    avaliacoes = load(open('avaliacoes.json', "r"))  
    for avali in avaliacoes: 
        if avali.get('id') == avaliacao_id: 
            avaliacao = avaliacao.dict() 
            avali['avaliacao'] = avaliacao['avaliacao'] 
            avali['comentario'] = avaliacao['comentario'] 
            
            dump(avaliacoes, open('avaliacoes.json', "w", encoding='utf8'), indent = 2) 
            
            return "A avaliação foi atualizada no banco de dados." 
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi achadada a avaliação para ser alterada.")

@app.delete("/avaliacao/{avaliacao_id}")
async def delete_avaliacao(avaliacao_id: int):
    """ O usuário pode deletar uma avaliação de um filme. """

    avaliacoes = load(open('avaliacoes.json', "r")) 
    for avali in avaliacoes:  
        if avali.get('id') == avaliacao_id: 
            avaliacoes.remove(avali) 
            dump(avaliacoes, open('avaliacoes.json', "w", encoding='utf8'), indent = 2)
            
            return "A avaliação foi deletada." 
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não foi achadada a avaliação para ser deletada.") 

@app.get("/avaliacoes")
async def all_avaliacoes():
    """ Retorna todos as avaliações existentes no banco de dados. """

    avaliacoes = load(open('avaliacoes.json', "r"))
    return avaliacoes