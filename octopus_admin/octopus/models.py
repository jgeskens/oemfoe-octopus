from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Service(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(blank=True, default=False)


class PortForward(models.Model):
    service = models.ForeignKey(Service)
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(blank=True, default=False)
    source_port = models.PositiveIntegerField()
    destination_host = models.CharField(max_length=255)
    destination_port = models.PositiveIntegerField()


@receiver(post_save)
def apply_post_save(sender, **kwargs):
    from .apply import apply_port_forwards
    if sender in (Service, PortForward):
        apply_port_forwards()


@receiver(post_delete)
def apply_post_delete(sender, **kwargs):
    from .apply import apply_port_forwards
    if sender in (Service, PortForward):
        apply_port_forwards()
