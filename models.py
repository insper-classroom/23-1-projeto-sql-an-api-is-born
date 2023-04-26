from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    diretor = Column(String, index=True)
    ano_lancamento = Column(Integer, index=True)
    genero = Column(String, index=True)

    avaliacoes = relationship("Avaliacao", back_populates="filme")

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, index=True)
    avaliacao = Column(Integer, index=True)
    comentario = Column(String, index=True)
    filme_id = Column(Integer, ForeignKey("filmes.id"))

    filme = relationship("Filme", back_populates="avaliacoes")

