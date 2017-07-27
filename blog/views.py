# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import Post, Comentario
from django.utils import timezone
from .forms import formComentario, formPost
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def post_list(request):
    if request.user.id is None:
        return redirect(logar)

    posts_publicados = Post.objects.filter(data_publicacao__lte=timezone.now()).order_by('data_publicacao')
    return render(request, 'post_list.html', {'posts': posts_publicados})

def post_detail(request, pk):
    if request.user.id is None:
        return redirect(logar)

    if request.method == "POST":
        form =  formComentario(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.data = timezone.now()
            comentario.post = Post.objects.get(id=pk)
            comentario.save()
            return redirect(post_detail, pk=pk)
    else:
        post = Post.objects.get(id=pk)
        post.visualizacoes = post.visualizacoes + 1
        post.save()
        comentarios = Comentario.objects.filter(post=post).order_by('data')
        form = formComentario()


    return render(request, 'post_detail.html', {'post': post, 'comentarios': comentarios, 'form': form})

def post_new(request):
    if request.user.id is None:
        return redirect(logar)

    if request.method == "POST":
        form =  formPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.data_criacao = timezone.now()
            post.save()
            form = formPost()
            return render(request, 'post_new.html', {'form': form})

    else:
        form = formPost()
        return render(request, 'post_new.html', {'form': form})

def logar(request):

    if request.user.id is not None:
        return redirect(post_list)

    if request.method == "POST":
        username =  request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(post_list)


    return render(request, 'login.html', {})


def user_new(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(logar)
        else:
            return render(request, 'user_new.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'user_new.html', {'form': form})