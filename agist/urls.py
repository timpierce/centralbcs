from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^import_children/$', views.import_children),
    url(r'^process_birthdays/$', views.process_birthdays),
]
