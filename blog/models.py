# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    autor = models.ForeignKey('auth.User')
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    data_criacao = models.DateTimeField(default=timezone.now)
    data_publicacao = models.DateTimeField(blank=True, null=True)
    visualizacoes = models.IntegerField(default=0)

    def publish(self):
        self.data_publicacao = timezone.now()
        self.save()

    def __str__(self):
        return self.titulo.encode('utf-8')


class Comentario(models.Model):
    autor = models.ForeignKey('auth.User')
    post = models.ForeignKey(Post)
    data = models.DateTimeField(default=timezone.now)
    texto = models.TextField()

    def __str__(self):
        return (str(self.post.id) + " " + str(self.autor.username) + " " + str(self.data))