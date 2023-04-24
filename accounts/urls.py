
from django.urls import path
from .views import home, signup

urlpatterns = [
    path('', home, name='home'),
    path('signup/<str:role>/', signup, name='signup')
]
