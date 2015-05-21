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


class Command(NoArgsCommand):
    def handle(self, machine_name, *args, **kwargs):
        machine_core.create_machine(machine_name)
