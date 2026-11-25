INSERT INTO skoob.livro (livroid, nomelivro) VALUES
(1, 'Ainda estou aqui'),
(2, 'O festim dos corvos'),
(3, 'Dom Casmurro'),
(4, 'A hora da estrela'),
(5, 'It: a coisa');

INSERT INTO skoob.autor (autorid, nomeautor, descricaoautor) VALUES
(1, 'Machado de Assis', 'Joaquim Maria Machado de Assis, jornalista, contista, cronista, romancista, poeta e teatrólogo, nasceu no Rio de Janeiro, RJ, em 21 de junho de 1839, e faleceu também no Rio de Janeiro, em 29 de setembro de 1908. É o fundador da Cadeira nº. 23 da Academia Brasileira de Letras. Velho amigo e admirador de José de Alencar, que morrera cerca de vinte anos antes da fundação da ABL, era natural que Machado escolhesse o nome do autor de O Guarani para seu patrono. Ocupou por mais de dez anos a presidência da Academia, que passou a ser chamada também de Casa de Machado de Assis.'),
(2, 'Clarice Lispector', 'Clarice Lispector, nascida Haia Lispector (Chechelnyk, 10 de dezembro de 1920 — Rio de Janeiro, 9 de dezembro de 1977) foi uma escritora brasileira, nascida na Ucrânia. Autora de linha introspectiva, buscava exprimir, através de seus textos, as agruras e antinomias do ser. Suas obras caracterizam-se pela exacerbação do momento interior e intensa ruptura com o enredo factual, a ponto de a própria subjetividade entrar em crise.'),
(3, 'Marcelo Rubens Paiva', 'Nascido em São Paulo em 1959, aos 11 anos de idade sofreu o primeiro grande baque de sua vida: o desaparecimento do pai (o ex-Deputado Federal Rubens Paiva) pela ditadura militar. Um despertar violento da consciência política. Estudou na USP e Unicamp. E então aos 20 anos de idade, ele sofreu o segundo grande baque: um acidente que o deixou tetraplégico. Hoje, com muita fisioterapia, voltou a locomover as mãos e os braços.'),
(4, 'George RR Martin', 'George R. R. Martin nasceu em Bayonne, Nova Jérsei, filho de um estivador, cuja família de classa operária vivia perto das docas de Bayonne. Quando jovem, ele se tornou um leitor ávido de quadrinhos de superheróis. A edição de novembro de 1968 do Quarteto Fantástico possui uma nota ao editor que Martin escreveu quando ainda estava na escola. Ele credita a atenção que ele recebeu com a carta, junto com seu interesse em quadrinhos, como sua inspiração para se tornar escritor. Em 1970, Martin recebeu sue Bacharelado em jornalismo na Universidade Northwestern, Illinois, se formando com muitos elogios. Ele depois completou um Mestrado em jornalismo, também em Northwestern, em 1971.'),
(5, 'Stephen King', 'Stephen King era um leitor fanático dos quadrinhos EC''s horror comics incluindo Tales from the crypt, que estimulou seu amor pelo terror. Na escola, ele escrevia histórias baseadas nos filmes que assistia e as copiava com a ajuda de seu irmão David. King as vendia aos amigos, mas seus professores desaprovaram e o forçaram a parar.');

INSERT INTO skoob.avaliacao (avalid, tituloaval, corpoaval) VALUES
(101, 'Mudou minha vida', 'Fui atrás da obra original devido ao filme e não me arrependo.'),
(102, 'Assustador', 'Quase não consigo terminar, grande livro.');

INSERT INTO skoob.estado (estadoid, nomeestado) VALUES
('ES', 'Espírito Santo'),
('MG', 'Minas Gerais'),
('AL', 'Alagoas'),
('RJ', 'Rio de Janeiro'),
('SP', 'São Paulo');

INSERT INTO skoob.cidade (cidadeid, nomecidade, estadoid) VALUES
(47, 'Marilândia', 'ES'),
('192', 'São Miguel dos Campos', 'AL'),
(1636, 'Betim', 'MG'),
(2091, 'Novo Cruzeiro', 'MG'),
(2160, 'Piranga', 'MG');

INSERT INTO skoob.editora (editoraid, nomeeditora, siteoficial, descricaoeditora) VALUES
(1, 'Ática', '', 'Descer Para praia'),
(2, 'LeYa', '', 'Pular na onda'),
(3, 'Rocco', 'https://rocco.com.br/', 'Fundada em 1975, a editora Rocco possui um catálogo eclético de mais de 2 mil títulos em que se encontram obras de referência tanto de ficção quanto de não-ficção. Clarice Lispector, Autran Dourado, Affonso Romano de Sant’Anna e Silviano Santiago são alguns dos destaques do catálogo nacional da editora, que abre espaço também para novos talentos nacionais e estrangeiros. Editora de séries de sucesso no Brasil, como Harry Potter, Jogos Vorazes, Pretty Little Liars e Ciclo A Herança, a Rocco mantém-se atenta aos movimentos do mercado editorial internacional com o compromisso de levar ao leitor brasileiro as principais tendências da literatura e do pensamento mundial.'),
(4, 'Alfaguara', '', 'uma tarde longa'),
(5, 'Moderna', 'https://www.moderna.com.br/', 'Editora com foco em literatura educacional e didática, com um vasto catálogo de obras para todos os níveis de ensino e leitores em geral. Comprometida com a inovação e qualidade no conteúdo.');

