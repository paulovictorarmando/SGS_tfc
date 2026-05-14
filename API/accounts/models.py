from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    username = models.CharField(blank=False, null=False, unique=True, db_index=True)
    email = models.EmailField(blank=False, unique=True, db_index=True)
    telefone = models.CharField(max_length=15, unique=True, blank=True, db_index=True)
    class Meta:
        ordering = ['-id']
