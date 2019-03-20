"""GestaoDePraticasDiarias_v6 URL Configuration

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

urlpatterns = [
    path('verbs/', views.ListVerb.as_view(), name='verb_list'),
    path('verb/<int:pk>', views.DetailVerb.as_view(), name='verb_detail'),
    path('create_verb/', views.CreateVerb.as_view(), name='verb_create'),
    path('update_verb<int:pk>/',
         views.UpdateVerb.as_view(),
         name='verb_update'),
    path('delete_verb<int:pk>/',
         views.DeleteVerb.as_view(),
         name='verb_delete'),

    path('sentences/', views.ListSentence.as_view(), name='sentence_list'),
    path('sentence/<int:pk>', views.DetailSentence.as_view(),
         name='sentence_detail'),
    path('create_sentence/', views.CreateSentence.as_view(),
         name='sentence_create'),
    path('update_sentence<int:pk>/',
         views.UpdateSentence.as_view(),
         name='sentence_update'),
    path('delete_sentence<int:pk>/',
         views.DeleteSentence.as_view(),
         name='sentence_delete'),

    path('groups/', views.ListGroup.as_view(), name='group_list'),
    path('group/<int:pk>', views.DetailGroup.as_view(),
         name='group_detail'),
    path('create_group/', views.CreateGroup.as_view(),
         name='group_create'),
    path('update_group<int:pk>/',
         views.UpdateGroup.as_view(),
         name='group_update'),
    path('delete_group<int:pk>/',
         views.DeleteGroup.as_view(),
         name='group_delete'),

    path('patterns/', views.ListPattern.as_view(), name='pattern_list'),
    path('pattern/<int:pk>', views.DetailPattern.as_view(),
         name='pattern_detail'),
    path('create_pattern/', views.CreatePattern.as_view(),
         name='pattern_create'),
    path('update_pattern<int:pk>/',
         views.UpdatePattern.as_view(),
         name='pattern_update'),
    path('delete_pattern<int:pk>/',
         views.DeletePattern.as_view(),
         name='pattern_delete'),

]
