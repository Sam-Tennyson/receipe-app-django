from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import *
from django.contrib.auth import authenticate

class LoginSerializer(serializers.ModelSerializer):
    
    email = serializers.CharField()
    password = serializers.CharField()

    class Meta:

        model = User
        fields = ['email', 'password']

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        if (email and password) :
            user = authenticate(email=email, password=password)
            print(user, ">>")
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError({"message": msg})
            # else:
            #     msg = 'Invalid login credientials'
            #     raise serializers.ValidationError({"message": msg})
        return attrs

class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required= True,
        validators = [UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:

        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(
                username=self.validated_data['username'],
                first_name=self.validated_data['first_name'],
                last_name=self.validated_data['last_name'],
                email=self.validated_data['email'],
                password=self.validated_data['password']
            )
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class RecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = "__all__"

    # def validate(self, data):

    #     if (data["angryLevel"] < 2):
    #         raise serializers.ValidationError({"validation error": "AngryLevel must be greater than 1"})
    #     return data
    
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"

    # def validate(self, data):

    #     if (data["angryLevel"] < 2):
    #         raise serializers.ValidationError({"validation error": "AngryLevel must be greater than 1"})
    #     return data