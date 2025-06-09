from django.db import connection, transaction
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.http import JsonResponse

PRIMARY_KEYS = {
    'usuario': ['usuarioid'],
    'autor': ['autorid'],
    'avaliacao': ['avalid'],
    'cidade': ['cidadeid'],
    'estado': ['estadoid'],
    'livroaut': ['livroid', 'autorid'],
    'usrsegueusr': ['seguidorid', 'seguidoid'],
    'usravaliaaut': ['usuarioid', 'autorid'],
    'usrlelivro': ['usuarioid', 'livroid'],
    'usrsegueaut': ['usuarioid', 'autorid'],
    'edicao': ['edicaoid'],
    'editora': ['editoraid'],
    'livro': ['livroid'],
}

def iniciar(request):
    if request.method == "GET":
        return render(request, 'buttons.html')
    elif request.method == "POST":
        acao = request.POST.get('acao')
        tabela = request.POST.get('tabela')

        if not acao or not tabela:
            return HttpResponseBadRequest("Ação e tabela são obrigatórias.")
        if acao == "inserir":
            return redirect(f'/inserir/{tabela}')
        elif acao == "listar":
            return redirect(f'/listar/{tabela}')
    return HttpResponseBadRequest("Método não suportado.")

def cidades_por_estado(request, estado_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT cidadeid, nomecidade FROM cidade WHERE estadoid = %s", [estado_id])
        rows = cursor.fetchall()

    cidades = [{'id': row[0], 'nome': row[1]} for row in rows]
    return JsonResponse(cidades, safe=False)


def listar(request, tabela):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tabela} ")
            colunas = [col[0] for col in cursor.description]
            resultados = cursor.fetchall()

        return render(request, 'listar.html', {
            'colunas': colunas,
            'resultados': resultados,
            'tabela': tabela,
            'tabelas_com_chave_composta': ['livroaut', 'usrlelivro', 'usrsegueusr', 'usrsegueaut', 'usravaliaaut'],
            'tabelas_nao_editaveis': ['livroaut', 'usrsegueusr', 'usrsegueaut']
        })
        
def deletar(request, tabela, params, params2=None):
    if params2: 
        params = [params, params2]
    else: 
        params = [params]
    
    chaves = PRIMARY_KEYS.get(tabela)
    if not chaves:
        return HttpResponseBadRequest("Tabela inválida.")
    
    if request.method == "POST":
        try:
            with transaction.atomic(): 
                with connection.cursor() as cursor:
                    # 1. Encontrar todas as constraints de chave estrangeira que referenciam nossa tabela
                    cursor.execute("""
                        SELECT
                            conname,
                            conrelid::regclass AS foreign_table,
                            a.attname AS foreign_column
                        FROM
                            pg_constraint c
                        JOIN
                            pg_namespace n ON n.oid = c.connamespace
                        JOIN
                            pg_class cl ON cl.oid = c.conrelid
                        JOIN
                            pg_attribute a ON a.attnum = ANY(c.conkey) AND a.attrelid = c.conrelid
                        WHERE
                            c.confrelid = (SELECT oid FROM pg_class WHERE relname = %s LIMIT 1)
                            AND c.contype = 'f'
                    """, [tabela])
                    dependencias = cursor.fetchall()

                    # Para debug - mostrar as dependências encontradas
                    print(f"Dependências encontradas para {tabela}: {dependencias}")

                # 2. Deletar dependências
                for constraint_name, foreign_table, foreign_column in dependencias:
                    try:
                        # Construir a query de deleção baseada no tipo de chave
                        if len(chaves) == 1:
                            delete_query = f"DELETE FROM {foreign_table} WHERE {foreign_column} = %s"
                            delete_params = params
                        else:
                            # Para chaves compostas
                            conditions = []
                            delete_params = []
                            for i, chave in enumerate(chaves):
                                if foreign_column.lower() == chave.lower():
                                    conditions.append(f"{foreign_column} = %s")
                                    delete_params.append(params[i])
                            
                            if not conditions:
                                continue
                                
                            delete_query = f"DELETE FROM {foreign_table} WHERE " + " AND ".join(conditions)
                        
                        print(f"Executando: {delete_query} com params {delete_params}")
                        with connection.cursor() as cursor:
                            cursor.execute(delete_query, delete_params)
                    except Exception as e:
                        print(f"Erro ao deletar de {foreign_table}: {str(e)}")
                        raise

                # 3. Deletar da tabela principal
                delete_principal = f"DELETE FROM {tabela} WHERE " + " AND ".join([f"{chave} = %s" for chave in chaves])
                print(f"Executando principal: {delete_principal} com params {params}")
                with connection.cursor() as cursor:
                    cursor.execute(delete_principal, params)
                
                return redirect(f"/listar/{tabela}")
                
        except Exception as e:
            return HttpResponseBadRequest(f"Erro ao deletar: {str(e)}")
