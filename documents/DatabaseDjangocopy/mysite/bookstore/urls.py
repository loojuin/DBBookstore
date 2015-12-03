from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.all_books, name='index'),

    url(r'^(?P<book_id>(?:-?\d)+)/$', views.book, name='book'),
    url(r'^(?P<book_id>(?:-?\d)+)/add_comment$', views.add_comment, name='add_comment'),
    url(r'^(?P<book_id>(?:-?\d)+)/(?P<username>([A-Za-z]+))/rating$', views.rate_comment, name='rate_comment'),
    url(r'login', views.view_login, name='login'),
    url(r'logout', views.view_logout, name='logout'),
    url(r'register', views.register, name='register'),
    url(r'stats', views.show_statistics, name='stats'),
    url(r'^(?P<book_id>(?:-?\d)+)/usefulness', views.book, name='useful_feedbacks'),
    url(r'^user/(?P<user_name>([A-Z]|[a-z])\w+)/$', views.user_record, name='profile'),
    url(r'mycart', views.view_cart, name='shopping_cart'),
    url(r'myorders', views.view_orders, name='order_history'),
    url(r'^(?P<book_id>(?:-?\d)+)/add_to_cart$', views.add_book, name='add_book_to_cart'),
    url(r'^(?P<book_id>(?:-?\d)+)/remove_from_cart$', views.remove_book, name='remove_book_from_cart'),
]
