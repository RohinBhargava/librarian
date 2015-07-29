"""
plugin.py: ssid plugin

Change the identifier of the device on dashboard.

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from bottle import request
from bottle_utils.i18n import lazy_gettext as _, i18n_url

from ..dashboard import DashboardPlugin
from ...utils.template import view

import subprocess

@view('ssid/changed_results', error=None, name=None)
def exec_command():
    name = request.query.name
    reset = request.query.reset
    device = open('/etc/platform').read()
    receiver_name = "Outernet"
    path = None
    number = 0

    if name != '':
        if reset == 'no':
            receiver_name += '-' + name

        if 'ORxPi' in device:
            number = 81
            path = '/opt/orx'
            try:
                subprocess.call('sed -i \'3s/ssid=.*/ssid=%s/g\' %s/hostapd.conf'%(receiver_name, path), shell=True)
            except subprocess.CalledProcessError as err:
                return dict(error=err.message)

        elif 'wt200' in device:
            number = 45
            path = '/mnt/persist'

        if path != None and number != 0:
            try:
                subprocess.call('echo %s > %s/.ssid; /etc/init.d/S%dhostapd restart'%(receiver_name, path, number), shell=True)
            except subprocess.CalledProcessError as err:
                return dict(error=err.message)
            return dict(name=receiver_name)

        else:
            return dict(error='Something went wrong. Please try again. If the problem persists, please check your device name or contact your distributor.')

    else:
        return dict(error='You have not given a new name. Please try again!')

def install(app, route):
    route(('changed', exec_command, 'GET', '', {}))


class Dashboard(DashboardPlugin):
    # Translators, used as dashboard section title
    heading = _('Device identifier')
    name = 'ssid'
