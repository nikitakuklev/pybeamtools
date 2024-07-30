import logging
import time

logging.getLogger('numba').setLevel(logging.WARNING)
logging.getLogger('caproto').setLevel(logging.WARNING)

from pybeamtools.aps.daq.processor import FakeRayLifetimeProcessor

LTP_CONFIG = {'Lifetime1s': (5, 10), 'Lifetime2s': (10, 20)}

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    PAUSE = 4.5
    NEVENTS = 4 * 10 + 1

    import ray
    ray.init()

    ltp = FakeRayLifetimeProcessor(sectors=[1],
                                   lifetime_processors=LTP_CONFIG,
                                   #polling_period=0.5,
                                   debug=True,
                                   streamer_kwargs={'event_period':0.45})
    ltp.setup_streamers()
    ltp.start_streamers()
    ltp.start_aggregator_thread()

    while True:
        logger.info(f'LATEST {ltp.overall_processed=}')
        time.sleep(1)
