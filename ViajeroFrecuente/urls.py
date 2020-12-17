from . import views
from django.urls import path
from django.views.generic.base import TemplateView
from ViajeroFrecuente.views import triplist

urlpatterns = [
    #path('main', TemplateView.as_view(template_name='home.html'), name='main'), # new
    path('main', views.main, name='main'),
    path('newtrip', views.newtrip, name='newtrip'),
    path('triplist', views.triplist, name='triplist'),
    path('currenttrip', views.currenttrip, name='currenttrip'),
    path('tripdetail/<id>/', views.tripdetail, name='tripdetail'),
    path('tripjoin/<id>/', views.tripjoin, name='tripjoin'),
    path('tripclose/<id>/', views.tripclose, name='tripclose'),
    path('qualification/<id>/', views.qualification, name='qualification'),
    path('setqualification', views.setqualification, name='setqualification'),
    path('newvehicle', views.newvehicle, name='newvehicle'),
    path('signup', views.signup, name='signup'),
    #url(r'^tripdetail/(?P<id>\d+)/$', views.tripdetail, name='tripdetail'),
    #path('triplist', triplist.as_view()),
]