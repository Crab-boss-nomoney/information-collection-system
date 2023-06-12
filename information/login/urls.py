from django.urls import path, include
from login import views

urlpatterns = [
    path('', views.welcome, name='welcome'), # 欢迎页
    path('login/', views.login, name="login"),
    path('login_out/', views.login_out, name="login_out"),
    path('register/', views.register, name="register"),
    path('password-reset/', include('password_reset.urls'), name='password_reset'),
]