from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('img_plot',views.img_plot,name='img_plot'),
    path('regist', views.regist, name='regist'),
]
