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
            return redirect(f'/inserir/{tabela}')
        elif acao == "atualizar":
            return redirect(f'/atualizar/{tabela}')
        elif acao == "listar":
            return redirect(f'/listar/{tabela}')
        elif acao == "deletar":
            return redirect(f'/deletar/{tabela}')
    return HttpResponseBadRequest("Método não suportado.")


def inserir(request, tabela):
    if request.method == "GET":
        return render(request, f'{tabela}.html')
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
            return HttpResponse(f"Usuário {nomeusuario} inserido com sucesso!")

        elif tabela == "autor":
            autorid = request.POST.get('autorid')
            nomeautor = request.POST.get('nomeautor')
            descricaoautor = request.POST.get('descricaoautor')
            return HttpResponse("Autor inserido com sucesso!")

        elif tabela == "avaliacao":
            avalid = request.POST.get('avalid')
            tituloaval = request.POST.get('tituloaval')
            corpoaval = request.POST.get('corpoaval')
            return HttpResponse("Avaliação inserida com sucesso!")
        if tabela == "usuario":
            return render(request, 'usuario.html')
        elif tabela == "autor":
            return render(request, 'autor.html')
        elif tabela == "avaliacao":
            return render(request, 'avaliacao.html')
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
    
        

# def atualizar(request):
#     pass

# def listar(request):
#     pass

# def deletar(request):
#     pass
