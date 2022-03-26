from django.urls import path
from pwdapp.views import Inicio, login, register, protected_view, logout

urlpatterns = [
    path('', Inicio, name="login"), #El name se le coloca para luego navegar entre path dentro de los HTMLs
    path('login/', login),
    path('register/', register, name="register"),
    path('dashboard/', protected_view, name="protected"),
    path('logout/', logout, name="logout"),
]