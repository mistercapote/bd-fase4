from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponse

# Create your views here.
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


def formulario(request, acao, tabela):
    if request.method == "GET":
        return render(request, f'{tabela}.html', {'acao': acao})
    elif request.method == "POST":
        if tabela == "usuario":
            usuarioid = request.POST.get('usuarioid')
            nomeusuario = request.POST.get('nomeusuario')
            senha = request.POST.get('senha')
            emailusuario = request.POST.get('emailusuario')
            datanascimento = request.POST.get('datanascimento')
            genero = request.POST.get('genero')
            fotoperfil = request.FILES.get('fotoperfil') 
            biografia = request.POST.get('biografia')
            apelido = request.POST.get('apelido')
            cidadeid = request.POST.get('cidadeid')
            
            if acao == "inserir":
                query = f"INSERT INTO usuario (usuarioid, nomeusuario, senha, emailusuario,datanascimento, genero, fotoperfil, biografia, apelido, cidadeid) VALUES ({usuarioid},'{nomeusuario}', '{senha}', '{emailusuario}', '{datanascimento}', {genero}, '{fotoperfil}', '{biografia}', '{apelido}', {cidadeid});"
                with connection.cursor() as cursor:
                    cursor.execute(query, [
                    usuarioid, nomeusuario, senha, emailusuario,
                    datanascimento, genero,  biografia, apelido, cidadeid
                ])
            elif acao == "atualizar":
                query = "UPDATE usuario SET nomeusuario = %s, senha = %s, emailusuario = %s, datanascimento = %s, genero = %s, fotoperfil = %s, biografia = %s, apelido = %s, cidadeid = %s WHERE usuarioid = %s;"

                with connection.cursor() as cursor:
                    cursor.execute(query, [
    nomeusuario, senha, emailusuario, datanascimento,
    genero, fotoperfil, biografia, apelido, cidadeid, usuarioid
])


                
            return HttpResponse(f"Usuário {nomeusuario} inserido com sucesso!")

        elif tabela == "autor":
            autorid = request.POST.get('autorid')
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')
            if acao == "inserir":
                query = f"INSERT INTO autor (autorid, nomeautor, descricaoautor) VALUES ({autorid},'{nomeautor}', '{descricaoautor}');"
                return HttpResponse(f"Autor {nomeautor} inserido com sucesso!")
            elif acao == "atualizar":
                query = "UPDATE autor SET nomeautor = %s, descricaoautor = %s WHERE autorid = %s;"
                return HttpResponse(f"Autor {nomeautor} atualizado com sucesso!")
            
        elif tabela == "avaliacao":
            avalid = request.POST.get('avalid')
            tituloaval = request.POST.get('tituloaval')
            corpoaval = request.POST.get('corpoaval')
            if acao == "inserir":
                query = f"INSERT INTO avaliacao (avalid, tituloaval, corpoaval) VALUES ({avalid}, '{tituloaval}', '{corpoaval}');"
            elif acao == "atualizar":
                query = "UPDATE avaliacao SET tituloaval = %s, corpoaval = %s WHERE avalid = %s;"
            return HttpResponse(f"Avaliação {tituloaval} inserida com sucesso!")
        
        elif tabela == "cidade":
            cidadeid = request.POST.get('cidadeid')
            nomecidade = request.POST.get('nomecidade')
            estadoid = request.POST.get('estadoid')

            if acao == "inserir":
                query = f"INSERT INTO cidade (cidadeid, nomecidade, estadoid) VALUES ({cidadeid}, '{nomecidade}', '{estadoid}');"
                return HttpResponse(f"Cidade {nomecidade} inserida com sucesso!")
            elif acao == "atualizar":
                query = "UPDATE cidade SET nomecidade = %s, estadoid = %s WHERE cidadeid = %s;"
                return HttpResponse(f"Cidade {nomecidade} atualizada com sucesso!")

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

            if acao == "inserir":
                query = (f"INSERT INTO edicao (edicaoid, anopublicacao, isbn13, isbn10, idioma, numpaginas, descricaoedicao, livroid, editoraid) "
                        f"VALUES ({edicaoid}, {anopublicacao}, "
                        f"'{isbn13}', '{isbn10}', '{idioma}', {numpaginas}, "
                        f"'{descricaoedicao}', {livroid}, {editoraid});")
                return HttpResponse(f"Edição {edicaoid} inserida com sucesso!")
            elif acao == "atualizar":
                query = ("UPDATE edicao SET anopublicacao = %s, isbn13 = %s, isbn10 = %s, idioma = %s, numpaginas = %s, descricaoedicao = %s, livroid = %s, editoraid = %s "
                        "WHERE edicaoid = %s;")
                return HttpResponse(f"Edição {edicaoid} atualizada com sucesso!")

        elif tabela == "editora":
            editoraid = request.POST.get('editoraid')
            nomeeditora = request.POST.get('nomeeditora')
            siteoficial = request.POST.get('siteoficial')
            descricaoeditora = request.POST.get('descricaoeditora')

            if acao == "inserir":
                query = (
                    f"INSERT INTO editora (editoraid, nomeeditora, siteoficial, descricaoeditora) "
                    f"VALUES ({editoraid}, '{nomeeditora}', '{siteoficial}', '{descricaoeditora}');"
                )
                return HttpResponse(f"Editora {nomeeditora} inserida com sucesso!")

            elif acao == "atualizar":
                query = (
                    "UPDATE editora SET nomeeditora = %s, siteoficial = %s, descricaoeditora = %s "
                    "WHERE editoraid = %s;"
                )
                return HttpResponse(f"Editora {nomeeditora} atualizada com sucesso!")

        elif tabela == "livro":
            livroid = request.POST.get('livroid')
            nomelivro = request.POST.get('nomelivro')

            if acao == "inserir":
                query = (
                    f"INSERT INTO livro (livroid, nomelivro) "
                    f"VALUES ({livroid}, '{nomelivro}');"
                )
                return HttpResponse(f"Livro '{nomelivro}' inserido com sucesso!")

            elif acao == "atualizar":
                query = (
                    "UPDATE livro SET nomelivro = %s "
                    "WHERE livroid = %s;"
                )
                return HttpResponse(f"Livro '{nomelivro}' atualizado com sucesso!")

        if tabela == "livroaut":
            livroid = request.POST.get('livroid')
            autorid = request.POST.get('autorid')

            if acao == "inserir":
                query = f"INSERT INTO livroaut (livroid, autorid) VALUES ({livroid}, {autorid});"
            elif acao == "atualizar":
                query = "UPDATE livroaut SET autorid = %s WHERE livroid = %s;"

            return HttpResponse(f"Relacionamento Livro ({livroid}) ↔ Autor ({autorid}) processado com sucesso!")

        if tabela == "usravaliaaut":
            notaautor = request.POST.get('notaautor')
            autorid = request.POST.get('autorid')
            usuarioid = request.POST.get('usuarioid')

            if acao == "inserir":
                query = f"INSERT INTO usravaliaaut (notaautor, autorid, usuarioid) VALUES ({notaautor}, {autorid}, {usuarioid});"
            elif acao == "atualizar":
                query = "UPDATE usravaliaaut SET notaautor = %s WHERE autorid = %s AND usuarioid = %s;"

            return HttpResponse(f"Avaliação do autor ({autorid}) pelo usuário ({usuarioid}) registrada com nota {notaautor}.")

        if tabela == "usrlelivro":
            statusleitura = request.POST.get('statusleitura')
            notalivro = request.POST.get('notalivro') or 'NULL'
            usuarioid = request.POST.get('usuarioid')
            livroid = request.POST.get('livroid')
            avalid = request.POST.get('avalid') or 'NULL'

            if acao == "inserir":
                query = f"""
                    INSERT INTO usrlelivro (statusleitura, notalivro, usuarioid, livroid, avalid)
                    VALUES ('{statusleitura}', {notalivro}, {usuarioid}, {livroid}, {avalid});
                """
            elif acao == "atualizar":
                query = """
                    UPDATE usrlelivro
                    SET statusleitura = %s, notalivro = %s, avalid = %s
                    WHERE usuarioid = %s AND livroid = %s;
                """

            return HttpResponse(f"Leitura do livro {livroid} registrada para o usuário {usuarioid}.")

        if tabela == "usrsegueaut":
            usuarioid = request.POST.get('usuarioid')
            autorid = request.POST.get('autorid')
            datasegaut = request.POST.get('datasegaut')

            if acao == "inserir":
                query = f"""
                    INSERT INTO usrsegueaut (usuarioid, autorid, datasegaut)
                    VALUES ({usuarioid}, {autorid}, '{datasegaut}');
                """
            elif acao == "atualizar":
                query = """
                    UPDATE usrsegueaut
                    SET datasegaut = %s
                    WHERE usuarioid = %s AND autorid = %s;
                """

            return HttpResponse(f"Usuário {usuarioid} seguiu o autor {autorid}.")

        if tabela == "usrsegueusr":
            datasegusr = request.POST.get('datasegusr')
            seguidorid = request.POST.get('seguidorid')
            seguidoid = request.POST.get('seguidoid')

            if acao == "inserir":
                query = f"""
                    INSERT INTO usrsegueusr (datasegusr, seguidorid, seguidoid)
                    VALUES ('{datasegusr}', {seguidorid}, {seguidoid});
                """
            elif acao == "atualizar":
                query = """
                    UPDATE usrsegueusr
                    SET datasegusr = %s
                    WHERE seguidorid = %s AND seguidoid = %s;
                """

            return HttpResponse(f"Usuário {seguidorid} passou a seguir o usuário {seguidoid}.")


def listar(request, tabela):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {tabela} LIMIT 50")
            colunas = [col[0] for col in cursor.description]
            resultados = cursor.fetchall()

        return render(request, 'listar.html', {
            'colunas': colunas,
            'resultados': resultados,
            'tabela': tabela
        })

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

def deletar(request, tabela):
    chaves = PRIMARY_KEYS.get(tabela)
    if not chaves:
        return HttpResponseBadRequest("Tabela inválida.")

    if request.method == "GET":
        return render(request, 'deletar.html', {'tabela': tabela, 'chaves': chaves})

    elif request.method == "POST":
        valores = []
        condicoes = []

        for chave in chaves:
            valor = request.POST.get(chave)
            if not valor:
                return HttpResponseBadRequest(f"Campo obrigatório: {chave}")
            condicoes.append(f"{chave} = %s")
            valores.append(valor)

        query = f"DELETE FROM {tabela} WHERE " + " AND ".join(condicoes)

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, valores)
        except Exception as e:
            return HttpResponseBadRequest(f"Erro ao deletar: {str(e)}")

        return redirect('iniciar')
