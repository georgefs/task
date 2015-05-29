# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Job.requires'
        db.add_column(u'task_job', 'requires',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field requires on 'Job'
        db.delete_table(db.shorten_name(u'task_job_requires'))


    def backwards(self, orm):
        # Deleting field 'Job.requires'
        db.delete_column(u'task_job', 'requires')

        # Adding M2M table for field requires on 'Job'
        m2m_table_name = db.shorten_name(u'task_job_requires')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_job', models.ForeignKey(orm[u'task.job'], null=False)),
            ('to_job', models.ForeignKey(orm[u'task.job'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_job_id', 'to_job_id'])


    models = {
        u'djcelery.crontabschedule': {
            'Meta': {'ordering': "[u'month_of_year', u'day_of_month', u'day_of_week', u'hour', u'minute']", 'object_name': 'CrontabSchedule'},
            'day_of_month': ('django.db.models.fields.CharField', [], {'default': "u'*'", 'max_length': '64'}),
            'day_of_week': ('django.db.models.fields.CharField', [], {'default': "u'*'", 'max_length': '64'}),
            'hour': ('django.db.models.fields.CharField', [], {'default': "u'*'", 'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minute': ('django.db.models.fields.CharField', [], {'default': "u'*'", 'max_length': '64'}),
            'month_of_year': ('django.db.models.fields.CharField', [], {'default': "u'*'", 'max_length': '64'})
        },
        u'djcelery.intervalschedule': {
            'Meta': {'ordering': "[u'period', u'every']", 'object_name': 'IntervalSchedule'},
            'every': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        },
        u'djcelery.periodictask': {
            'Meta': {'object_name': 'PeriodicTask'},
            'args': ('django.db.models.fields.TextField', [], {'default': "u'[]'", 'blank': 'True'}),
            'crontab': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.CrontabSchedule']", 'null': 'True', 'blank': 'True'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'exchange': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.IntervalSchedule']", 'null': 'True', 'blank': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'default': "u'{}'", 'blank': 'True'}),
            'last_run_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'queue': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'routing_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'total_run_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'machine.machine': {
            'Meta': {'object_name': 'Machine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'settings': ('picklefield.fields.PickledObjectField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'task.job': {
            'Meta': {'object_name': 'Job'},
            'container_id': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'data': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'environment': ('picklefield.fields.PickledObjectField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'machine': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['machine.Machine']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'output': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'requires': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'script': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'watting'", 'max_length': '1024'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['task.Task']"})
        },
        u'task.jobtrigger': {
            'Meta': {'object_name': 'JobTrigger', '_ormbases': [u'task.TaskTrigger']},
            'listen_task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trigger_dispatcher'", 'to': u"orm['task.Task']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'success'", 'max_length': '1024'}),
            u'tasktrigger_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['task.TaskTrigger']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'task.project': {
            'Meta': {'object_name': 'Project'},
            'basic_env': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'basic_script': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'docker_image': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'task.task': {
            'Meta': {'object_name': 'Task'},
            'cpuset': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'event_trigger': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'gtask'", 'null': 'True', 'to': u"orm['task.TaskTrigger']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_name_template': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'machine_filter': ('django.db.models.fields.CharField', [], {'default': "'.*'", 'max_length': '1024'}),
            'mem_limit': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'output_path': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gtask'", 'to': u"orm['task.Project']"}),
            'requires': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'task_env': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'task_script': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'})
        },
        u'task.tasktrigger': {
            'Meta': {'object_name': 'TaskTrigger'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        },
        u'task.timetrigger': {
            'Meta': {'object_name': 'TimeTrigger', '_ormbases': [u'task.TaskTrigger']},
            u'tasktrigger_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['task.TaskTrigger']", 'unique': 'True', 'primary_key': 'True'}),
            'time_trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['djcelery.PeriodicTask']"})
        },
        u'task.webhooktrigger': {
            'Meta': {'object_name': 'WebHookTrigger', '_ormbases': [u'task.TaskTrigger']},
            u'tasktrigger_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['task.TaskTrigger']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['task']