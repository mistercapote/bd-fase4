from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse
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
            return redirect(f'/formulario/inserir/{tabela}')
        elif acao == "atualizar":
            return redirect(f'/formulario/atualizar/{tabela}')
        elif acao == "listar":
            return redirect(f'/listar/{tabela}')
        elif acao == "deletar":
            return redirect(f'/deletar/{tabela}')
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
            'tabelas_com_chave_composta': ['usrlelivro', 'usurseguusr', 'usrsegueaut', 'usravaliaaut']
        })
        
def deletar(request, tabela, *params):
    chaves = PRIMARY_KEYS.get(tabela)
    if not chaves:
        return HttpResponseBadRequest("Tabela inválida.")
    if request.method == "POST":
        query = f"DELETE FROM {tabela} WHERE " + " AND ".join([f"{chave} = %s" for chave in chaves])
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return HttpResponse(f"{tabela} {params} excluido com sucesso")
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
            query = "INSERT INTO estado (estadoid, nomeestado) VALUES (%s, %s);"
            params = [estadoid, nomeestado]
            mensagem_sucesso = f"Estado {nomeestado} inserido com sucesso!"
        elif tabela == "livro":
            livroid = request.POST.get('livroid')
            nomelivro = request.POST.get('nomelivro')
            query = "INSERT INTO livro (livroid, nomelivro) VALUES (%s, %s);"
            params = [livroid, nomelivro]
            mensagem_sucesso = f"Livro {nomelivro} inserido com sucesso!"
        elif tabela == "editora":
            editoraid = request.POST.get('editoraid')
            nomeeditora = request.POST.get('nomeeditora')
            siteoficial = request.POST.get('siteoficial')
            descricaoeditora = request.POST.get('descricaoeditora')
            query = ("INSERT INTO editora (editoraid, nomeeditora, siteoficial, descricaoeditora) VALUES (%s, %s, %s, %s);")
            params = [editoraid, nomeeditora, siteoficial, descricaoeditora]
            mensagem_sucesso = f"Editora {nomeeditora} inserida com sucesso!"
        elif tabela == "autor":
            autorid = request.POST.get('autorid')
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')
            query = "INSERT INTO autor (autorid, nomeautor, descricaoautor) VALUES (%s, %s, %s);"
            params = [autorid, nomeautor, descricaoautor]
            mensagem_sucesso = f"Autor {nomeautor} inserido com sucesso!"
        elif tabela == "livroaut":
            livroid = request.POST.get('livroid')
            autorid = request.POST.get('autorid')
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
            query = ("INSERT INTO edicao (edicaoid, anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
            params = [edicaoid, anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid]
            mensagem_sucesso = f"Edição {edicaoid} inserida com sucesso!"
        elif tabela == "avaliacao":
            avalid = request.POST.get('avalid')
            tituloaval = request.POST.get('tituloaval')
            corpoaval = request.POST.get('corpoaval')
            avalid = int(avalid) if avalid else None
            query = "INSERT INTO avaliacao (avalid, tituloaval, corpoaval) VALUES (%s, %s, %s);"
            params = [avalid, tituloaval, corpoaval]
            mensagem_sucesso = f"Avaliação {tituloaval} inserida com sucesso!"
        elif tabela == "cidade":
            cidadeid = request.POST.get('cidadeid')
            nomecidade = request.POST.get('nomecidade')
            estadoid = request.POST.get('estadoid')
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
            query = ("INSERT INTO usuario (usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
            params = [usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid]
            mensagem_sucesso = f"Usuário {nomeusuario} inserido com sucesso!"
        elif tabela == "usrlelivro":
            statusleitura = request.POST.get('statusleitura')
            notalivro = request.POST.get('notalivro')
            usuarioid = request.POST.get('usuarioid')
            livroid = request.POST.get('livroid')
            avalid = request.POST.get('avalid')
            query = ("INSERT INTO usrlelivro (statusleitura, notalivro, usuarioid, livroid, avalid) VALUES (%s, %s, %s, %s, %s);")
            params = [statusleitura, notalivro, usuarioid, livroid, avalid]
            mensagem_sucesso = f"Status de leitura inserido com sucesso!"
        elif tabela == "usrsegueaut":
            datasegaut = request.POST.get('datasegaut')
            usuarioid = request.POST.get('usuarioid')
            autorid = request.POST.get('autorid')
            query = "INSERT INTO usrsegueaut (datasegaut, usuarioid, autorid) VALUES (%s, %s, %s);"
            params = [datasegaut, usuarioid, autorid]
            mensagem_sucesso = f"Usuário começou a seguir o autor com sucesso!"
        elif tabela == "usravaliaaut":
            notaautor = request.POST.get('notaautor')
            autorid = request.POST.get('autorid')
            usuarioid = request.POST.get('usuarioid')
            query = "INSERT INTO usravaliaaut (notaautor, autorid, usuarioid) VALUES (%s, %s, %s);"
            params = [notaautor, autorid, usuarioid]
            mensagem_sucesso = f"Avaliação do autor inserida com sucesso!"
        elif tabela == "usurseguusr":
            datasegusr = request.POST.get('datasegusr')
            seguidorid = request.POST.get('seguidorid')
            seguidoid = request.POST.get('seguidoid')
            query = "INSERT INTO usurseguusr (datasegusr, seguidorid, seguidoid) VALUES (%s, %s, %s);"
            params = [datasegusr, seguidorid, seguidoid]
            mensagem_sucesso = f"Usuário começou a seguir outro usuário com sucesso!"
        else:
            return HttpResponseBadRequest("Tabela inválida.")

        if query:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return HttpResponse(mensagem_sucesso)

def editar(request, tabela, *params):
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
            return render(request, 'usuario.html', {'dados': dados, 'estados': estados_dict})
        else:
            return render(request, f"{tabela}.html", {'dados': dados})
        
    elif request.method == "POST":
        query = None
        params = []
        mensagem_sucesso = ""

        if tabela == "estado":
            estadoid = request.POST.get('estadoid')
            nomeestado = request.POST.get('nomeestado')
            query = "UPDATE estado SET nomeestado = %s WHERE estadoid = %s;"
            params = [nomeestado, estadoid]
            mensagem_sucesso = f"Estado {nomeestado} atualizado com sucesso!"
        elif tabela == "livro":
            livroid = request.POST.get('livroid')
            nomelivro = request.POST.get('nomelivro')
            query = "UPDATE livro SET nomelivro = %s WHERE livroid = %s;"
            params = [nomelivro, livroid]
            mensagem_sucesso = f"Livro {nomelivro} atualizado com sucesso!"
        elif tabela == "editora":
            editoraid = request.POST.get('editoraid')
            nomeeditora = request.POST.get('nomeeditora')
            siteoficial = request.POST.get('siteoficial')
            descricaoeditora = request.POST.get('descricaoeditora')
            query = ("UPDATE editora SET nomeeditora = %s, siteoficial = %s, descricaoeditora = %s "
                        "WHERE editoraid = %s;")
            params = [nomeeditora, siteoficial, descricaoeditora, editoraid]
            mensagem_sucesso = f"Editora {nomeeditora} atualizada com sucesso!"
        elif tabela == "autor":
            autorid = request.POST.get('autorid')
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')
            query = "UPDATE autor SET nomeautor = %s, descricaoautor = %s WHERE autorid = %s;"
            params = [nomeautor, descricaoautor, autorid]
            mensagem_sucesso = f"Autor {nomeautor} atualizado com sucesso!"
        elif tabela == "livroaut":
            livroid = request.POST.get('livroid')
            autorid = request.POST.get('autorid')
            query = "UPDATE livroaut SET autorid = %s WHERE livroid = %s;"
            params = [autorid, livroid]
            mensagem_sucesso = f"Relacionamento Livro-Autor atualizado com sucesso!"
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
            query = ("UPDATE edicao SET anopublicacao = %s, isbn13 = %s, isbn10 = %s, idioma = %s, numpaginas = %s, descricaoedicao = %s, livroid = %s, editoraid = %s WHERE edicaoid = %s;")
            params = [anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid, edicaoid]
            mensagem_sucesso = f"Edição {edicaoid} atualizada com sucesso!"
        elif tabela == "avaliacao":
            avalid = request.POST.get('avalid')
            tituloaval = request.POST.get('tituloaval')
            corpoaval = request.POST.get('corpoaval')
            avalid = int(avalid) if avalid else None
            query = "UPDATE avaliacao SET tituloaval = %s, corpoaval = %s WHERE avalid = %s;"
            params = [tituloaval, corpoaval, avalid]
            mensagem_sucesso = f"Avaliação {tituloaval} atualizada com sucesso!"
        elif tabela == "cidade":
            cidadeid = request.POST.get('cidadeid')
            nomecidade = request.POST.get('nomecidade')
            estadoid = request.POST.get('estadoid')
            query = "UPDATE cidade SET nomecidade = %s, estadoid = %s WHERE cidadeid = %s;"
            params = [nomecidade, estadoid, cidadeid]
            mensagem_sucesso = f"Cidade {nomecidade} atualizada com sucesso!"
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
            query = ("UPDATE usuario SET nomeusuario = %s, senha = %s, emailusuario = %s, datanascimento = %s, genero = %s, fotoperfil = %s, biografia = %s, apelido = %s, cidadeid = %s WHERE usuarioid = %s;")
            params = [nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid, usuarioid]
            mensagem_sucesso = f"Usuário {nomeusuario} atualizado com sucesso!"
        elif tabela == "usrlelivro":
            statusleitura = request.POST.get('statusleitura')
            notalivro = request.POST.get('notalivro')
            usuarioid = request.POST.get('usuarioid')
            livroid = request.POST.get('livroid')
            avalid = request.POST.get('avalid')
            query = ("UPDATE usrlelivro SET statusleitura = %s, notalivro = %s, usuarioid = %s, livroid = %s, avalid = %s WHERE usuarioid = %s AND livroid = %s;")
            params = [statusleitura, notalivro, usuarioid, livroid, avalid, usuarioid, livroid]
            mensagem_sucesso = f"Status de leitura atualizado com sucesso!"
        elif tabela == "usrsegueaut":
            datasegaut = request.POST.get('datasegaut')
            usuarioid = request.POST.get('usuarioid')
            autorid = request.POST.get('autorid')
            query = "UPDATE usrsegueaut SET datasegaut = %s WHERE usuarioid = %s AND autorid = %s;"
            params = [datasegaut, usuarioid, autorid]
            mensagem_sucesso = f"Atualização de seguimento do autor realizada com sucesso!"
        elif tabela == "usravaliaaut":
            notaautor = request.POST.get('notaautor')
            autorid = request.POST.get('autorid')
            usuarioid = request.POST.get('usuarioid')
            query = "UPDATE usravaliaaut SET notaautor = %s WHERE autorid = %s AND usuarioid = %s;"
            params = [notaautor, autorid, usuarioid]
            mensagem_sucesso = f"Avaliação do autor atualizada com sucesso!"
        elif tabela == "usurseguusr":
            datasegusr = request.POST.get('datasegusr')
            seguidorid = request.POST.get('seguidorid')
            seguidoid = request.POST.get('seguidoid')
            query = "UPDATE usurseguusr SET datasegusr = %s WHERE seguidorid = %s AND seguidoid = %s;"
            params = [datasegusr, seguidorid, seguidoid]
            mensagem_sucesso = f"Atualização de seguimento de usuário realizada com sucesso!"
        else:
            return HttpResponseBadRequest("Tabela inválida.")

        if query:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return HttpResponse(mensagem_sucesso)

