from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # API routes
    path('api/yourmodel/', views.YourModelView.as_view(), name='yourmodel-api'),

    # หน้า HTML
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('location/', views.location, name='location'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.login, name='login'),
    path('signup/', views.signUp, name='signup'),
    path('forgotpassword/', views.forgot_password, name='forgot_password'),
    path('status/', views.get_status, name='status'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
