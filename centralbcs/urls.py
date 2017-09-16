from django.conf.urls import include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^agist/', include('agist.urls')),
    url(r'^f2fsignup/', include('f2fsignup.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
