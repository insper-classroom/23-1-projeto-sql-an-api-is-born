from fastapi import FastAPI, HTTPException, status, Depends
from json import *
from sqlalchemy.orm import Session
from . import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# Inicialização e criação da API
app = FastAPI(title="An API is born",
              description="API criada para guardar filmes e suas avaliações.")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Criação do json que serve para guardar o valor do id e servir como um id auto incremento
quantidade_id = load(open('id.json', "r"))


# class Avaliacao_Update(BaseModel):
#     """ Utilizado para poder fazer o update da avaliação sem alterar os id's dos filmes. """

#     avaliacao: Annotated[float, Field(gt=0, lt=10)]
#     comentario: str = Field(
#         default = None, description = "Comentário sobre o filme", max_length = 300
#     )
    
@app.post("/filme", response_model= schemas.Filme)
async def create_filme(filme: schemas.FilmeCreate, db: Session = Depends(get_db)):
    """ Criação de novos filmes para adicionar ao banco de dados, não sendo possível a criação de dois filmes com 
    o mesmo nome e ano de lançamento. """
    
    db_filme = crud.get_filme_by_nome(db, nome=filme.nome)
    #se o filme já existir, verifica se o ano de lançamento é o mesmo
    if db_filme:
        if db_filme.ano_lancamento == filme.ano_lancamento:
            raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Filme já existente.")
    #se o filme não existir, cria o filme
    return crud.create_filme(db=db, filme=filme)

@app.get("/filmes", response_model= list[schemas.Filme])
async def all_filmes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Retorna todos os filmes existentes no banco de dados. """

    filmes = crud.get_filmes(db, skip=skip, limit=limit)
    return filmes

    
@app.get("/filmes/{filme_id}", response_model= schemas.Filme)
async def read_filme(filme_id: int, db: Session = Depends(get_db)):
    """ Retorna o filme, recebdno o id especificado como argumento, com todos os dados do filme. """

    db_filme = crud.get_filme(db, filme_id=filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return db_filme

# update de filme
@app.put("/filmes/{filme_id}", response_model= schemas.Filme)
async def update_filme(filme_id: int, filme: schemas.FilmeUpdate, db: Session = Depends(get_db)):
    """ O usuário pode alterar os dados de um filme, checando se realmente o filme existe para dar o update. """
    
    db_filme = crud.get_filme(db, filme_id=filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return crud.update_filme(db=db, filme=filme, filme_id=filme_id)

# delete de filme  (colocar on delete cascade para deletar as avaliações do filme)
@app.delete("/filmes/{filme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_filme(filme_id: int, db: Session = Depends(get_db)):
    """ O usuário pode deletar um filme, checando se realmente o filme existe para dar o delete. """

    db_filme = crud.get_filme(db, filme_id=filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return crud.delete_filme(db=db, filme_id=filme_id)

# criar avaliação
@app.post("/avaliacao", response_model= schemas.Avaliacao)
async def create_avaliacao(avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    """ Usuário pode criar uma avaliação para um filme, sendo que o filme deve existir no banco de dados. """
    
    db_filme = crud.get_filme(db, filme_id=avaliacao.filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return crud.create_avaliacao(db=db, avaliacao=avaliacao)
    
# ler avaliação
@app.get("/filmes/{filme_id}/avaliacao", response_model= list[schemas.Avaliacao])
async def read_avaliacao(filme_id: int, db: Session = Depends(get_db)):
   """Retorna as avaliações de um filme, recebendo o id do filme como argumento. As avaliações vem do banco de dados, não do json"""
   db_filme = crud.get_filme(db, filme_id=filme_id)
   if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
   return crud.get_avaliacoes_filme(db, filme_id=filme_id)

    
# update de avaliação
@app.put("/avaliacao/{avaliacao_id}", response_model= schemas.Avaliacao)
async def update_avaliacao(avaliacao_id: int, avaliacao: schemas.AvaliacaoUpdate, db: Session = Depends(get_db)):
    """ Permite ao usuário alterar a nota e o comentário feito em alguma avaliação. """

    db_avaliacao = crud.get_avaliacao(db, avaliacao_id=avaliacao_id)
    if db_avaliacao is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Avaliação não encontrada.")
    return crud.update_avaliacao(db=db, avaliacao=avaliacao, avaliacao_id=avaliacao_id)

# delete de avaliação
@app.delete("/avaliacao/{avaliacao_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avaliacao(avaliacao_id: int, db: Session = Depends(get_db)):
    """ O usuário pode deletar uma avaliação de um filme. """

    db_avaliacao = crud.get_avaliacao(db, avaliacao_id=avaliacao_id)
    if db_avaliacao is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Avaliação não encontrada.")
    return crud.delete_avaliacao(db=db, avaliacao_id=avaliacao_id)


# listar todas as avaliações (skip e limit opcionais passados como argumentos na url)
@app.get("/avaliacoes", response_model= list[schemas.Avaliacao])
async def all_avaliacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Retorna todas as avaliações existentes no banco de dados. """

    avaliacoes = crud.get_avaliacoes(db, skip=skip, limit=limit)
    return avaliacoes
   