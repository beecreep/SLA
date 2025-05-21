CREATE TABLE usuarios (
	id INTEGER NOT NULL, 
	nome VARCHAR(150) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	senha VARCHAR(150) NOT NULL, 
	turma VARCHAR(50), 
	numero VARCHAR(50), 
	role VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
CREATE TABLE atividades (
	id INTEGER NOT NULL, 
	titulo VARCHAR NOT NULL, 
	descricao VARCHAR NOT NULL, 
	arquivo BLOB, 
	extensao VARCHAR(10), 
	data_envio DATETIME, 
	PRIMARY KEY (id)
);
CREATE TABLE respostas (
	id INTEGER NOT NULL, 
	aluno_id INTEGER NOT NULL, 
	atividade_id INTEGER NOT NULL, 
	resposta TEXT NOT NULL, 
	arquivo_resposta BLOB, 
	extensao VARCHAR(10), 
	data_resposta DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(aluno_id) REFERENCES usuarios (id), 
	FOREIGN KEY(atividade_id) REFERENCES atividades (id)
);
CREATE TABLE mensagens (
	id INTEGER NOT NULL, 
	usuario_id INTEGER NOT NULL, 
	mensagem TEXT, 
	arquivo BLOB, 
	extensao VARCHAR(10), 
	timestamp DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);
CREATE TABLE cronogramas (
	id INTEGER NOT NULL, 
	usuario_id INTEGER NOT NULL, 
	turma VARCHAR(50) NOT NULL, 
	dia_semana VARCHAR(50) NOT NULL, 
	horario VARCHAR(10) NOT NULL, 
	aula VARCHAR(150), 
	professor VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(usuario_id) REFERENCES usuarios (id)
);
