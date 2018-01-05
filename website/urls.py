from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^gallery/(?P<category>\w+)/$', views.gallery, name='gallery'),
    url(r'^gallery/(?P<category>(.*?))/(?P<date>(.*?))/(?P<name>(.*?))/$', views.shoot, name='shoot'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about-me/$', views.about, name='aboutme')

]