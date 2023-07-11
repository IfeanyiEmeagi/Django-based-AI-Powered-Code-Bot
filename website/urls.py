from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
    path('suggest/', views.suggest, name='suggest'),
     path('login/', views.login_user, name='login'),
      path('logout/', views.logout_user, name='logout'),
       path('register/', views.register_user, name='register'),
       path('code_history/', views.code_history, name='code_history'),
       path('delete_history/<history_id>', views.delete_history, name='delete_history'),
]