import functools
import logging
import time

logging.getLogger('numba').setLevel(logging.WARNING)
logging.getLogger('caproto').setLevel(logging.WARNING)

from pybeamtools.aps.daq.processor import FakeLifetimeProcessor, LifetimeProcessor
from pybeamtools.aps.daq.streamer import FakeTBTStreamer, LifetimeCallback

LTP_CONFIG = {'Lifetime1s': (10, 20), 'Lifetime2s': (20, 40)}

logger = logging.getLogger(__name__)


def test_daq_streamer():
    PAUSE = 5
    NEVENTS = PAUSE * 10 - 3
    streamer = FakeTBTStreamer(name='s1',
                               sector=1,
                               channel='CH:BLA',
                               daemon=True,
                               debug=True
                               )
    streamer.connect()
    assert streamer.is_connected
    time.sleep(0.5)
    assert streamer.event_cnt == 0
    assert not streamer.is_monitoring

    ltcb = LifetimeCallback(LTP_CONFIG, debug=True)
    streamer.add_callback('lifetime', functools.partial(ltcb, st_name='bla'))
    streamer.start_monitor()
    assert streamer.is_monitoring
    time.sleep(PAUSE)
    assert streamer.event_cnt > NEVENTS
    streamer.get_perf_stats()
    perf = streamer.get_perf_stats2()
    assert 0 < perf.avg_load < 1
    assert 9 < perf.event_rate < 11
    logger.info(perf)

    r = streamer.get_callback_results()
    assert len(r) == 3
    assert len(r['cbs']) == 1
    assert r['success']
    assert 0.48 < r['cbs']['lifetime']['Lifetime1s']['raw']['bpm011'] < 0.53
    assert 0.48 < r['cbs']['lifetime']['Lifetime2s']['raw']['bpm011'] < 0.53

    time.sleep(1)
    streamer.stop_monitor()
    assert not streamer.is_monitoring


def test_daq_lifetime_processor():
    PAUSE = 4.5
    NEVENTS = 4 * 10 + 1
    logger.info('test1')
    ltp = FakeLifetimeProcessor(sectors=[1, 3],
                                lifetime_processors=LTP_CONFIG,
                                reset_logging=False,
                                debug=True)
    ltp.setup_streamers()
    assert len(ltp.streamers) == 2
    ltp.start_streamers(NEVENTS)
    for k, v in ltp.streamers.items():
        assert v.is_connected
        assert v.is_monitoring
    logger.info(f'{ltp.streamers=}')

    ltp.start_aggregator_thread()
    time.sleep(PAUSE)

    ltp.stop_aggregator_thread()
    assert not ltp.agg_thread.is_alive()



    assert ltp.n_agg > NEVENTS
    for k, streamer in ltp.streamers.items():
        assert streamer.event_cnt == NEVENTS
        perf = streamer.get_perf_stats2()
        assert 0 < perf.avg_load < 1
        assert 9 < perf.event_rate < 11
        r = streamer.get_callback_results()
        logger.info(f'{r=}')

        assert 0.48 < r['cbs']['lifetime']['Lifetime1s']['raw'][f'bpm{streamer.sector:02d}1'] < 0.52

    logger.info(f'{ltp.last_processed=}')
    logger.info(f'{ltp.overall_processed=}')
    ov = ltp.overall_processed
    assert 0.48 < ov['median_by_streamer']['Lifetime1s']['st_01'] < 0.52
    assert 0.48 < ov['median_by_streamer']['Lifetime2s']['st_01'] < 0.52
    assert 0.48 < ov['by_sector']['Lifetime1s'][1] < 0.52
    assert 0.48 < ov['by_sector']['Lifetime1s'][3] < 0.52

