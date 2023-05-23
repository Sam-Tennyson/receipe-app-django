from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .models import *

# Create your views here.
class RecipeView(APIView):
    authenticateion_classes =  [JWTAuthentication]
    permission_classes =  [IsAuthenticated]

    def post(self, request):
        data = request.data
        print(data)
        serializer = RecipeSerializer(data= request.data)
        
        if (not serializer.is_valid()):
            return Response({
                "status": status.HTTP_403_FORBIDDEN, 
                "errors": serializer.errors
            })

        return Response({
            "status": status.HTTP_200_OK,
            "data": serializer.data,
        })

    def get(self, request, *args, **kwargs):
        queryset_data = Recipe.objects.all()
        
        paginator = Paginator(queryset_data, 10) # 10 objects per page
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        serialized_data = RecipeSerializer(queryset_data, many=True)
        
        return Response({
            "status": status.HTTP_200_OK ,
            "data": serialized_data.data
        })

class LoginAPIView(APIView):

    def post(self, request):
        email = request.POST.get('enauk')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # Generate or retrieve the token
            serializer = LoginSerializer(data= request.data)
            newUser =  User.objects.get(email= serializer.data['email'])
            refresh = RefreshToken.for_user(user=newUser)

            return Response({
                "status": status.HTTP_200_OK,
                "data": serializer.data,
                "message": "Logged in successfully", 
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })  
            # token, created = Token.objects.get_or_create(user=user)
            # return Response({'token': token.key})
        else:
            return Response({'msg':'Invalid credentials', "status":401})

        # try:   
        #     print("---------------------...................")
        #     data = request.data
        #     print(data)
        #     serializer = LoginSerializer(data= request.data)
        #     if (not serializer.is_valid()):
        #         return Response({
        #             "status": status.HTTP_403_FORBIDDEN, 
        #             "errors": serializer.errors
        #         })
            
        
        #     newUser =  User.objects.get(email= serializer.data['email'])
        #     refresh = RefreshToken.for_user(user=newUser)

        #     # return Response({
        #     #     "status": status.HTTP_200_OK,
        #     #     "data": serializer.data,
        #     #     "message": "Logged in successfully", 
        #     #     'refresh': str(refresh),
        #     #     'access': str(refresh.access_token),
        #     # })  
        # except ConnectionError as e:
        #     # Handle connection error
        #     return Response({'message': 'Connection error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  
        # except Exception as e:
        #     # Handle other exceptions
        #     return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def get(self):
        return Response({'message': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RegisterAPIView(APIView):
    
    def get(self, request, *args, **kwargs):
        queryset_data = User.objects.all()
        
        paginator = Paginator(queryset_data, 10) # 10 objects per page
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        serialized_data = RegisterSerializer(queryset_data, many=True)
        
        return Response({
            "status": status.HTTP_200_OK ,
            "data": serialized_data,
            "count": paginator.count,
        })

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = RegisterSerializer(data= request.data)
        
        if (not serializer.is_valid()):
            return Response({
                "status": status.HTTP_403_FORBIDDEN, 
                "errors": serializer.errors
            })
        
        serializer.save()

        newUser = User.objects.get(username= serializer.data['username'])
        refresh = RefreshToken.for_user(user=newUser)

        return Response({
            "status": status.HTTP_201_CREATED,
            "data": serializer.data,
            "message": "Added", 
            "data": data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })    
