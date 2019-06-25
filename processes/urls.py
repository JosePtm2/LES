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

app_name = "processes"

urlpatterns = [
    path("processos", views.processos, name="processos"),
    path("processos/ProcessCreate", login_required(views.ProcessCreate.as_view(success_url=('/processos')),login_url="/login"), name="ProcessCreate"),
    path("processos/ProcessUpdate/<int:pk>", login_required(views.ProcessUpdate.as_view(success_url=('/processos')),login_url="/login"), name="ProcessUpdate"),
    path("processos/ProcessDelete/<int:pk>", login_required(views.ProcessDelete.as_view(success_url=('/processos')),login_url="/login"), name="ProcessDelete"),
    path("processos/ProcessDetail/<int:pk>", login_required(views.ProcessDetail.as_view(),login_url="/login"), name="ProcessDetail"),
    path("actividades", views.actividades, name="actividades"),
    path("actividades/ActivityCreate", login_required(views.ActivityCreate.as_view(success_url=('/actividades')),login_url="/login"), name="ActivityCreate"),
    path("actividades/ActivityDetail/<int:pk>", login_required(views.ActivityDetail.as_view(), login_url="/login"), name="ActivityDetail"),
    path("actividades/ActivityUpdate/<int:pk>", login_required(views.ActivityUpdate.as_view(success_url=('/actividades')),login_url="/login") , name="ActivityUpdate"),
    path("actividades/ActivityDelete/<int:pk>", login_required(views.ActivityDelete.as_view(success_url=('/actividades')),login_url="/login"), name="ActivityDelete"),
    path("actividades/ActivitySwap/<int:pk>/<int:fk>", login_required(views.ActivitySwap.as_view(success_url=('/actividades/AssociateReferer')),login_url="/login"), name="ActivitySwap"),
    path("actividades/AssociateReferer", views.AssociateReferer, name="AssociateReferer"),
    path("actividades/ActivityDessociate/<int:pk>", views.removeActivityFromProcess, name="ActivityDessociate"),
    path("actividades/PatternDessociate/<int:pk>/<int:fk>", views.removePatternFromActivity, name="PatternDessociate"),
    path("actividades/PatternAssociate/<int:pk>/<int:fk>", views.addPatternToActivity, name="PatternAssociate"),
    path("produtos", views.produtos, name="produtos"),
    path("produtos/ProductCreate", login_required(views.ProductCreate.as_view(success_url=('/produtos')),login_url="/login"), name="ProductCreate"),
    path("produtos/ProductDetail/<int:pk>", login_required(views.ProductDetail.as_view(),login_url="/login"), name="ProductDetail"),
    path("produtos/ProductUpdate/<int:pk>", login_required(views.ProductUpdate.as_view(success_url=('/produtos')),login_url="/login"), name="ProductUpdate"),
    path("produtos/ProductDelete/<int:pk>", login_required(views.ProductDelete.as_view(success_url=('/produtos')),login_url="/login"), name="ProductDelete"),
    path("produtos/ProductDessociate/<int:pk>/<int:fk>", views.removeActivityFromProduct, name="ProductDessociate"),
    path("produtos/ProductAssociate/<int:pk>/<int:fk>", views.addActivityToProduct, name="ProductAssociate"),
    path("papeis", views.papeis, name="papeis"),
    path("papeis/RoleCreate", login_required(views.RoleCreate.as_view(success_url=('/papeis')),login_url="/login"), name="RoleCreate"),
    path("papeis/RoleDetail/<int:pk>", login_required(views.RoleDetail.as_view(),login_url="/login"), name="RoleDetail"),
    path("papeis/RoleUpdate/<int:pk>", login_required(views.RoleUpdate.as_view(success_url=('/papeis')),login_url="/login"), name="RoleUpdate"),
    path("papeis/RoleDelete/<int:pk>", login_required(views.RoleDelete.as_view(success_url=('/papeis')),login_url="/login"), name="RoleDelete"),
    path("actividades/RoleDessociate/<int:pk>/<int:fk>", views.removeRoleFromActivity, name="RoleDessociate"),
    path("actividades/RoleAssociate/<int:pk>/<int:fk>", views.addRoleToActivity, name="RoleAssociate"),
    path('actividades/SeeProcess/<int:pk>/', views.ViewProcess.as_view(), name='ViewProcess'),
    path('actividades/SeePattern/<int:pk>/', views.ViewPattern.as_view(), name='ViewPattern'),
    path('actividades/SeeProduct/<int:pk>/', views.ViewProduct.as_view(), name='ViewProduct'),
    path('actividades/SeeRole/<int:pk>/', views.ViewRole.as_view(), name='ViewRole'),
    path('actividades/SeeActivity/<int:pk>/', views.ViewActivity.as_view(), name='ViewActivity'),
]

