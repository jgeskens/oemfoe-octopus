from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from octopus.apply import apply_port_forwards


class Command(BaseCommand):
    help = 'Applies the octopus configuration to the system'

    def handle(self, *args, **options):
        apply_port_forwards()
