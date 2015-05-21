#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings")

from task.models import *
from machine import core


job = Task.objects.get(pk=1).create_job(123)
job.start()


