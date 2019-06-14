from django.conf.urls import url
from django.contrib import admin
from blog import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url(r'^bloglist', views.bloglist),
    url(r'^becomePartner/', views.becomePartner),
    url(r'^singleblog/(?P<bid>[0-9]+)$', views.singleblog),
    url(r'^user_notifications/$', views.first_notifications),
    url(r'^read_delete/(?P<id>[0-9]+)/$', views.read_delete),
    url(r'^delete_all_notification/', views.delete_all_notification),
]