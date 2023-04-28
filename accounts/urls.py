from django.urls import path
from .views import home, signup, signin, dashboard, delete, update, addPrescription

urlpatterns = [
    path("", home, name="home"),
    path("signup/<str:role>/", signup, name="signup"),
    path("signin/<str:role>/", signin, name="signin"),
    path("dashboard/<str:role>/", dashboard, name="dashboard"),
    path("delete/<str:user>/<str:pk>/<str:role>", delete, name="delete"),
    path("update/<str:user>/<str:pk>/<str:role>", update, name="update"),
    path("addPrescription/<str:pk>/", addPrescription, name="add-prescription"),
]
