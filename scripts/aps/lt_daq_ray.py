import logging
import os
import socket
import threading
import time

logging.getLogger('numba').setLevel(logging.WARNING)
logging.getLogger('caproto').setLevel(logging.WARNING)

from pybeamtools.aps.daq.processor import FakeRayLifetimeProcessor

LTP_CONFIG = {'Lifetime500': (2, 5), 'Lifetime1s': (10, 20), 'Lifetime2s': (20, 40)}

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    PAUSE = 4.5
    NEVENTS = 4 * 10 + 1

    import ray
    ray.init()

    ltp = FakeRayLifetimeProcessor(sectors=[1],
                                   lifetime_processors=LTP_CONFIG,
                                   debug=True)
    ltp.setup_streamers()
    ltp.start_streamers()
    ltp.start_aggregator_thread()

    while True:
        logger.info(f'LATEST {ltp.overall_processed=}')
        time.sleep(1)