INSERT INTO skoob.edicao (
    edicaoid, anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid
) VALUES
(1, '2014-01-01', '9788560280940', '8560280944', 'Português', 1104,
 'Durante as férias escolares de 1958, em Derry, pacata cidadezinha do Maine, Bill, Richie, Stan, Mike, Eddie, Ben e Beverly aprenderam o real sentido da amizade, do amor, da confiança e... do medo. O mais profundo e tenebroso medo. Naquele verão, eles enfrentaram pela primeira vez a Coisa, um ser sobrenatural e maligno que deixou terríveis marcas de sangue em Derry. Quase trinta anos depois, os amigos voltam a se encontrar. Uma nova onda de terror tomou a pequena cidade.',
 5, 5),

(2, '1997-01-01', '9788508040810', '8508040814', 'Português', 216,
 'Machado de Assis (1839-1908), escrevendo Dom Casmurro, produziu um dos maiores livros da literatura universal. Mas criando Capitu, a espantosa menina de "olhos oblíquos e dissimulados", de "olhos de ressaca", Machado nos legou um incrível mistério, um mistério até hoje indecifrado. Há quase cem anos os estudiosos e especialistas o esmiúçam, o analisam sob todos os aspectos. Em vão. Embora o autor se tenha dado ao trabalho de distribuir pelo caminho todas as pistas para quem quisesse decifrar o enigma, ninguém ainda o desvendou.',
 3, 1),

(3, '2015-01-01', '9788579624162', '8579624169', 'Português', 296,
 'Eunice Paiva é uma mulher de muitas vidas. Casada com o deputado Rubens Paiva, esteve ao seu lado quando foi cassado e exilado, em 1964. Mãe de cinco filhos, passou a criá-los sozinha quando, em 1971, o marido foi preso por agentes da ditadura, a seguir torturado e morto. Em meio à dor, ela se reinventou. Voltou a estudar, tornou-se advogada, defensora dos direitos indígenas. Nunca chorou na frente das câmeras.',
 1, 4),

(4, '2011-01-01', '9788580443769', '8580443768', 'Português', 644,
 'Os Ventos do Inverno será o sexto livro da série de fantasia épica As Crônicas de Gelo e Fogo, escrita pelo norte-americano George R. R. Martin e publicada pelas editoras Bantam Spectra e Leya. Seu enredo se passa após os dois livros paralelos da saga, O Festim dos Corvos e A Dança dos Dragões.',
 2, 2),

(5, '2020-01-01', '9786555320350', '6555320354', 'Português', 88,
 'Último livro escrito por Clarice Lispector, A hora da estrela é também uma despedida. Lançada pouco antes de sua morte, em 1977, a obra conta os momentos de criação do escritor Rodrigo S. M. (a própria Clarice) narrando a história de Macabéa, uma alagoana órfã, virgem e solitária, criada por uma tia tirana, que a leva para o Rio de Janeiro, onde trabalha como datilógrafa.',
 4, 3);

INSERT INTO skoob.livroaut (livroid, autorid) VALUES
(1, 3),
(2, 4),
(3, 1),
(4, 2),
(5, 5);

INSERT INTO skoob.usuario (usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid) VALUES
(305, 'Elisa Soares', 'bdElisaS#33', 'elisa.soares305@example.com', '1995-11-11', 0, 'https://randomuser.me/api/portraits/women/55.jpg', 'Apaixonada por fotografia.', 'elisinha', 2160),
(30, 'Luiz Bravin', 'bdC4p0t3456', 'luiz.bravin@example.com', '2003-07-12', 1, 'https://placeimg.com/500/102/flower', 'Um leitor avulso de ficção', 'capote', 47),
(20, 'Elisa Soares', 'eL!5aW41', 'elisa.soares@example.com', '2003-04-04', 0, 'https://placeimg.com/100/10', NULL, 'llwall_', 2160),
(10, 'Jaime William', 'carneirinho', 'jaimecarneiro@gmail.com', '2004-01-10', NULL, 'https://placeimg.com/100/100/people', 'Eu ainda estou aqui!', 'carneirinho', 192),
(40, 'Gabrielle Chacara', 'bd400@', 'gabrielle.chacara@example.com', NULL, 0, 'https://placeimg.com/500/102/taylor', 'Who’s afraid of little old me? You should be', 'x.aca', 2091), 
(50, 'Gustavo Luciano', 'P@s5w0Rd', 'gustavoluciano@gmail.com', '1999-01-31', 1, NULL, 'Mangás são feitos para mim', 'gust', 1636);

INSERT INTO skoob.usravaliaaut (usuarioid, autorid, notaautor) VALUES
(10, 4, 3),
(20, 1, 4),
(30, 3, 4),
(30, 5, 3),
(30, 2, 4);

INSERT INTO skoob.usrlelivro (statusleitura, notalivro, usuarioid, livroid, avalid) VALUES
('Lido', 5, 10, 5, 101),
('Lendo', 4, 305, 4, 102),
('Quero ler', NULL, 305, 3, NULL),
('Abandonei', NULL, 30, 3, NULL),
('Relendo', NULL, 40, 2, NULL),
('Lendo', NULL, 30, 5, NULL),
('Lido', NULL, 30, 4, NULL);

INSERT INTO skoob.usrsegueaut (DataSegAut, UsuarioID, AutorID) VALUES
('2019-03-07', 10, 3),
('2014-09-28', 305, 2),
('2020-10-10', 30, 4),
('2023-11-12', 30, 5),
('2022-07-14', 30, 3);

INSERT INTO skoob.usrsegueusr (DataSegUsr, SeguidorID, SeguidoID) VALUES
('2020-10-10', 10, 20),
('2022-07-14', 20, 10),
('2014-09-28', 20, 40),
('2023-11-12', 30, 50),
('2019-03-07', 50, 30);