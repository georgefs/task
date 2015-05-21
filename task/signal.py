#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2015 vagrant 
#
# Distributed under terms of the MIT license.
import django.dispatch

job_prestart = django.dispatch.Signal(providing_args=["instance"])
job_poststart = django.dispatch.Signal(providing_args=["instance"])

job_success = django.dispatch.Signal(providing_args=["instance"])
job_end = django.dispatch.Signal(providing_args=["instance"])
job_fault = django.dispatch.Signal(providing_args=["instance"])


job_create = django.dispatch.Signal(providing_args=["instance"])
