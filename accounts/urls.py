
from django.urls import path
from .views import home, signup, signin, dashboard

urlpatterns = [
    path('', home, name='home'),
    path('signup/<str:role>/', signup, name='signup'),
    path('signin/<str:role>/', signin, name='signin'),
    path('dashboard/<str:role>/', dashboard, name='dashboard')
]
