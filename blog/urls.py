from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('article/<int:article_id>/', views.article_detail, name='detail'),
    path('edit/<int:article_id>/', views.article_edit, name='edit'),
    path('edit/<int:article_id>/submit/', views.article_submit, name='submit'),
    path('edit/<int:article_id>/delete/', views.article_delete, name='delete')
]