from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from PIL import Image, ImageDraw
import os
from Aplicativo.models import User,Post
from django.contrib import messages
import datetime
from pathlib import Path
import numpy

# User.objects.all().delete()
# Post.objects.all().delete()

def excluir_imagem():
    imagens_usuarios = []
    posts = User.objects.all().values()
    s = os.listdir(f'{os.getcwd()}/media')
    
    for i in posts:
        if i['imagem'] not in imagens_usuarios:
            imagens_usuarios.append(i['imagem'])
        # if abrir.tobytes("xbm", "rgb") != j.tobytes("xbm", "rgb") and arquivos != 'anonimo.png':
        #     imagens_nao_usadas.append(arquivos)

    for i in s:
        if i not in imagens_usuarios and i != 'anonimo.png':
            os.remove(f'{os.getcwd()}/media/{i}')
    return

def definir_data():
    data_atual = datetime.datetime.now().strftime("%H:%M %d/%m/%Y")

    return data_atual
    
# Create your views here.

user2 = []
def home(request):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    # if request.method == "POST":
    #     file = request.FILES.get('my_file')
    #     # img = Image.open(file)
    #     # path =  os.path.join(settings.BASE_DIR, f'media/{file.name}')
    #     # print(file.name)
    #     # img = img.save(path)

        
    #     return HttpResponse('Teste')
    # else:
    dados = {}
    dados['tabela'] = Post.objects.all().values()
    return render(request, 'index.html', dados)
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        file = request.FILES.get('file')
        
        if nome == '' or senha == '':
            messages.info(request, "Senha ou nome não podem passar em braco")
            dados = {}
            dados['n'] = nome
            dados['s'] = senha
            return render(request,'cadastro.html', dados)
        
        for i in User.objects.all().values():
            if i['user'].lower() == nome.lower():
                messages.info(request, "Usuário já existente")
                dados = {}
                dados['n'] = nome
                dados['s'] = senha
                return render(request,'cadastro.html',dados)

        try:
            i = Image.open(file)
            s = os.listdir(f'{os.getcwd()}/media')
            for arquivos in s:
                abrir = Image.open(f'{os.getcwd()}/media/{arquivos}')
                if abrir.tobytes("xbm", "rgb") == i.tobytes("xbm", "rgb") and arquivos != 'anonimo.png':
                    u = User(user=nome,senha=senha,imagem=arquivos)
                    u.save()
                    user2.clear()
                    user2.append(nome)
                    return redirect(home)
            t = User(user=nome,senha=senha,imagem=file)
            t.save()
            user2.clear()
            user2.append(nome)
            return redirect(home)
        except:
            t = User(user=nome,senha=senha)
            t.save()
            user2.clear()
            user2.append(nome)
            return redirect(home)
        
    else:
        return render(request,'cadastro.html')
def login(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        for i in User.objects.all().values():
            if i['user'].lower() == nome.lower() and i['senha'] == senha:
                user2.clear()
                user2.append(i['user'])
                return redirect(home)
            

        messages.info(request, "Algo de errado não está certo")
        return render(request,'login.html')
    else:
         return render(request,'login.html')

def postar(request):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    
    if request.method == 'POST':
        post = request.POST.get('post')
        
            
        if post == '':
            messages.info(request, "A postagem não pode ter texto em branco")
            return render(request,'postar.html')
        else:
            if len(post) > 140 :
               messages.info(request, "A postagem não pode ter mais do que 140 caracteres")
               return render(request,'postar.html')
            else:
                img = []
                for i in User.objects.filter(user=user2[0]).values():
                    if i['imagem'] != '':
                        img.append(i['imagem'])
                    
                    else:
                        img.append('anonimo.png')
                
                
                p = Post(user=user2[0],post=post,data=definir_data(),imagem=img[0])
                p.save()
                return redirect(home)

    else:
        dados = {}
        dados['tabela'] = Post.objects.all().values()
        return render(request,'postar.html',dados)

def deletar(request,id):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    
    p = Post.objects.filter(id=id).values()
    for i in p:
        if i['user'].lower() != user2[0].lower():
            messages.info(request, "Você não tem autorização para apagar este post")
            return redirect(home)
        
    if request.method == 'POST':
        s = request.POST.get('sim')
        n = request.POST.get('nao')
        if s == 'on' and n == None:
            t = Post.objects.get(id=id)
            t.delete()
            return redirect(home)
        elif n == 'on' and s == None:
            return redirect(home)
        else:
            messages.info(request, "Marque uma dasopções")
            return render(request,'deletar.html')
    else:
        dados = {}
        dados['tabela'] = Post.objects.all().values()
        return render(request,'deletar.html',dados)
    
def atualizar(request,id):
    if len(user2) == 0 or user2[0] == '':
        return render(request,'login.html')
    
    x = Post.objects.filter(id=id).values()
    for i in x:
        if i['user'].lower() != user2[0].lower():
            messages.info(request, "Você não tem autorização para editar este post")
            return redirect(home)
        
    if request.method == 'POST':
        a = request.POST.get('atualizacao')
        if a == '':
            messages.info(request, "A postagem não pode ter texto em branco")
            return render(request,'atualizar.html')
        else:
            if len(a) > 140 :
               messages.info(request, "A postagem não pode ter mais do que 140 caracteres")
               return render(request,'atualizar.html')
            else:
                p = Post.objects.get(id=id)
                p.post = a
                p.data = definir_data()
                p.save()
                return redirect(home)
    else:
        dados = {}
        dados['tabela'] = Post.objects.all().values()
        return render(request,'atualizar.html',dados)

def mudar_imagem(request):
    def mudar_imagem_dos_posts(x):
        if x != '':
            po = Post.objects.filter(user=user2[0])
            for v in po:
                v.imagem = x
                v.save()
        elif x == '':
            po = Post.objects.filter(user=user2[0])
            for v in po:
                v.imagem = 'anonimo.png'
                v.save()
        return
    if request.method == 'POST':
        f = request.FILES.get('file')
        per = request.POST.get('img')
        u = User.objects.get(user=user2[0])
        if per == 'on':
            u.imagem = ''
            u.save()
            mudar_imagem_dos_posts(u.imagem)
            return redirect(home)
        else:
            if f == '':
                return redirect(home)
            else:
                i = Image.open(f)
                try:
                 d = Image.open(u.imagem, mode='r')
                except:
                    d = Image.open(f'{os.getcwd()}/media/anonimo.png')
                #Retornar imagem como um objeto de bytes
                if i.tobytes("xbm", "rgb") == d.tobytes("xbm", "rgb"):
                    i.close()
                    d.close()
                    excluir_imagem()
                    return redirect(home)
                else:
                    s = os.listdir(f'{os.getcwd()}/media')
                    for arquivos in s:
                        abrir = Image.open(f'{os.getcwd()}/media/{arquivos}')
                        if abrir.tobytes("xbm", "rgb") == i.tobytes("xbm", "rgb") and arquivos != 'anonimo.png':
                            u.imagem = arquivos
                            u.save()
                            mudar_imagem_dos_posts(u.imagem)
                            abrir.close()
                            i.close()
                            d.close()
                            excluir_imagem()
                            return redirect(home)
                        abrir.close()
                    #s = os.remove(f'{os.getcwd()}/media/{u.imagem}')
                    u.imagem = f
                    u.save()
                    mudar_imagem_dos_posts(u.imagem)
                    i.close()
                    d.close()
                    excluir_imagem()
                    return redirect(home)
                #u.save()
                

    else:
        return render(request, 'mudar_imagem.html')
    
def sair(request):
    user2.clear()
    print('sair')
    return redirect(login)