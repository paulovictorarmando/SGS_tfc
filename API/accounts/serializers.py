from rest_framework import serializers
from accounts.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    telefone = serializers.CharField(required=True, max_length=15,min_length=9)
    email = serializers.EmailField(required=True)
    is_staff = serializers.BooleanField(required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'password', 'first_name', 'last_name', 'telefone', 'email', 'is_staff')

    def create(self, validated_data):
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefone=validated_data['telefone'],
            email=validated_data['email'],
            is_staff=validated_data['is_staff']
        )
        return user