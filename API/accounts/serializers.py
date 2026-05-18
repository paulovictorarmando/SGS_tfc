from rest_framework import serializers
from accounts.models import Usuario
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=150, validators=[UniqueValidator(queryset=Usuario.objects.all())])
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    telefone = serializers.CharField(required=True, max_length=15,min_length=9, validators=[UniqueValidator(queryset=Usuario.objects.all())])
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=Usuario.objects.all())])
    is_staff = serializers.BooleanField(required=True)

    class Meta:
        model = Usuario
        fields = ("id", 'username', 'password', 'first_name', 'last_name', 'telefone', 'email', 'is_staff')

    def create(self, validated_data):
        try:
            user = Usuario.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
            )
            user.first_name = validated_data['first_name']
            user.last_name = validated_data['last_name']
            user.telefone = validated_data['telefone']
            user.is_staff = validated_data['is_staff']
            user.save()
            return user
        except IntegrityError:
            raise ValidationError({"detail": "Dados existentes."})