#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#

from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
    url(r'^partidos/$', views.match_list, name='match_list'),
    url(r'^partidos/(?P<tournament_id>\w+)$', views.match_list, name='match_list'),
    url(r'^horario/$', views.timetable, name='timetable'),
    url(r'^(?P<tournament>\w+)/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
)
