#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.

def get_job_name(task_name, data):
    return Task.objects.get(name=task_name).create_job().name

