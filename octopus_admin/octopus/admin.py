from django.contrib import admin

from .models import Service, PortForward


class PortForwardInline(admin.TabularInline):
    model = PortForward
    extra = 0


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'enabled')
    list_editable = ('enabled',)
    inlines = (PortForwardInline,)


admin.site.register(Service, ServiceAdmin)
