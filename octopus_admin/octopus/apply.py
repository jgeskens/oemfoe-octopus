from __future__ import unicode_literals
import os
import six
import glob

from django.template.loader import render_to_string

from .models import PortForward


SERVICE_PREFIX = 'octopus_portfw_'

SERVICE_DIRECTORY = '/etc/service/'


def get_service_directory(portfw):
    return SERVICE_DIRECTORY + SERVICE_PREFIX + six.text_type(portfw.pk)


def get_service_run_script(portfw):
    return get_service_directory(portfw) + '/run'


def render_service_script(portfw):
    return render_to_string('octopus/runit_run_file', {'fw': portfw})


def apply_port_forwards():
    existing_service_dirs = glob.glob(SERVICE_DIRECTORY + SERVICE_PREFIX + '*')

    defined_service_dirs = []
    for portfw in PortForward.objects.filter(enabled=True, service__enabled=True):
        service_dir = get_service_directory(portfw)
        service_script = get_service_run_script(portfw)
        defined_script_content = render_service_script(portfw).encode('utf-8')

        defined_service_dirs.append(service_dir)

        # Create/overwrite service script
        if not service_dir in existing_service_dirs:
            os.makedirs(service_dir)
            need_write = True
            need_restart = False
        else:
            fh = open(service_script, 'rb')
            existing_script_content = fh.read()
            fh.close()
            need_restart = defined_script_content != existing_script_content
            need_write = need_restart

        if need_write:
            fh = open(service_script, 'wb')
            fh.write(defined_script_content)
            fh.close()
            os.system('chmod +x {} > /dev/null'.format(service_script))
        if need_restart:
            os.system('sv restart {} > /dev/null'.format(SERVICE_PREFIX + six.text_type(portfw.pk)))

    for existing_service_dir in existing_service_dirs:
        if not existing_service_dir in defined_service_dirs:
            # Remove service script
            os.system('rm -r {} > /dev/null'.format(existing_service_dir))
