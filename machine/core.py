#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.

from gmachine import machine
from . import models
import random

def get_machine(machine_filter, mem_limit, cpuset):
    machine_status = scan_machine()
    activity_machines = machine_status['activity_machines']
    return random.choice(activity_machines)


def scan_machine():
    machines = models.Machine.objects.all()
    activity_machines = []
    change_machine = []

    for _machine in machines:
        ori_machine_status = _machine.status
        try:
            _machine.info()
            _machine.status = 'running'
            activity_machines.append(_machine)
        except Exception as e:
            print e
            _machine.status = 'stop'
            
        if ori_machine_status != _machine.status:
            change_machine.append(_machine)

    for _machine in change_machine:
        _machine.save()

    return {"activity_machines": activity_machines, "change_machine": change_machine}


def create_machine(machine_name):
    try:
        return models.Machine.objects.get(name=machine_name)
    except models.Machine.DoesNotExist as e:
        pass

    try:
        settings = machine.info(machine_name)
    except SystemExit  as e:
        machine.create(machine_name)
        settings = machine.info(machine_name)

    new_machine = models.Machine(name=machine_name, settings=settings)
    new_machine.save()
    return new_machine
