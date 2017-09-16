from django.conf.urls import include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^', include('f2fsignup.urls')),
    url(r'^agist/', include('agist.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
