from django.urls import path
from users.views import CustomLoginView, CustomRegistrationView, ProfileView
from django.contrib.auth import views as auth_views 

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegistrationView.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]