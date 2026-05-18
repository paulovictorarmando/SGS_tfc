from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    telefone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    class Meta:
        ordering = ['-id']
