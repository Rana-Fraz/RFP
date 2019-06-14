from django.conf.urls import url
from django.contrib import admin
from category import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
    url('catget', views.catget),

]