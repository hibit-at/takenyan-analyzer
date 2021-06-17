from django.contrib import admin
from django.urls import include  # 追加
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("app.urls")) #追加
]
