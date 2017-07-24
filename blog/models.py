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
    def publish(self):
        self.data_publicacao = timezone.now()
        self.save()
    def __str__(self):
        return self.titulo.encode('utf-8')