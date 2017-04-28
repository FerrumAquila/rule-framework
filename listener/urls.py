# App Imports
import views

# Django Imports
from django.conf.urls import url


urlpatterns = [
    # App APIs
    url(r'^$', views.listener, name='listener'),
]
