from django.urls import path
from .views import *

urlpatterns = [
    path('', Main.as_view()),
    path('profile/', Profile.as_view()),
    path('calculator/', Calculator.as_view()),
    path('search/', Search.as_view()),
]
