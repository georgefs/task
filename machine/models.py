from django.db import models
from gmachine import machine
from picklefield.fields import PickledObjectField

# Create your models here.

class Machine(models.Model):
    name = models.CharField(max_length=1024)
    settings = PickledObjectField()
    status = models.CharField(max_length=1024, choices=(('running', 'running'), ('stop', 'stop')))
    

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __unicode_(self):
        return self.name
    
    @property
    def docker_client(self):
        return machine.docker_client(self.name, self.settings)

    def fab(self, callback):
        return machine.fab(self.name, callback, machine_info=self.settings)

    def info(self):
        settings = self.settings

        client = machine.docker_client(machine_name=self.name, machine_info=settings)
        info = client.info()
        return info
