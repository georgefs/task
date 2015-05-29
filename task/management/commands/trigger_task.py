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


class Command(NoArgsCommand):
    def handle(self, task_id, **data):
        task_utils.trigger_task(task_id, data)
