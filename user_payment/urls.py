from django.conf.urls import url
from user_payment import  views
urlpatterns = [
    url(r'^history/(?P<username>[-\w.,/_\-].+?)/$',views.Purchase),
    url(r'^cardinfo/$',views.cardInfo),
    url(r'^cardnoexist/$',views.cardno),
    url(r'^cardinfodelete/(?P<id>[0-9]+)$', views.cardInfoDelete),
]
