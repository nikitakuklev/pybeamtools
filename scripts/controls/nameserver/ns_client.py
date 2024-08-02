import logging
import socket
import time

from pybeamtools.controls.nameserver import NSClient
from pybeamtools.sim.softioc import DynamicIOC
from pybeamtools.utils.logging import config_root_logging

"""
Example of a soft IOC that has clock PV and declares it to the nameserver occasionally
"""

if __name__ == "__main__":

    config_root_logging(level=logging.DEBUG, reset_handlers=True, suppress_low_priority=False)

    # A way to try guessing primary interface with default route
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    db = {'AOP:CONSTANT': 1.0}
    sioc = DynamicIOC(data=db, interfaces=['0.0.0.0'])
    sioc.run_in_background()
    time.sleep(1)

    # Note how we can add a channel to the IOC after it has started
    # Wildcards, mirrors, and other forbidden magic things are possible
    sioc.add_channel('AOP:CLOCK', time.time())

    nsc = NSClient(nameserver='127.0.0.1')
    port = sioc.port

    t = 0.0
    while True:
        sioc.send_updates('AOP:CLOCK', time.time())
        time.sleep(1.0)

        if time.time() - t > 30.0:
            try:
                nsc.publish_channels(channels=list(sioc.pvdb.keys()), address=ip, port=port, timeout=60)
                logging.info(f'Published {sioc.pvdb.keys()} to NS')
            except Exception as ex:
                logging.error(f'Couldnt update NS', exc_info=True, stack_info=True)
            finally:
                t = time.time()
