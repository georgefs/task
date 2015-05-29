#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 vagrant 
#
# Distributed under terms of the MIT license.

from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
import logging
import json
from machine import core as machine_core
from task import utils as task_utils
from task import models as task_models


class Command(NoArgsCommand):
    def handle(self, *args, **kwargs):
        task_models.Job.scan()

