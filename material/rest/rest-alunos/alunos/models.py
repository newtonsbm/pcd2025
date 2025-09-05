from django.db import models

# Create your models here.
class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    data_matricula = models.DateField()
    registro_academico = models.CharField(max_length=100)

    def __str__(self):
        return self.nome