from django.conf.urls import url
from . import views
urlpatterns = [
    #login START
    url(r'^$', views.index),
    url(r'^home$', views.home),
    url(r'^login$', views.login),
    url(r'^create$', views.create),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
    #login END

    url(r'^add$', views.add),
    # url(r'^process', views.process),
    url(r'^create_trip', views.create_trip),

    url(r'^join/(?P<trip_id>\d+)$',views.join),
    url(r'^destination/(?P<trip_id>\d+)$',views.destination),
    #please jeebus be right

]