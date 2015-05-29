#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings")

from task.models import *
from machine import core


job = Task.objects.get(name="Children").create_job(value=0)
job.start()


