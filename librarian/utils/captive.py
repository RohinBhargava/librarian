"""
captive.py: Traps and redirects captive portals

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import logging

from functools import wraps
from urlparse import urljoin

from bottle import request, redirect, abort

from .netutils import IPv4Range, get_target_host

apple = None
mcsft = None
other = None

def setup_portals():
    apple = app.config(conf['librarian.apple_captive_domains']).splitlines()
    mcsft = app.config(conf['librarian.mcsft_captive_domains']).splitlines()
    other = app.config(conf['librarian.other_captive_domains']).splitlines()

def check_captive_portal(root_url, domain):
    if domain in apple:
        path = 'apple-success'
    elif domain in mcsft:
        path = 'microsoft-success'
    elif domain in other:
        path = ''
    else:
        pass
    return urljoin(root_url, path)

def captive_resolver_plugin(root_url, ap_client_ip_range):
    """Load content based on the requested domain"""
    ip_range = IPv4Range(*ap_client_ip_range)

    def decorator(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            target_host = get_target_host()
            is_regular_access = target_host in root_url
            if not is_regular_access and request.remote_addr in ip_range:
                captive_url = check_captive_portal(root_url, target_host)
                return redirect(captive_url)
            return callback(*args, **kwargs)
        return wrapper
    return decorator

def captive_domain_plugin(app):
    app.install(content_resolver_plugin(
        root_url=app.config['librarian.root_url'],
        ap_client_ip_range=app.config['librarian.ap_client_ip_range']
    ))
