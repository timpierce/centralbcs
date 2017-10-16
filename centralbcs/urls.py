from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='Index'),
    url(r'^f2fsignup/', include('f2fsignup.urls')),
    url(r'^faithpath/', include('faithpath.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
