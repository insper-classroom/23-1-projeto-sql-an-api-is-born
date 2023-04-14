# API de Filmes e Avaliações
### Essa é uma API criada com o FastAPI para gerenciar filmes e suas avaliações. 

## A API possui os seguintes endpoints:

POST /filme
- Cria um novo filme no banco de dados.
- Não é possível criar dois filmes com o mesmo nome e ano de lançamento.
- O ID do filme é gerado automaticamente, com base no último ID registrado.
- Os dados do filme são salvos no arquivo filmes.json.

GET /filmes
- Retorna todos os filmes existentes no banco de dados.
- Os dados dos filmes são obtidos a partir do arquivo filmes.json.

GET /filmes/{filme_id}
- Retorna os dados de um filme específico com base em seu ID.
- Os dados do filme são obtidos a partir do arquivo filmes.json.

DELETE /filmes/{filme_id}
- Deleta um filme específico com base em seu ID.
- Também deleta todas as avaliações relacionadas a esse filme no banco de dados.
- Os dados do filme são removidos do arquivo filmes.json e as avaliações são removidas do arquivo avaliacoes.json.

PUT /filmes/{filme_id}
- Permite atualizar os dados de um filme específico com base em seu ID.
- Os dados atualizados são passados no corpo da requisição em formato JSON.
- Os dados do filme são atualizados no arquivo filmes.json.

GET /filmes/{filme_id}/avaliacao
- Retorna todas as avaliações de um filme com o ID especificado

POST /avaliacao
- Cria uma nova avaliação para um filme específico com base em seu ID.
- Os dados da avaliação, como a nota e o comentário, são salvos no arquivo avaliacoes.json.

GET /avaliacoes
- Retorna todas as avaliações existentes no banco de dados.
- Os dados das avaliações são obtidos a partir do arquivo avaliacoes.json.

GET /avaliacoes/{avaliacao_id}
- Retorna os dados de uma avaliação específica com base em seu ID.
- Os dados da avaliação são obtidos a partir do arquivo avaliacoes.json.

PUT /avaliacoes/{avaliacao_id}
- Permite atualizar os dados de uma avaliação específica com base em seu ID.
- Os dados atualizados são passados no corpo da requisição em formato JSON.
- Os dados da avaliação são atualizados no arquivo avaliacoes.json.

DELETE /avaliacoes/{avaliacao_id}
- Deleta uma avaliação específica com base em seu ID.
- Os dados da avaliação são removidos do arquivo avaliacoes.json.
