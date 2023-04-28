from fastapi import FastAPI, HTTPException, status, Depends
from json import *
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import *

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

@app.post("/filme", response_model= schemas.Filme, tags=["Filme"])
async def create_filme(filme: schemas.FilmeCreate, db: Session = Depends(get_db)):
    
    db_filme = crud.create_filme(db, filme)
    if db_filme == True:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme já existe no banco de dados.")
   
    return db_filme

@app.get("/filmes", response_model= list[schemas.Filme], tags=["Filme"])
async def all_filmes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    filmes = crud.get_filmes(db, skip=skip, limit=limit)
    return filmes

@app.get("/filmes/{filme_id}", response_model= schemas.Filme, tags=["Filme"])
async def read_filme(filme_id: int, db: Session = Depends(get_db)):

    db_filme = crud.get_filme(db, filme_id=filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return db_filme

@app.put("/filmes/{filme_id}", response_model= schemas.Filme, tags=["Filme"])
async def update_filme(filme_id: int, filme: schemas.FilmeUpdate, db: Session = Depends(get_db)):

    db_filme = crud.get_filme(db, filme_id=filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return crud.update_filme(db=db, filme=filme, filme_id=filme_id)

@app.delete("/filmes/{filme_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Filme"])
async def delete_filme(filme_id: int, db: Session = Depends(get_db)):

    db_filme = crud.get_filme(db, filme_id=filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return crud.delete_filme(db=db, filme_id=filme_id)

@app.post("/avaliacao", response_model= schemas.Avaliacao, tags=["Avaliação"])
async def create_avaliacao(avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
    
    db_filme = crud.get_filme(db, filme_id=avaliacao.filme_id)
    if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
    return crud.create_avaliacao(db=db, avaliacao=avaliacao)
    
@app.get("/filmes/{filme_id}/avaliacao", response_model= list[schemas.Avaliacao], tags=["Avaliação"])
async def read_avaliacao(filme_id: int, db: Session = Depends(get_db)):

   db_filme = crud.get_filme(db, filme_id=filme_id)
   if db_filme is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Filme não encontrado.")
   return crud.get_avaliacoes_filme(db, filme_id=filme_id)
  
@app.put("/avaliacao/{avaliacao_id}", response_model= schemas.Avaliacao, tags=["Avaliação"])
async def update_avaliacao(avaliacao_id: int, avaliacao: schemas.AvaliacaoUpdate, db: Session = Depends(get_db)):

    db_avaliacao = crud.get_avaliacao(db, avaliacao_id=avaliacao_id)
    if db_avaliacao is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Avaliação não encontrada.")
    return crud.update_avaliacao(db=db, avaliacao_id=avaliacao_id, avaliacao=avaliacao)

@app.delete("/avaliacao/{avaliacao_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Avaliação"])
async def delete_avaliacao(avaliacao_id: int, db: Session = Depends(get_db)):

    db_avaliacao = crud.get_avaliacao(db, avaliacao_id=avaliacao_id)
    if db_avaliacao is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Avaliação não encontrada.")
    return crud.delete_avaliacao(db=db, avaliacao_id=avaliacao_id)

@app.get("/avaliacoes", response_model= list[schemas.Avaliacao], tags=["Avaliação"])
async def all_avaliacoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):

    avaliacoes = crud.get_avaliacoes(db, skip=skip, limit=limit)
    return avaliacoes
   