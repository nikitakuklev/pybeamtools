import functools
import logging
import time

logging.getLogger('numba').setLevel(logging.WARNING)
logging.getLogger('caproto').setLevel(logging.WARNING)

from pybeamtools.aps.daq.processor import FakeLifetimeProcessor, LifetimeProcessor
from pybeamtools.aps.daq.streamer import FakeTBTStreamer, LifetimeCallback

LTP_CONFIG = {'Lifetime1s': (10, 20), 'Lifetime2s': (20, 40)}

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    PAUSE = 4.5
    NEVENTS = 4 * 10 + 1
    ltp = FakeLifetimeProcessor(sectors=[1, 3],
                                lifetime_processors=LTP_CONFIG,
                                debug=True)
    ltp.setup_streamers()
    ltp.start_streamers(NEVENTS)
    ltp.start_aggregator_thread()

    while True:
        logger.info(f'{ltp.overall_processed=}')
        time.sleep(1)