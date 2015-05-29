#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.
from task.models import *
from machine import core

def get_job_name(task_name, data):
    task = Task.objects.get(name=task_name)
    job = task.create_job(**data)
    return job.name



def update_job_status():
    jobs = Job.objects.exclude(status="success")
    for job in jobs:
        job.load_status()


def trigger_task(task_id, data):
    Task.objects.get(pk=task_id).create_job(data)
