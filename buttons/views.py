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
        query = None
        params = []
        mensagem_sucesso = ""

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
                query = ("INSERT INTO usuario "
                         "(usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
                params = [usuarioid, nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid]
                mensagem_sucesso = f"Usuário {nomeusuario} inserido com sucesso!"
            elif acao == "atualizar":
                query = ("UPDATE usuario SET nomeusuario = %s, senha = %s, emailusuario = %s, datanascimento = %s, "
                         "genero = %s, fotoperfil = %s, biografia = %s, apelido = %s, cidadeid = %s WHERE usuarioid = %s;")
                params = [nomeusuario, senha, emailusuario, datanascimento, genero, fotoperfil, biografia, apelido, cidadeid, usuarioid]
                mensagem_sucesso = f"Usuário {nomeusuario} atualizado com sucesso!"

        elif tabela == "autor":
            autorid = request.POST.get('autorid')
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')

            if acao == "inserir":
                query = "INSERT INTO autor (autorid, nomeautor, descricaoautor) VALUES (%s, %s, %s);"
                params = [autorid, nomeautor, descricaoautor]
                mensagem_sucesso = f"Autor {nomeautor} inserido com sucesso!"
            elif acao == "atualizar":
                query = "UPDATE autor SET nomeautor = %s, descricaoautor = %s WHERE autorid = %s;"
                params = [nomeautor, descricaoautor, autorid]
                mensagem_sucesso = f"Autor {nomeautor} atualizado com sucesso!"

        # Repita essa estrutura para as outras tabelas...

        # No final, executa a query se tiver sido criada
        if query:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            return HttpResponse(mensagem_sucesso)
        else:
            return HttpResponseBadRequest("Ação ou tabela inválida.")



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
