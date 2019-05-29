# coding:utf-8
__author__ = 'wgy'
__date__ = '2019-05-29 13:57'
from django.conf.urls import url
from myapp import views

urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
]