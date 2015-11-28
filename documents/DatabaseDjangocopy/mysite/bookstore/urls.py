from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.all_books, name='index'),
    url(r'^(?P<book_id>(?:-?\d)+)/$', views.book, name='book'),
    url(r'login', views.login, name='login'),
]
