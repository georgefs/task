#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.


from django.contrib import admin
from .models import Task, Job, Project, TaskTrigger

class JobAdmin(admin.ModelAdmin):
    readonly_fields  = ["name", "requires", "log", "output", "environment", "status", "machine", "container_id","script", "task" ]
    list_display = ["name", "requires", "status", "machine", "container_id"]

    def requires(self, instance, *args, **kwargs):
        requires = self.requires.replace("\n", "")
        return requires

admin.site.register(TaskTrigger)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Job, JobAdmin)