def inserir(request, tabela):
    if request.method == "GET":
        if tabela == "usuario":
            with connection.cursor() as cursor:
                cursor.execute("SELECT estadoid, nomeestado FROM estado")
                estados = cursor.fetchall() 
                estados_dict = [{'estadoid': row[0], 'nomeestado': row[1]} for row in estados]
            return render(request, 'usuario.html', {'dados': {}, 'estados': estados_dict})
        else:
            return render(request, f"{tabela}.html", {'dados': {}})
    elif request.method == "POST":
        query = ""
        params = []
        mensagem_sucesso = ""

        if tabela == "estado":
            estadoid = request.POST.get('estadoid')
            nomeestado = request.POST.get('nomeestado')
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM estado WHERE estadoid = %s", [estadoid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: O estado com ID {estadoid} já existe.")
            
            
            query = "INSERT INTO estado (estadoid, nomeestado) VALUES (%s, %s);"
            params = [estadoid, nomeestado]
            mensagem_sucesso = f"Estado {nomeestado} inserido com sucesso!"
        elif tabela == "livro":
            livroid = request.POST.get('livroid')
            nomelivro = request.POST.get('nomelivro')
            # Verificar se o livro já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM livro WHERE livroid = %s", [livroid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: O livro com ID {livroid} já existe.")
            
            query = "INSERT INTO livro (livroid, nomelivro) VALUES (%s, %s);"
            params = [livroid, nomelivro]
            mensagem_sucesso = f"Livro {nomelivro} inserido com sucesso!"
        elif tabela == "editora":
            editoraid = request.POST.get('editoraid')
            nomeeditora = request.POST.get('nomeeditora')
            siteoficial = request.POST.get('siteoficial')
            descricaoeditora = request.POST.get('descricaoeditora')
             # Verificar se a editora já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM editora WHERE editoraid = %s", [editoraid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: A editora com ID {editoraid} já existe.")
            query = ("INSERT INTO editora (editoraid, nomeeditora, siteoficial, descricaoeditora) VALUES (%s, %s, %s, %s);")
            params = [editoraid, nomeeditora, siteoficial, descricaoeditora]
            mensagem_sucesso = f"Editora {nomeeditora} inserida com sucesso!"
        
        elif tabela == "autor":
            
            autorid = request.POST.get('autorid')
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM autor WHERE autorid = %s", [autorid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: O autor com ID {autorid} já existe.")
    
            query = "INSERT INTO autor (autorid, nomeautor, descricaoautor) VALUES (%s, %s, %s);"
            params = [autorid, nomeautor, descricaoautor]
            mensagem_sucesso = f"Autor {nomeautor} inserido com sucesso!"
        elif tabela == "livroaut":
            livroid = request.POST.get('livroid')
            autorid = request.POST.get('autorid')
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM livroaut WHERE livroid = %s AND autorid = %s", [livroid, autorid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: Este relacionamento livro-autor já existe.")
            
            query = "INSERT INTO livroaut (livroid, autorid) VALUES (%s, %s);"
            params = [livroid, autorid]
            mensagem_sucesso = f"Relacionamento Livro-Autor inserido com sucesso!"
        elif tabela == "edicao":
            edicaoid = request.POST.get('edicaoid')
            anopublicacao = request.POST.get('anopublicacao')
            isbn13 = request.POST.get('isbn13')
            isbn10 = request.POST.get('isbn10')
            idioma = request.POST.get('idioma')
            numpaginas = request.POST.get('numpaginas')
            descricaoedicao = request.POST.get('descricaoedicao')
            livroid = request.POST.get('livroid')
            editoraid = request.POST.get('editoraid')
            
            # Verificar se a edição já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM edicao WHERE edicaoid = %s", [edicaoid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: A edição com ID {edicaoid} já existe.")
            
            query = ("INSERT INTO edicao (edicaoid, anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
            params = [edicaoid, anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid]
            mensagem_sucesso = f"Edição {edicaoid} inserida com sucesso!"
        elif tabela == "avaliacao":
            avalid = request.POST.get('avalid')
            tituloaval = request.POST.get('tituloaval')
            corpoaval = request.POST.get('corpoaval')
            avalid = int(avalid) if avalid else None
            
            # Verificar se a avaliação já existe (se avalid foi fornecido)
            if avalid is not None:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT 1 FROM avaliacao WHERE avalid = %s", [avalid])
                    if cursor.fetchone():
                        return HttpResponseBadRequest(f"Erro: A avaliação com ID {avalid} já existe.")
            
            
            query = "INSERT INTO avaliacao (avalid, tituloaval, corpoaval) VALUES (%s, %s, %s);"
            params = [avalid, tituloaval, corpoaval]
            mensagem_sucesso = f"Avaliação {tituloaval} inserida com sucesso!"
        
        elif tabela == "cidade":
            cidadeid = request.POST.get('cidadeid')
            nomecidade = request.POST.get('nomecidade')
            estadoid = request.POST.get('estadoid')
            # Verificar se a cidade já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM cidade WHERE cidadeid = %s", [cidadeid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: A cidade com ID {cidadeid} já existe.")
            
            query = "INSERT INTO cidade (cidadeid, nomecidade, estadoid) VALUES (%s, %s, %s);"
            params = [cidadeid, nomecidade, estadoid]
            mensagem_sucesso = f"Cidade {nomecidade} inserida com sucesso!"
            
            query = "INSERT INTO cidade (cidadeid, nomecidade, estadoid) VALUES (%s, %s, %s);"
            params = [cidadeid, nomecidade, estadoid]
            mensagem_sucesso = f"Cidade {nomecidade} inserida com sucesso!"
        elif tabela == "usuario":
            usuarioid = request.POST.get('usuarioid')
            nomeusuario = request.POST.get('nomeusuario')
            senha = request.POST.get('senha')
            emailusuario = request.POST.get('emailusuario')
            datanascimento = request.POST.get('datanascimento')
            genero = request.POST.get('genero')
            fotoperfil = request.POST.get('fotoperfil') 
            biografia = request.POST.get('biografia')
            apelido = request.POST.get('apelido')
            cidadeid = request.POST.get('cidadeid')
            
             # Verificar se o usuário já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usuario WHERE usuarioid = %s", [usuarioid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: O usuário com ID {usuarioid} já existe.")
                
                # Verificar se o email já está cadastrado
                cursor.execute("SELECT 1 FROM usuario WHERE emailusuario = %s", [emailusuario])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: O email {emailusuario} já está cadastrado para outro usuário.")
                
                
            query = ("INSERT INTO usuario (usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
            params = [usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid]
            mensagem_sucesso = f"Usuário {nomeusuario} inserido com sucesso!"
        elif tabela == "usrlelivro":
            statusleitura = request.POST.get('statusleitura')
            notalivro = request.POST.get('notalivro')
            notalivro = int(notalivro) if notalivro else None
            usuarioid = request.POST.get('usuarioid')
            livroid = request.POST.get('livroid')
            avalid = request.POST.get('avalid')
            avalid = int(avalid) if avalid else None
            
            # Verificar se o relacionamento já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usrlelivro WHERE usuarioid = %s AND livroid = %s", [usuarioid, livroid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: Este relacionamento usuário-livro já existe.")
            query = ("INSERT INTO usrlelivro (statusleitura, notalivro, usuarioid, livroid, avalid) VALUES (%s, %s, %s, %s, %s);")
            params = [statusleitura, notalivro, usuarioid, livroid, avalid]
            mensagem_sucesso = f"Status de leitura inserido com sucesso!"
        elif tabela == "usrsegueaut":
            datasegaut = request.POST.get('datasegaut')
            usuarioid = request.POST.get('usuarioid')
            autorid = request.POST.get('autorid')
            # Verificar se o relacionamento já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usrsegueaut WHERE usuarioid = %s AND autorid = %s", [usuarioid, autorid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: Este relacionamento usuário-autor já existe.")
            
            query = "INSERT INTO usrsegueaut (datasegaut, usuarioid, autorid) VALUES (%s, %s, %s);"
            params = [datasegaut, usuarioid, autorid]
            mensagem_sucesso = f"Usuário começou a seguir o autor com sucesso!"
        elif tabela == "usravaliaaut":
            notaautor = request.POST.get('notaautor')
            autorid = request.POST.get('autorid')
            usuarioid = request.POST.get('usuarioid')
            # Verificar se o relacionamento já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usravaliaaut WHERE autorid = %s AND usuarioid = %s", [autorid, usuarioid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: Este relacionamento avaliação-autor já existe.")
            
            query = "INSERT INTO usravaliaaut (notaautor, autorid, usuarioid) VALUES (%s, %s, %s);"
            params = [notaautor, autorid, usuarioid]
            mensagem_sucesso = f"Avaliação do autor inserida com sucesso!"
        elif tabela == "usrsegueusr":
            datasegusr = request.POST.get('datasegusr')
            seguidorid = request.POST.get('seguidorid')
            seguidoid = request.POST.get('seguidoid')
            
            # Verificar se o relacionamento já existe
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usrsegueusr WHERE seguidorid = %s AND seguidoid = %s", [seguidorid, seguidoid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: Este relacionamento seguidor-seguido já existe.")
            query = "INSERT INTO usrsegueusr (datasegusr, seguidorid, seguidoid) VALUES (%s, %s, %s);"
            params = [datasegusr, seguidorid, seguidoid]
            mensagem_sucesso = f"Usuário começou a seguir outro usuário com sucesso!"
        else:
            return HttpResponseBadRequest("Tabela inválida.")

        if query:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                return redirect('/')
            except Exception as e:
                return HttpResponseBadRequest(f"Erro ao inserir: {str(e)}")

def editar(request, tabela, params, params2=None):
    if params2: params = [params, params2]
    else: params = [params]
    if request.method == "GET":
        chaves = PRIMARY_KEYS.get(tabela)
        query = f"SELECT * FROM {tabela} WHERE " + " AND ".join([f"{chave} = %s" for chave in chaves])
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                col_names = [col[0] for col in cursor.description]
                dados = dict(zip(col_names, row))
        if tabela == "usuario":
            with connection.cursor() as cursor:
                cursor.execute("SELECT estadoid, nomeestado FROM estado")
                estados = cursor.fetchall() 
                estados_dict = [{'estadoid': row[0], 'nomeestado': row[1]} for row in estados]
                
            estado_selecionado = None
            cidadeid = dados.get('cidadeid')
            if cidadeid:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT estadoid FROM cidade WHERE cidadeid = %s", [cidadeid])
                    resultado = cursor.fetchone()
                    if resultado:
                        estado_selecionado = resultado[0]
                    
            return render(request, 'usuario.html', {'dados': dados, 'estados': estados_dict, 'estado_selecionado': estado_selecionado,})
        else:
            return render(request, f"{tabela}.html", {'dados': dados})
        
    elif request.method == "POST":
        query = None
        parametros = []
        mensagem_sucesso = ""

        if tabela == "estado":
            estadoid = params[0]
            nomeestado = request.POST.get('nomeestado')
            query = "UPDATE estado SET nomeestado = %s WHERE estadoid = %s;"
            parametros = [nomeestado, estadoid]
            mensagem_sucesso = f"Estado {nomeestado} atualizado com sucesso!"
        elif tabela == "livro":
            livroid = params[0]
            nomelivro = request.POST.get('nomelivro')
            query = "UPDATE livro SET nomelivro = %s WHERE livroid = %s;"
            parametros = [nomelivro, livroid]
            mensagem_sucesso = f"Livro {nomelivro} atualizado com sucesso!"
        elif tabela == "editora":
            editoraid = params[0]
            nomeeditora = request.POST.get('nomeeditora')
            siteoficial = request.POST.get('siteoficial')
            descricaoeditora = request.POST.get('descricaoeditora')
            query = ("UPDATE editora SET nomeeditora = %s, siteoficial = %s, descricaoeditora = %s "
                        "WHERE editoraid = %s;")
            parametros = [nomeeditora, siteoficial, descricaoeditora, editoraid]
            mensagem_sucesso = f"Editora {nomeeditora} atualizada com sucesso!"
        elif tabela == "autor":
            autorid = params[0]
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')
            query = "UPDATE autor SET nomeautor = %s, descricaoautor = %s WHERE autorid = %s;"
            parametros = [nomeautor, descricaoautor, autorid]
            mensagem_sucesso = f"Autor {nomeautor} atualizado com sucesso!"
        elif tabela == "livroaut":
            livroid = params[0]
            autorid = params[1]
            query = "UPDATE livroaut SET autorid = %s WHERE livroid = %s;"
            parametros = [autorid, livroid]
            mensagem_sucesso = f"Relacionamento Livro-Autor atualizado com sucesso!"
        elif tabela == "edicao":
            edicaoid = params[0]
            anopublicacao = request.POST.get('anopublicacao')
            isbn13 = request.POST.get('isbn13')
            isbn10 = request.POST.get('isbn10')
            idioma = request.POST.get('idioma')
            numpaginas = request.POST.get('numpaginas')
            descricaoedicao = request.POST.get('descricaoedicao')
            livroid = request.POST.get('livroid')
            editoraid = request.POST.get('editoraid')
            query = ("UPDATE edicao SET anopublicacao = %s, isbn13 = %s, isbn10 = %s, idioma = %s, numpaginas = %s, descricaoedicao = %s, livroid = %s, editoraid = %s WHERE edicaoid = %s;")
            parametros = [anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid, edicaoid]
            mensagem_sucesso = f"Edição {edicaoid} atualizada com sucesso!"
        elif tabela == "avaliacao":
            avalid = params[0]
            tituloaval = request.POST.get('tituloaval')
            corpoaval = request.POST.get('corpoaval')
            avalid = int(avalid) if avalid else None
            query = "UPDATE avaliacao SET tituloaval = %s, corpoaval = %s WHERE avalid = %s;"
            parametros = [tituloaval, corpoaval, avalid]
            mensagem_sucesso = f"Avaliação {tituloaval} atualizada com sucesso!"
        elif tabela == "cidade":
            cidadeid = params[0]
            nomecidade = request.POST.get('nomecidade')
            estadoid = request.POST.get('estadoid')
            query = "UPDATE cidade SET nomecidade = %s, estadoid = %s WHERE cidadeid = %s;"
            parametros = [nomecidade, estadoid, cidadeid]
            mensagem_sucesso = f"Cidade {nomecidade} atualizada com sucesso!"
        elif tabela == "usuario":
            usuarioid = params[0]
            nomeusuario = request.POST.get('nomeusuario')
            senha = request.POST.get('senha')
            emailusuario = request.POST.get('emailusuario')
            datanascimento = request.POST.get('datanascimento')
            genero = request.POST.get('genero')
            fotoperfil = request.POST.get('fotoperfil') 
            biografia = request.POST.get('biografia')
            apelido = request.POST.get('apelido')
            cidadeid = request.POST.get('cidadeid')
            datanascimento = datanascimento if datanascimento else None
            genero = int(genero) if genero else None
            query = ("UPDATE usuario SET nomeusuario = %s, senha = %s, emailusuario = %s, datanascimento = %s, genero = %s, fotoperfil = %s, biografia = %s, apelido = %s, cidadeid = %s WHERE usuarioid = %s;")
            parametros = [nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid, usuarioid]
            mensagem_sucesso = f"Usuário {nomeusuario} atualizado com sucesso!"
            
            # Verificar se o email já está sendo usado por OUTRO usuário
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM usuario WHERE emailusuario = %s AND usuarioid != %s", 
                              [emailusuario, usuarioid])
                if cursor.fetchone():
                    return HttpResponseBadRequest(f"Erro: O email {emailusuario} já está cadastrado para outro usuário.")
            
            query = ("UPDATE usuario SET nomeusuario = %s, senha = %s, emailusuario = %s, "
                    "datanascimento = %s, genero = %s, fotoperfil = %s, biografia = %s, "
                    "apelido = %s, cidadeid = %s WHERE usuarioid = %s;")
            parametros = [nomeusuario, senha, emailusuario, datanascimento, genero, 
                     fotoperfil, biografia, apelido, cidadeid, usuarioid]
        
        elif tabela == "usrlelivro":
            statusleitura = request.POST.get('statusleitura')
            notalivro = request.POST.get('notalivro')
            notalivro = int(notalivro) if notalivro else None
            usuarioid = params[0]
            livroid = params[1]
            avalid = request.POST.get('avalid')
            avalid = int(avalid) if avalid else None
            query = ("UPDATE usrlelivro SET statusleitura = %s, notalivro = %s, usuarioid = %s, livroid = %s, avalid = %s WHERE usuarioid = %s AND livroid = %s;")
            parametros = [statusleitura, notalivro, usuarioid, livroid, avalid, usuarioid, livroid]
            mensagem_sucesso = f"Status de leitura atualizado com sucesso!"
        elif tabela == "usrsegueaut":
            datasegaut = request.POST.get('datasegaut')
            usuarioid = params[0]
            autorid = params[0]
            query = "UPDATE usrsegueaut SET datasegaut = %s WHERE usuarioid = %s AND autorid = %s;"
            parametros = [datasegaut, usuarioid, autorid]
            mensagem_sucesso = f"Atualização de seguimento do autor realizada com sucesso!"
        elif tabela == "usravaliaaut":
            notaautor = request.POST.get('notaautor')
            usuarioid = params[0]
            autorid = params[1]
            query = "UPDATE usravaliaaut SET notaautor = %s WHERE autorid = %s AND usuarioid = %s;"
            parametros = [notaautor, autorid, usuarioid]
            mensagem_sucesso = f"Avaliação do autor atualizada com sucesso!"
        elif tabela == "usrsegueusr":
            datasegusr = request.POST.get('datasegusr')
            seguidorid = params[0]
            seguidoid = params[1]
            query = "UPDATE usrsegueusr SET datasegusr = %s WHERE seguidorid = %s AND seguidoid = %s;"
            parametros = [datasegusr, seguidorid, seguidoid]
            mensagem_sucesso = f"Atualização de seguimento de usuário realizada com sucesso!"
        else:
            return HttpResponseBadRequest("Tabela inválida.")

        if query:
            with connection.cursor() as cursor:
                cursor.execute(query, parametros)
            return redirect(f"/listar/{tabela}")
