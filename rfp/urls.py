from django.conf.urls import url
from django.contrib import admin
from rfp import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_jwt.views import refresh_jwt_token

urlpatterns = [
        url(r'^rfp/(?P<sort>[-\w.,]+)/(?P<order>[-\w.].+?)/(?P<items>[-\w.,/_\-].+?)$', views.rfp),
        # url(r'^rfpdata/', views.singlerfp),
        url(r'^rfpdata/(?P<slug>[\w-]+)/$', views.singlerfp),
        url(r'^unsub_rfpdata/(?P<pk>[0-9]+)$', views.unsub_singlerfp),

        url(r'^category' , views.category),
        url(r'^allcategory', views.allcategory),
        url(r'^state' , views.states),
        url(r'^allstate' , views.allstates),

        url('allagency', views.allagencies),
        url('allcities/(?P<query>[-\w.,/_\-].+?)', views.allcities),

        url('totalrfp/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$',views.searchRfp_total),

        url(r'^city/(?P<query>[-\w.,/_\-].+?)', views.getCity),
        url(r'^std/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.stateData),
        url(r'^agency/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.agencyData),
        url(r'^citydata/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.cityData),
        url(r'^unsub_std/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.unsubstateData),
        url(r'^cat/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.categoryData),

        url(r'^search_state/(?P<query>[-\w.,/_\-].+?)/$', views.searchState),
        url(r'^search_title/(?P<query>[-\w.,/_\-].+?)/$', views.searchTitle),
        # url(r'^search_id/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.searchRfp),
        url(r'^search_id/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.searchRfp_raw),
        url(r'^search_with_sort/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)/(?P<search>[-\w.,/_\-].+?)/(?P<order>[-\w.,/_\-].+?)$', views.searchRfp_withsorting),
        url(r'^search_key/(?P<query>[-\w.,/_\-].+?)/(?P<items>[-\w.,/_\-].+?)$', views.searchKeyword_raw),
        url(r'^latest/(?P<items>[-\w.,/_\-].+?)$', views.latestRfp),
        url(r'^search_category/(?P<query>[-\w.,/_\-].+?)/$', views.searchCategory),
        url('filters/(?P<totalResult>[0-9]+)/$', views.filters),
        url(r'^contacts', views.vendorsContacts),
        url(r'^message', views.Contacts),
        url(r'^download_file/(?P<filename>[-\w.,/_\-].+?)/$', views.downloadFiles),

        url(r'^watchlist/$', views.UserWatchList),
        url(r'^Delete_all_watch_list/$', views.Delete_all_watch_list),
        url(r'^watchlistdelete/(?P<rfpId>[0-9]+)$', views.WatchlistDelete),

        url(r'^dateupdate/$',views.dateupdate),
        url(r'^getpreferencened/$',views.getpreferencened),
        url(r'^test/(?P<items>[-\w.,/_\-].+?)$',views.test),
        # url(r'^(?P<query>[-\w.].+?)/(?P<sort_by>[-\w.,]+)/$', views.influencer_list, name='influencer_list'),
]
