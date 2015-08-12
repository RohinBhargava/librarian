"""
captive.py: Traps and redirects captive portals

Copyright 2014-2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import logging, sys

from functools import wraps
from urlparse import urljoin

from bottle import request, redirect, abort

from core_helpers import get_content_url

from .netutils import IPv4Range, get_target_host

def check_captive_portal(root_url, domain, apple, mcsft, other):
    if domain in apple:
        path = 'apple-success'
    elif domain in mcsft:
        path = 'microsoft-success'
    elif domain in other:
        path = ''
    else:
        return get_content_url(root_url, domain)
    return urljoin(root_url, path)

def captive_resolver_plugin(root_url, ap_client_ip_range, apple, mcsft, other):
    """Load content based on the requested domain"""
    ip_range = IPv4Range(*ap_client_ip_range)

    def decorator(callback):
        @wraps(callback)
        def wrapper(*args, **kwargs):
            target_host = get_target_host()
            is_regular_access = target_host in root_url
            if not is_regular_access and request.remote_addr in ip_range:
                captive_url = check_captive_portal(root_url, target_host, apple, mcsft, other)
                return redirect(captive_url)
            return callback(*args, **kwargs)
        return wrapper
    return decorator

def captive_domain_plugin(app):
    app.install(captive_resolver_plugin(
        root_url=app.config['librarian.root_url'],
        ap_client_ip_range=app.config['librarian.ap_client_ip_range'],
        apple = app.config['librarian.apple_captive_domains'].splitlines(),
        mcsft = app.config['librarian.mcsft_captive_domains'].splitlines(),
        other = app.config['librarian.other_captive_domains'].splitlines()
    ))
