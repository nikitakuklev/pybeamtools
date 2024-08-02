from pybeamtools.aps.daq.streamer import TBTStreamer
from pybeamtools.controlsdirect import Accelerator

acc = Accelerator.get_singleton()


class TimingDelayStreamer(TBTStreamer):
    def __init__(self, reference_channel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reference_channel = reference_channel

        self.add_callback('timing_delay', self.timing_delay_callback)
