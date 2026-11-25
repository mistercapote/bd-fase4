-- Criação do schema skoob, se ainda não existir
CREATE SCHEMA IF NOT EXISTS skoob;

---

-- Tabela: skoob.autor
CREATE TABLE skoob.autor (
    autorid INT PRIMARY KEY,
    nomeautor VARCHAR(64) NOT NULL,
    descricaoautor TEXT NOT NULL
);

---

-- Tabela: skoob.avaliacao
CREATE TABLE skoob.avaliacao (
    avalid INT PRIMARY KEY,
    tituloaval VARCHAR(64) NOT NULL,
    corpoaval VARCHAR(512) NOT NULL
);


---

-- Tabela: skoob.estado
CREATE TABLE skoob.estado (
    estadoid CHAR(2) PRIMARY KEY,
    nomeestado VARCHAR(64) NOT NULL
);

---

-- Tabela: skoob.cidade
CREATE TABLE skoob.cidade (
    cidadeid INT PRIMARY KEY,
    nomecidade VARCHAR(128) NOT NULL,
    estadoid CHAR(2) NOT NULL,
    CONSTRAINT cidade_estadoid_fkey FOREIGN KEY (estadoid) REFERENCES skoob.estado(estadoid)
);

---

-- Tabela: skoob.editora
CREATE TABLE skoob.editora (
    editoraid INT PRIMARY KEY,
    nomeeditora VARCHAR(64) NOT NULL,
    siteoficial VARCHAR(128),
    descricaoeditora TEXT
);

---

-- Tabela: skoob.livro
CREATE TABLE skoob.livro (
    livroid INT PRIMARY KEY,
    nomelivro VARCHAR(64) NOT NULL
);

---

-- Tabela: skoob.edicao
CREATE TABLE skoob.edicao (
    edicaoid INT PRIMARY KEY,
    anopublicacao DATE NOT NULL,
    isbn13 VARCHAR(13),
    isbn10 VARCHAR(10),
    idioma VARCHAR(32) NOT NULL,
    numpaginas INT NOT NULL,
    descricaoedicao TEXT NOT NULL,
    livroid INT NOT NULL,
    editoraid INT NOT NULL,
    CONSTRAINT edicao_livroid_fkey FOREIGN KEY (livroid) REFERENCES skoob.livro(livroid),
    CONSTRAINT edicao_editoraid_fkey FOREIGN KEY (editoraid) REFERENCES skoob.editora(editoraid)
);

---

-- Tabela: skoob.livroaut
CREATE TABLE skoob.livroaut (
    livroid INT NOT NULL,
    autorid INT NOT NULL,
    PRIMARY KEY (livroid, autorid),
    CONSTRAINT livroaut_livroid_fkey FOREIGN KEY (livroid) REFERENCES skoob.livro(livroid),
    CONSTRAINT livroaut_autorid_fkey FOREIGN KEY (autorid) REFERENCES skoob.autor(autorid)
);

---

-- Tabela: skoob.usuario
CREATE TABLE skoob.usuario (
    usuarioid INT PRIMARY KEY,
    nomeusuario VARCHAR(64) NOT NULL,
    senha VARCHAR(32) NOT NULL,
    emailusuario VARCHAR(64) NOT NULL UNIQUE,
    datanascimento DATE,
    genero INT,
    fotoperfil VARCHAR(512),
    biografia VARCHAR(312),
    apelido VARCHAR(64) NOT NULL,
    cidadeid INT NOT NULL,
    CONSTRAINT usuario_cidadeid_fkey FOREIGN KEY (cidadeid) REFERENCES skoob.cidade(cidadeid)
);

---

-- Tabela: skoob.usravaliaaut
CREATE TABLE skoob.usravaliaaut (
    notaautor INT NOT NULL,
    autorid INT NOT NULL,
    usuarioid INT NOT NULL,
    PRIMARY KEY (autorid, usuarioid),
    CONSTRAINT usravaliaaut_autorid_fkey FOREIGN KEY (autorid) REFERENCES skoob.autor(autorid),
    CONSTRAINT usravaliaaut_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES skoob.usuario(usuarioid)
);

---

-- Tabela: skoob.usrlelivro
CREATE TABLE skoob.usrlelivro (
    statusleitura VARCHAR(16) NOT NULL,
    notalivro INT,
    usuarioid INT NOT NULL,
    livroid INT NOT NULL,
    avalid INT UNIQUE, -- Adicionado UNIQUE para avalid, onde não é nulo
    PRIMARY KEY (usuarioid, livroid),
    CONSTRAINT usrlelivro_avalid_fkey FOREIGN KEY (avalid) REFERENCES skoob.avaliacao(avalid),
    CONSTRAINT usrlelivro_livroid_fkey FOREIGN KEY (livroid) REFERENCES skoob.livro(livroid),
    CONSTRAINT usrlelivro_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES skoob.usuario(usuarioid)
);
-- Adicionando a restrição UNIQUE com WHERE para avalid, se necessário e suportado pelo seu SGBD (PostgreSQL)
-- ALTER TABLE skoob.usrlelivro ADD CONSTRAINT uq_usrlelivro_avalid_not_null UNIQUE (avalid) WHERE avalid IS NOT NULL;


---

-- Tabela: skoob.usrsegueaut
CREATE TABLE skoob.usrsegueaut (
    datasegaut DATE NOT NULL,
    usuarioid INT NOT NULL,
    autorid INT NOT NULL,
    PRIMARY KEY (usuarioid, autorid),
    CONSTRAINT usrsegueaut_autorid_fkey FOREIGN KEY (autorid) REFERENCES skoob.autor(autorid),
    CONSTRAINT usrsegueaut_usuarioid_fkey FOREIGN KEY (usuarioid) REFERENCES skoob.usuario(usuarioid)
);

---

-- Tabela: skoob.usrsegueusr
CREATE TABLE skoob.usrsegueusr (
    datasegusr DATE NOT NULL,
    seguidorid INT NOT NULL,
    seguidoid INT NOT NULL,
    PRIMARY KEY (seguidorid, seguidoid),
    CONSTRAINT usursegueusr_seguidorid_fkey FOREIGN KEY (seguidorid) REFERENCES skoob.usuario(usuarioid),
    CONSTRAINT usursegueusr_seguidoid_fkey FOREIGN KEY (seguidoid) REFERENCES skoob.usuario(usuarioid)
);