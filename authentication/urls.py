from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^get_last_login/', views.get_last_login, name='get_last_login'),
    url(r'^log_out_from_all_apps/', views.log_out_from_all_apps, name='log_out_from_all_apps'),
]