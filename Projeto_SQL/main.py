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
mesmo nome e ano de lançamento, cria o id automaticamente, devido ao 'id.json' que guarda o último id criado. A 
função também deve adicionar o filme criado no fim do 'filmes.json'."""
    
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




@app.put("/filmes/{filme_id}")
async def update_filme(filme_id: int, filme: schemas.FilmeUpdate, db: Session = Depends(get_db)):
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
async def create_avaliacao(avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(get_db)):
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
async def update_avaliacao(avaliacao_id: int, avaliacao: schemas.AvaliacaoUpdate, db: Session = Depends(get_db)):
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