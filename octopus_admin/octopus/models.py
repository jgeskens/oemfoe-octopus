from __future__ import unicode_literals

import six

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


@six.python_2_unicode_compatible
class Service(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return '{} (ID {})'.format(self.name, self.pk)


@six.python_2_unicode_compatible
class PortForward(models.Model):
    service = models.ForeignKey(Service)
    name = models.CharField(max_length=255)
    enabled = models.BooleanField(blank=True, default=False)
    source_port = models.PositiveIntegerField()
    destination_host = models.CharField(max_length=255)
    destination_port = models.PositiveIntegerField()

    def __str__(self):
        return '{} (ID {})'.format(self.name, self.pk)


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
