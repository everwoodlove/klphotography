from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^pricing/$', views.pricing, name='pricing'),
    url(r'^gallery/(?P<category>\w+)/$', views.gallery, name='gallery'),
    url(r'^gallery/(?P<category>(.*?))/(?P<date>(.*?))/(?P<name>(.*?))/$', views.shoot, name='shoot'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about-me/$', views.about, name='aboutme')
]

# Want self-generated URLS:
# Standard gallery ones
# Then each shoot has one -- Url looks like:
# /category/date/shoot-name

# For performance probably want to load smaller versions and then allow people to click to pop into fullscreen
#Maybe blocks of 3/4 instead of 1/2?