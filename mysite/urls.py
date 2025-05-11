"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from api import views

urlpatterns = [
    path('', include("api.urls")),  # รวม API URLs
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    
    # API rest framework URLs
        # ListAPIView - แสดงผล Task ทั้งหมด
        # CreateAPIView - สร้าง Task ใหม่
        # RetrieveAPIView - แสดงผล Task นั้น ๆ
        # UpdateAPIView - อัพเดต Task นั้น ๆ
        # DeleteAPIView - ลบ Task นั้น ๆ
    path('api/tasks/', views.BoatListCreate.as_view()),
    path('api/tasks/<int:pk>', views.BoatDetailUpdateDelete.as_view()),
    path('api/boatstatus/', views.YourModelView.as_view(), name='yourmodel-api'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
