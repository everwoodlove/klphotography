from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^pricing/$', views.pricing, name='pricing'),
    url(r'^gallery/(?P<category>\w+)/$', views.gallery, name='gallery'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about-me/$', views.about, name='aboutme')
]