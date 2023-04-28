from pydantic import BaseModel, Field
from typing import Annotated

class AvaliacaoBase(BaseModel):
    avaliacao: Annotated[int, Field(gt=-1, lt=6)]
    comentario: str = Field(
        default = None, description = "Comentário sobre o filme", max_length = 300
    )
    filme_id: int = Field(
        description = "O id do filme interligado ao modelo Filme criado anteriormente."
    )

class AvaliacaoCreate(AvaliacaoBase):
    pass

class AvaliacaoUpdate(BaseModel):
    avaliacao: Annotated[int, Field(gt=-1, lt=6)]
    comentario: str = Field(
        default = None, description = "Comentário sobre o filme", max_length = 300
    )


class Avaliacao(AvaliacaoBase):
    """ Cria uma classe de avaliacoes de filmes de 0.0 a 10.0, um campo de texto livre e o id do filme. """
    id: int = Field(
        description = "O id da avaliação, criado automaticamente."
    )
    
    class Config:
        orm_mode = True

class FilmeBase(BaseModel):
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

class FilmeCreate(FilmeBase):
    pass

class FilmeUpdate(FilmeBase):
    pass

class Filme(FilmeBase):
    """ Criação do modelo Filme que irá guardar os dados obtidos dos usuários."""
    id : int = Field(
        description = "O id do filme, criado automaticamente."
    )
    
    class Config:
        orm_mode = True



