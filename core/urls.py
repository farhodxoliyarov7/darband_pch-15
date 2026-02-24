from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import login_view, register_view, home_view, profile_update_view # Tahrirlash funksiyasini qo'shdik

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Kirish sahifasi
    path('', login_view, name='login'), 

    # Ro'yxatdan o'tish
    path('register/', register_view, name='register'), 

    # Dashboard sahifasi
    path('home/', home_view, name='home'), 

    # Profilni tahrirlash (POST so'rovlar uchun)
    path('profile/update/', profile_update_view, name='profile_update'),

    # Tizimdan chiqish
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]