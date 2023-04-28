DROP DATABASE IF EXISTS sql_app;
CREATE DATABASE IF NOT EXISTS sql_app;

USE sql_app;

DROP TABLE IF EXISTS Filme;
    CREATE TABLE Filme (
     id INT NOT NULL AUTO_INCREMENT,
	 nome VARCHAR(50) NOT NULL,
     diretor VARCHAR(300) NOT NULL,
     ano_lancamento INT NOT NULL,
	 genero VARCHAR(50) NOT NULL,
     PRIMARY KEY (id)
);

DROP TABLE IF EXISTS Avaliacao;
    CREATE TABLE Avaliacao (
     id INT NOT NULL AUTO_INCREMENT,
	 avaliacao INT NOT NULL,
     comentario VARCHAR(300) NOT NULL,
	 filme_id INT NOT NULL,
     FOREIGN KEY (filme_id) REFERENCES Filme(id) ON DELETE CASCADE,
     PRIMARY KEY (id)
);
