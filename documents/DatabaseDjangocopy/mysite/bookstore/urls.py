from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.all_books, name='index'),
    url(r'^(?P<book_id>(?:-?\d)+)/$', views.book, name='book'),
    url(r'^(?P<book_id>(?:-?\d)+)/add_comment$', views.add_comment, name='add_comment'),
    url(r'login', views.login, name='login'),
    url(r'register', views.register, name='register'),
]
