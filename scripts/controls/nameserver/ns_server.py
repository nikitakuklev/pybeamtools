import logging

import netifaces as ni

from pybeamtools.controls.nameserver import start_nameserver_loop
from pybeamtools.utils.logging import config_root_logging


"""
Example of nameserver startup script
"""

if __name__ == "__main__":

    print(f'Interfaces: {ni.interfaces()}')

    config_root_logging(level=logging.DEBUG, reset_handlers=True, suppress_low_priority=False)

    # Find first interface with an IP address
    ip, bcastip = None, None
    for i in ni.interfaces():
        inet = ni.ifaddresses(i).get(ni.AF_INET, None)
        if inet is None:
            continue
        ip = inet[0]['addr']
        bcastip = inet[0].get('broadcast', None)
        if ip is not None and bcastip is not None:
            print(f'Main IP: {ip=} {bcastip=} on {i=}')
            break

    if ip is None or bcastip is None:
        print(f'No IP address found, using defaults')
        ip = '0.0.0.0'
        bcastip = '255.255.255.255'
        interfaces = [ip, bcastip]
    else:
        interfaces = [ip, bcastip, '127.0.0.1']

    # permanent mapping
    pvdb = {'AOP:IOC:TEST1': ('127.0.0.2', 12345, -1.0)}

    try:
        start_nameserver_loop(pvdb=pvdb, epics_interfaces=interfaces)
    except KeyboardInterrupt:
        print(f'Stopping due to keyboard interrupt')
