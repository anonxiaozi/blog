#!/usr/bin/env python
# coding=utf-8
# Author: bloke

from django.urls import path, re_path
from .views import IndexView, BlogView, UploadDataView, UploadImgView, AboutView, ContactView

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('upload/', UploadDataView.as_view(), name='upload'),
    path('img/', UploadImgView.as_view(), name='img'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    re_path(r'^(?P<blog_id>\d+)/', BlogView.as_view(), name='blog'),
    # re_path(r'^(?P<blog_id>\d+)/(?P<action>((edit)|(view)))', BlogView.as_view(), name='blog'),
    # path('view/<int:blog_id>/', ContentView.as_view(), name='content'),
    # path('edit/<int:blog_id>/', BlogView.as_view(), name='edit'),
]
