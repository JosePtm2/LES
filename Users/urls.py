"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "Users"

urlpatterns = [
    path("utilizadores", views.utilizadores, name="utilizadores"),
    path("utilizadores/UserCreate", login_required(views.UserCreate.as_view(success_url=('/utilizadores')),login_url="/login"),  name="UserCreate"),
    path("utilizadores/UserDelete/<int:pk>", login_required(views.UserDelete.as_view(success_url=('/utilizadores')),login_url="/login"),  name="UserDelete"),
    path("utilizadores/UserUpdate/<int:pk>", login_required(views.UserUpdate.as_view(success_url=('/utilizadores')),login_url="/login"),  name="UserUpdate"),
    path("utilizadores/UserUpdateEmail/<int:pk>", login_required(views.UserUpdateEmail.as_view(success_url=('/')),login_url="/login"),  name="UserUpdateEmail"),
    path("utilizadores/UserChangePassword/<int:pk>", login_required(views.UserChangePassword.as_view(success_url=('/')),login_url="/login"),  name="UserUpdatePassword"),
    path("utilizadores/UserDetail/<int:pk>", login_required(views.UserDetail.as_view(),login_url="/login"), name="UserDetail"  ),
    path("empresas", views.empresas, name="empresas"),
    path("empresas/OrganizationCreate", login_required(views.OrganizationCreate.as_view(success_url=('/empresas')), login_url="/login"), name="empresas"),
    path("empresas/OrganizationDelete/<int:pk>", login_required(views.OrganizationDelete.as_view(success_url=('/empresas')),login_url="/login"),  name="OrganizationDelete"),
    path("empresas/OrganizationUpdate/<int:pk>", login_required(views.OrganizationUpdate.as_view(success_url=('/empresas')),login_url="/login"),  name="OrganizationUpdate"),
    path("empresas/OrganizationDetail/<int:pk>", login_required(views.OrganizationDetail.as_view(),login_url="/login"), name="OrganizationDetail"  ),
    path("logout", views.logout_request, name="logout"),
    path("login", views.login_request, name="login"),
]
