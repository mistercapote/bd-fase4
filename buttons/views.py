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
            elif acao == "atualizar":
                query = "UPDATE usuario SET nomeusuario = %s, senha = %s, emailusuario = %s, datanascimento = %s, genero = %s, fotoperfil = %s, biografia = %s, apelido = %s, cidadeid = %s WHERE usuarioid = %s;"
    
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
            return render(request, 'cidade.html')
        elif tabela == "edicao":
            return render(request, 'edicao.html')
        elif tabela == "editora":
            return render(request, 'editora.html')
        elif tabela == "livro":
            return render(request, 'livro.html')
        elif tabela == "livroaut":
            return render(request, 'livroaut.html')
        elif tabela == "usravaliaaut":
            return render(request, 'usravaliaaut.html')
        elif tabela == "usrlelivro":
            return render(request, 'usrlelivro.html')
        elif tabela == "usrsegueaut":
            return render(request, 'usrsegueaut.html')
        elif tabela == "usrsegueusr":
            return render(request, 'usrsegueusr.html')
    
        
# def listar(request, tabela):
#     query = f"SELECT * FROM {tabela};"
    
# def deletar(request, tabela):
#     id = request.POST.get('id')
