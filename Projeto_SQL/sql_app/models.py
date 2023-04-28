from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Filme(Base):
    __tablename__ = "filme"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), index=True)
    diretor = Column(String(300), index=True)
    ano_lancamento = Column(Integer, index=True)
    genero = Column(String(50), index=True)

class Avaliacao(Base):
    __tablename__ = "avaliacao"

    id = Column(Integer, primary_key=True, index=True)
    avaliacao = Column(Integer, index=True)
    comentario = Column(String(300), index=True)
    filme_id = Column(Integer, ForeignKey("filme.id"))

