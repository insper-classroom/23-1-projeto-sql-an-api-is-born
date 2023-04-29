# API de Filmes e Avaliações
### Essa é uma API criada com o FastAPI para gerenciar filmes e suas avaliações. 

### O diagrama ER do projeto está abaixo:
![Imagem do WhatsApp de 2023-04-28 à(s) 18 11 10](https://user-images.githubusercontent.com/72052521/235273891-855c2d17-463e-4368-9c68-f6553cc3a537.jpg)

### O vídeo descrevendo e demonstrando as atualizações do handout 02 na API pode ser acessado aqui:https://youtu.be/mJt3WxHqSoI

### O vídeo (parte 1 do projeto) descrevendo e demonstrando as funcionalidades da API pode ser acessado aqui: https://youtu.be/n9Ev8t0KOdo .
-------------------------------------------------
## Como rodar o projeto?
- Clone o repositório localmente.
- Rode o scrip "cria_banco.sql".
- No mesmo nível do arquivo "cria_banco.sql", crie um arquivo ".env" com seguinte conteúdo:
```python
database_url = mysql+mysqlconnector://{user}:{password}@localhost:3306/sql_app
```
- Subistitua **{user}** e **{password}** por suas credencias de conexão. 
- Finalmente, rode o comando abaixo no terminal:
```python
uvicorn sql_app.main:app --reload
```
-------------------------------------------------
## A API possui os seguintes endpoints:

POST /filme
- Cria um novo filme no banco de dados.
- Não é possível criar dois filmes com o mesmo nome e ano de lançamento.
- O ID do filme é gerado automaticamente, com base no último ID registrado.
- Os dados do filme são salvos no arquivo filmes.json.

GET /filmes
- Retorna todos os filmes existentes no banco de dados.

GET /filmes/{filme_id}
- Retorna os dados de um filme específico com base em seu ID.

DELETE /filmes/{filme_id}
- Deleta um filme específico com base em seu ID.
- Também deleta todas as avaliações relacionadas a esse filme no banco de dados.

PUT /filmes/{filme_id}
- Permite atualizar os dados de um filme específico com base em seu ID.

GET /filmes/{filme_id}/avaliacao
- Retorna todas as avaliações de um filme com o ID especificado

POST /avaliacao
- Cria uma nova avaliação para um filme específico com base em seu ID.

GET /avaliacoes
- Retorna todas as avaliações existentes no banco de dados.

GET /avaliacoes/{avaliacao_id}
- Retorna os dados de uma avaliação específica com base em seu ID.

PUT /avaliacoes/{avaliacao_id}
- Permite atualizar os dados de uma avaliação específica com base em seu ID.

DELETE /avaliacoes/{avaliacao_id}
- Deleta uma avaliação específica com base em seu ID.
