# -*- coding: utf-8 -*- 
from django.db import models
from datetime import datetime
from fabric.api import run, sudo, cd, put, get
from fabric.contrib.files import exists
from cStringIO import StringIO
import machine.models
import machine
import tempfile
import os
import signal as task_signal
from django.dispatch import receiver
from picklefield.fields import PickledObjectField
import yaml
import docker
from django.core.files.base import ContentFile
import re
from jinja2 import Template


class Task(models.Model):
    name = models.CharField(max_length=1024)

    ## 使用的 docker image
    docker_image = models.CharField(max_length=1024)

    ## 需要上傳的檔案
    input_file = models.FileField(upload_to="./input", null=True, blank=True)

    ### filter machine resource
    machine_filter = models.CharField(max_length=1024, default=".*")
    mem_limit = models.CharField(max_length=1024, null=True, blank=True)
    cpuset = models.CharField(max_length=1024, null=True, blank=True)
    
    ## job 名稱 必須由 task & 輸入資料確定(唯一
    job_name_template = models.CharField(max_length=1024)

    ## requires task 的script
    requires = models.TextField(null=True, blank=True)


    ## docker 環境變數 template
    env_template = models.TextField(null=True, blank=True)

    ## 執行script 的template
    script_template = models.TextField(null=True, blank=True)
    

    ## get job output file from container path
    output_path = models.CharField(max_length=1024, null=True, blank=True)
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode_(self):
        return self.name
    
    def create_job(self, **data):
        job_name =self.job_name_template.format(data=data, now=datetime.now(), task=self)
        try:
            job = Job.objects.get(name=job_name)
        except Exception as e:
            job = Job(name=job_name, status='watting', task=self, data=data)
            job.save()
            task_signal.job_create.send(sender=self.__class__, instance=self)

        return job

    def get_machine(self):
        return machine.get_machine()


class Job(models.Model):
    name = models.CharField(max_length=1024)
    task = models.ForeignKey(Task)
    data = PickledObjectField(null=True, blank=True)

    machine = models.ForeignKey(machine.models.Machine, null=True, blank=True)
    container_id = models.CharField(max_length=1024, null=True, blank=True)


    requires = models.ManyToManyField("self", null=True, blank=True)

    environment = PickledObjectField()
    script = models.TextField()

    status = models.CharField(max_length=1024, default="watting")

    log = models.TextField(null=True, blank=True)

    output = models.FileField(upload_to="output")

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode_(self):
        return self.name

    def save(self, *args, **kwargs):
        self.set_environment()
        self.set_script()
        super(Job, self).save(*args, **kwargs)
        self.set_requires()

    def set_requires(self):
        requires_template = self.task.requires.strip()
        if not requires_template:
            return

        import utils
        from datetime import timedelta

        data = {}
        data["job"] = self
        data["data"] = self.data
        data["get_job_name"] = utils.get_job_name
        data["timedelta"] = timedelta

        job_names = Template(requires_template).render().split(',')
        job_names = [job_name.strip() for job_name in job_names]

        for job in Job.objects.filter(name__in=job_names):
            self.requires.add(job)

    def set_environment(self):
        yaml_data = self.task.env_template.format(job=self)
        data = yaml.load(yaml_data)
        self.environment = data

    def set_script(self):
        self.script = self.task.script_template.format(job=self)


    def prepare(self):
        self.clear()
        ## clean old container
        def upload():
            info = {}
            run('mkdir {}'.format(self.name))
            with cd(self.name):
                file_path = run("pwd")
                requires_path = "input"
                input_file = "input_file"
                script_file_path = "run"
                for job in self.requires.all():
                    put(job.output, os.path.join(requires_path, "{}.out".format(self.name)))

                if self.task.input_file:
                    put(self.task.input_file, input_file)
            
                if self.script.strip():
                    script_file = tempfile.NamedTemporaryFile()
                    script_file.write(self.script.replace("\r", ""))
                    script_file.flush()
                    put(script_file.name, script_file_path, mode="777")

            info['path'] = file_path
            info['requires_path'] = requires_path
            info['input_file'] = input_file
            info['script_file'] = script_file_path

            return info
        return self.machine.fab(upload)




    def clear(self):
        ## clean old container
        containers = self.machine.docker_client.containers(all=True)
        if any(["/{}".format(self.name) in container['Names'] for container in containers]):
            print 'clear container'
            self.machine.docker_client.stop(self.name)
            self.machine.docker_client.remove_container(self.name)
        
        def remove():
            if exists(self.name):
                sudo('rm -rf {}'.format(self.name))

        self.machine.fab(remove)

    def load_status(self):
        try:
            info = self.machine.docker_client.inspect_container(self.container_id)
            self.log = self.machine.docker_client.logs(self.container_id)
            status = info['State']
            if status['Running']:
                self.status = 'running'
            elif status['ExitCode']: 
                self.status = 'fault'
                task_signal.job_fault.send(sender=self.__class__, instance=self)
            else:
                self.status = 'success'
                self.post_success()
                task_signal.job_success.send(sender=self.__class__, instance=self)
        except Exception as e:
            print e
            self.status = 'fault'
            task_signal.job_fault.send(sender=self.__class__, instance=self)
             
        self.save()
            

    def post_success(self):
        if not self.task.output_path:
            return
        client = self.machine.docker_client
        output_file = client.copy(self.container_id, self.task.output_path)
        output_content = re.sub( "\x00+$", "", output_file.read())
        client.remove_container(self.container_id)
        f = ContentFile(output_content)
        self.output.save("output", f)
        self.clear()

            
    def start(self):
        if self.status in ('watting', 'fault') and all([job.status=='success' for job in self.requires.all()]):
            self.machine = self.task.get_machine()

            task_signal.job_prestart.send(sender=self.__class__, instance=self)

            info = self.prepare()
            
            file_path = info['path']
            env = self.environment

            container_path = "/srv/info"
            env['SCRIPT'] = os.path.join(container_path, info['script_file'])
            env['REQUIREMENTS'] = os.path.join(container_path, info['requires_path'])
            env['INPUT_FILE'] = os.path.join(container_path, info['input_file'])




            try:
                self.machine.docker_client.inspect_image(self.task.docker_image)
            except Exception as e:
                self.machine.docker_client.pull(self.task.docker_image)
            container_info = self.machine.docker_client.create_container(
                    image=self.task.docker_image,
                    command="bash {}".format(env['SCRIPT']),
                    environment=env,
                    name=self.name,
                    working_dir=container_path,
                    volumes=[container_path],
                    host_config=docker.utils.create_host_config(
                        binds={file_path:
                            {"bind":container_path, "ro":False}
                        }
                    )
                )



            self.container_id = container_info['Id']
            self.machine.docker_client.start(self.container_id)
            self.status = 'running'
            self.save()

            task_signal.job_poststart.send(sender=self.__class__, instance=self)


    def stop(self):
        self.clear()
        self.status = 'fault'

    def restart(self):
        self.stop()
        self.start()

    @classmethod
    def scan(cls):
        watting_jobs = cls.objects.filter(status = 'watting')
        for job in watting_jobs:
            job.start()

        running_jobs = cls.objects.filter(status == 'running')
        for job in running_jobs:
            job.load_status()
        



@receiver(task_signal.job_prestart, sender=Job)
def job_prestart(*args, **kwargs):
    print 'job_prestart'


@receiver(task_signal.job_poststart, sender=Job)
def job_poststart(*args, **kwargs):
    print 'job_poststart'


@receiver(task_signal.job_success, sender=Job)
def job_success(*args, **kwargs):
    print 'job_success'
