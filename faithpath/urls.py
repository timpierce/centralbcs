from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^addchild$', views.addchild, name='addchild'),
]
