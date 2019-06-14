from django.conf.urls import url
from django.contrib import admin
from core import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
        url(r'^register/', views.register),
        url(r'^social_login/$', views.customer_social_register_login),
        url(r'^package/', views.postcr),
        url(r'^ac_login/', views.authenticated_login),
        url(r'^ac_code/', views.send_activation_code),
        url(r'^forget_password/', views.forget_password),
        url(r'^change_password/', views.change_password),
        url(r'^activate/(?P<uid>\w+)$', views.activate_account),
        url(r'^user-token-auth/', obtain_jwt_token),
        url(r'^api-token-verify/', verify_jwt_token),
        url(r'^api-token-refresh/', refresh_jwt_token),
        url(r'^pkg_sub', views.pkgsubscribe),
        url(r'^email_exist/' , views.email_exist),
        url(r'^user_name_exist/' , views.username_exist),
        url(r'^users_update/' , views.userProfile),
        url(r'^subscription/', views.sendSubscription),
        url(r'^unsubscribe/(?P<email>\w+|[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.unsubscribe),
        url(r'^unsubscribe_query/', views.unsubscribeQuery),
        url(r'^marketing/', views.sendMarketing),
        url(r'^profile_update/(?P<username>[-\w.,/_\-].+?)/$', views.Users_details_update),
        url(r'^preferance_Updates/(?P<username>[-\w.,/_\-].+?)/$', views.preferance_update),
        url(r'^user_information/(?P<usernam>[-\w.,/_\-].+?)/$' , views.user_information),
        url(r'^user_change_password/(?P<username>[-\w.,/_\-].+?)/$', views.loginchangePassword),
        url(r'^zipcode/(?P<zipcode>[0-9]+)/$', views.zip_data),
       # url(r'^allagenncies', views.allagenncies),
        url(r'^allcites', views.cites),
        url(r'^allcounty', views.county),
        # url(r'^user_notifications/$', views.first_notifications),
        # url(r'^read_delete/(?P<id>[0-9]+)/$', views.read_delete),
        # url(r'^delete_all_notification/', views.delete_all_notification),
        #url(r'^prac/', views.preventuserloginagain),
]