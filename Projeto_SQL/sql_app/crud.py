from sqlalchemy.orm import Session

from . import models, schemas

def create_filme(db: Session, filme: schemas.FilmeCreate):
    """ Criação de novos filmes para adicionar ao banco de dados, não sendo possível a criação de dois filmes com 
    o mesmo nome e ano de lançamento. """
    
    lista = get_filmes(db)
    for i in lista:
        if filme.nome == i.nome and filme.ano_lancamento == i.ano_lancamento:
            return True
    db_filme = models.Filme(nome=filme.nome, diretor=filme.diretor, ano_lancamento=filme.ano_lancamento, genero=filme.genero)
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme

def get_filme(db: Session, filme_id: int):
    """ Retorna o filme, recebendo o id especificado como argumento, com todos os dados do filme. """
   
    return db.query(models.Filme).filter(models.Filme.id == filme_id).first()

def get_filmes(db: Session, skip: int = 0, limit: int = 100):
    """ Retorna todos os filmes existentes no banco de dados. """

    return db.query(models.Filme).offset(skip).limit(limit).all()

def update_filme(db: Session, filme_id: int, filme: schemas.FilmeCreate):
    """ O usuário pode alterar os dados de um filme, checando se realmente o filme existe para dar o update. """

    db_filme = db.query(models.Filme).filter(models.Filme.id == filme_id).first()
    db_filme.nome = filme.nome
    db_filme.diretor = filme.diretor
    db_filme.ano_lancamento = filme.ano_lancamento
    db_filme.genero = filme.genero
    db.commit()
    db.refresh(db_filme)
    return db_filme

def delete_filme(db: Session, filme_id: int):
    """ O usuário pode deletar um filme, checando se realmente o filme existe para dar o delete. """

    db_filme = db.query(models.Filme).filter(models.Filme.id == filme_id).first()
    db.delete(db_filme)
    db.commit()
    return db_filme

#criar uma nova avaliação
def create_avaliacao(db: Session, avaliacao: schemas.AvaliacaoCreate):
    db_avaliacao = models.Avaliacao(avaliacao=avaliacao.avaliacao, comentario=avaliacao.comentario, filme_id=avaliacao.filme_id)
    db.add(db_avaliacao)
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao

#retornar uma avaliação pelo id
def get_avaliacao(db: Session, avaliacao_id: int):
    return db.query(models.Avaliacao).filter(models.Avaliacao.id == avaliacao_id).first()

#retornar todas as avaliações de um filme
def get_avaliacoes_filme(db: Session, filme_id: int):
    return db.query(models.Avaliacao).filter(models.Avaliacao.filme_id == filme_id).all()

#retornar todas as avaliações
def get_avaliacoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Avaliacao).offset(skip).limit(limit).all()

#atualizar uma avaliação
def update_avaliacao(db: Session, avaliacao_id: int, avaliacao: schemas.AvaliacaoCreate):
    db_avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id == avaliacao_id).first()
    db_avaliacao.avaliacao = avaliacao.avaliacao
    db_avaliacao.comentario = avaliacao.comentario
    db.commit()
    db.refresh(db_avaliacao)
    return db_avaliacao

#deletar uma avaliação
def delete_avaliacao(db: Session, avaliacao_id: int):
    db_avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id == avaliacao_id).first()
    db.delete(db_avaliacao)
    db.commit()
    return db_avaliacao

