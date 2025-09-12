from django.urls import path
from .views import HomeView
from . import views

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chatbot-reply/', views.chatbot_reply, name='chatbot-reply'),
 
         # Activation link
    path('activate/<uidb64>/<token>/', views.activate_view, name='activate'),
]