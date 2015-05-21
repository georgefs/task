#!/usr/bin/env python
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings")

from task.models import *
from machine import core

jobs = Job.objects.exclude(status="success")
for job in jobs:
    job.load_status()


