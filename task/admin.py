#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.


from django.contrib import admin
from .models import Task, Job

admin.site.register(Task)
admin.site.register(Job)
