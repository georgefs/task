# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskTrigger'
        db.create_table(u'task_tasktrigger', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal(u'task', ['TaskTrigger'])

        # Adding model 'WebHookTrigger'
        db.create_table(u'task_webhooktrigger', (
            (u'tasktrigger_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['task.TaskTrigger'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'task', ['WebHookTrigger'])

        # Adding model 'JobTrigger'
        db.create_table(u'task_jobtrigger', (
            (u'tasktrigger_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['task.TaskTrigger'], unique=True, primary_key=True)),
            ('listen_task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trigger_dispatcher', to=orm['task.Task'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='success', max_length=1024)),
        ))
        db.send_create_signal(u'task', ['JobTrigger'])

        # Adding model 'TimeTrigger'
        db.create_table(u'task_timetrigger', (
            (u'tasktrigger_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['task.TaskTrigger'], unique=True, primary_key=True)),
            ('time_trigger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['djcelery.PeriodicTask'])),
        ))
        db.send_create_signal(u'task', ['TimeTrigger'])

        # Adding model 'Project'
        db.create_table(u'task_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('docker_image', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('input_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('basic_env', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('basic_script', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal(u'task', ['Project'])

        # Adding model 'Task'
        db.create_table(u'task_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gtask', to=orm['task.Project'])),
            ('machine_filter', self.gf('django.db.models.fields.CharField')(default='.*', max_length=1024)),
            ('mem_limit', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('cpuset', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('job_name_template', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('requires', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('task_env', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('task_script', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('output_path', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('event_trigger', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='gtask', null=True, to=orm['task.TaskTrigger'])),
        ))
        db.send_create_signal(u'task', ['Task'])

        # Adding model 'Job'
        db.create_table(u'task_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['task.Task'])),
            ('data', self.gf('picklefield.fields.PickledObjectField')(null=True, blank=True)),
            ('machine', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['machine.Machine'], null=True, blank=True)),
            ('container_id', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('environment', self.gf('picklefield.fields.PickledObjectField')()),
            ('script', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='watting', max_length=1024)),
            ('log', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('output', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'task', ['Job'])

        # Adding M2M table for field requires on 'Job'
        m2m_table_name = db.shorten_name(u'task_job_requires')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_job', models.ForeignKey(orm[u'task.job'], null=False)),
            ('to_job', models.ForeignKey(orm[u'task.job'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_job_id', 'to_job_id'])


    def backwards(self, orm):
        # Deleting model 'TaskTrigger'
        db.delete_table(u'task_tasktrigger')

        # Deleting model 'WebHookTrigger'
        db.delete_table(u'task_webhooktrigger')

        # Deleting model 'JobTrigger'
        db.delete_table(u'task_jobtrigger')

        # Deleting model 'TimeTrigger'
        db.delete_table(u'task_timetrigger')

        # Deleting model 'Project'
        db.delete_table(u'task_project')

        # Deleting model 'Task'
        db.delete_table(u'task_task')

        # Deleting model 'Job'
        db.delete_table(u'task_job')

        # Removing M2M table for field requires on 'Job'
        db.delete_table(db.shorten_name(u'task_job_requires'))


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
            'requires': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'requires_rel_+'", 'null': 'True', 'to': u"orm['task.Job']"}),
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