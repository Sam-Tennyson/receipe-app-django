from django.urls import path
from .views import *

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view()),
    path('auth/login/', LoginAPIView.as_view()),
    path('recipe/app/', RecipeView.as_view()),
]
