import django
from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False)
    location = models.CharField(max_length=200, blank=False)
    def __str__(self):
        return self.name



class User(AbstractUser):
    id = models.AutoField(db_column='ID',primary_key=True)
    username = models.CharField(db_column='UserName',
                                max_length=255,
                                unique=True)
    useremail = models.CharField(db_column='UserEmail',
                                 max_length=255)
    password = models.CharField(db_column='Password',
                                max_length=255,
                                blank=True, null=True)

    organization = models.ForeignKey(Organization, null=True,blank=True, on_delete=models.SET_NULL)




    class Meta:
        managed = True
        db_table = 'User'
        permissions = (
            ("test_GProc", "Teste de permissao geral Gestor de Processos"),
            ("test_Analist", "Teste de permissao geral Analista"),
            ("test_Func", "Teste de permissao geral Funcionário"),
            ("test_Admin", "Teste de permissao geral Administrador"),)

