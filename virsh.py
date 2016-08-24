# Copyright 2015 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Virsh Power Driver."""

from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    )
import urllib2
str = None

__metaclass__ = type
__all__ = []

from provisioningserver.drivers.hardware.virsh import (
    power_control_virsh,
    power_state_virsh,
)
from provisioningserver.drivers.power import PowerDriver
from provisioningserver.utils import shell


REQUIRED_PACKAGES = []


def extract_virsh_parameters(context):
    poweraddr = context.get('power_address')
    machine = context.get('power_id')
    password = context.get('power_pass')
    return poweraddr, machine, password


class VirshPowerDriver(PowerDriver):

    name = 'virsh'
    description = "Virsh Power Driver."
    settings = []
    vmrunapi_url="http://10.0.0.1:6000/vmrun"

    def detect_missing_packages(self):
        missing_packages = set()
        for binary, package in REQUIRED_PACKAGES:
            if not shell.has_command_available(binary):
                missing_packages.add(package)
        return list(missing_packages)

    def power_on(self, system_id, context):
        """Power on Virsh node."""
        power_change = 'on'
        poweraddr, machine, password = extract_virsh_parameters(context)
        urllib2.urlopen('http://10.0.0.1:6000/vmrun/vm/start/%s' %poweraddr)

    def power_off(self, system_id, context):
        """Power off Virsh node."""
        power_change = 'off'
        poweraddr, machine, password = extract_virsh_parameters(context)
        urllib2.urlopen('http://10.0.0.1:6000/vmrun/vm/stop/%s' %poweraddr)

    def power_query(self, system_id, context):
        poweraddr, machine, password = extract_virsh_parameters(context)
        """Power query Virsh node."""
        status = urllib2.urlopen('http://10.0.0.1:6000/vmrun/vm/status/%s' %poweraddr).read()
        return status
