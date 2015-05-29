from django.contrib import admin

from .models import Machine


# Register your models here.

class MachineAdmin(admin.ModelAdmin):
    list_display = ["name", "status"]


admin.site.register(Machine, MachineAdmin)
