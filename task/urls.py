#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.


from django.conf.urls import patterns, include, url

from views import webhook_view

urlpatterns = patterns('',
    url(r'^webhook/(?P<id>\d+)', webhook_view),
)

