import logging
import queue
import threading
import time
from typing import Callable, Any, Union

import numpy as np

from .devices import VirtualDevice

TRACE=False

class Subscription:
    def __init__(self, device: VirtualDevice, engine):
        self.device = device
        self.name = self.device.name
        self.engine = engine
        self.callbacks = []
        self.logger = logging.getLogger(self.__class__.__qualname__)

    def add_callback(self, cb: Callable):
        assert isinstance(cb, Callable)
        self.callbacks.append(cb)

    def process_update(self, value):
        for cb in self.callbacks:
            cb(self, value)


class Metadata:
    pass


class Measurement:
    def __init__(self, data: np.ndarray, timestamp: float):
        self.metadata = Metadata()
        self.metadata.timestamp = timestamp
        self.data = data

    data_count = property(lambda self: len(self.data))


class ChannelSubscription:
    def __init__(self, channel: str, engine):
        self.channel = channel
        self.name = channel
        self.engine = engine
        self.callbacks = []
        self.logger = logging.getLogger(self.__class__.__qualname__)

    def add_callback(self, cb: Callable):
        assert isinstance(cb, Callable)
        self.callbacks.append(cb)

    def process_update(self, value):
        if self.engine.TRACE:
            self.logger.debug(f'Running ({len(self.callbacks)}) callbacks for channel ({self.name})')
        for cb in self.callbacks:
            cb(self, value)


class SimulationError(Exception):
    pass


class ChannelMap:
    def __init__(self, device: VirtualDevice, output: str, read_fun: Callable, write_fun: Callable = None):
        self.device = device
        self.output = output
        self.read_fun = read_fun
        self.write_fun = write_fun

    def process_read(self) -> Union[str, int, float]:
        return self.read_fun(self.device, self.output)

    def process_write(self, value):
        if self.write_fun is None:
            raise SimulationError(f'Channel map ({self.output}) -> ({self.device}) does not support writes')
        return self.write_fun(self.device, self.output, value)


class ChannelMapper:
    def __init__(self, maps: list[ChannelMap]):
        self.channel_maps = maps
        self.output_to_map = {}
        for m in maps:
            if m.output in self.output_to_map:
                raise ValueError(f'Output ({m.output}) already exists in this mapper')
            self.output_to_map[m.output] = m

    def required_devices(self):
        return list(set([c.device.name for c in self.channel_maps]))

    def available_channels(self):
        return list(set([c.output for c in self.channel_maps]))

    def process_read(self, output_name: str) -> Union[str, int, float]:
        return self.output_to_map[output_name].process_read()

    def process_write(self, output_name: str, value) -> Union[str, int, float]:
        return self.output_to_map[output_name].process_write(value)


class SimulationEngine:

    def __init__(self):
        self.devices: dict[str, VirtualDevice] = {}
        self.channels: list[str] = []
        self.subscriptions: dict[str, Subscription] = {}
        self.channel_subs: dict[str, ChannelSubscription] = {}
        self.periods = {}
        self.times = []
        self.next_periodic_read_time: dict[str, float] = {}
        self.maps: list[ChannelMapper] = []
        self.channel_to_mapper: dict[str, ChannelMapper] = {}
        self.device_channels: dict[str, list[str]] = {}
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.is_running = False
        self.cmdq = None
        self.poll_thread = None
        self.TRACE = False

    def add_device(self, device: VirtualDevice, period: float):
        assert not self.is_running
        if device.name in self.devices:
            raise ValueError(f'Device {device.name} is already added')
        self.devices[device.name] = device
        self.periods[device.name] = period
        self.logger.debug(f'Added device {device.name} with update period of {period}')

    def add_mapper(self, mapper: ChannelMapper):
        device_names = mapper.required_devices()
        for dn in device_names:
            assert dn in self.devices
        outputs = mapper.available_channels()
        for dn in device_names:
            if dn not in self.device_channels:
                self.device_channels[dn] = []
            self.device_channels[dn] += outputs
        for out in outputs:
            self.channel_to_mapper[out] = mapper
        self.channels.extend(outputs)
        self.maps.append(mapper)
        self.logger.debug(f'Added mapper for outputs {outputs} from devices {device_names}')

    def subscribe(self, device_name: str) -> Subscription:
        assert device_name in self.devices
        if device_name not in self.subscriptions:
            self.logger.debug(f'Created subscription for device {device_name}')
            self.subscriptions[device_name] = Subscription(device=self.devices[device_name],
                                                           engine=self)
        return self.subscriptions[device_name]

    def subscribe_channel(self, channel_name: str) -> ChannelSubscription:
        assert channel_name in self.channels, f'Channel {channel_name} not found'
        if channel_name not in self.channel_subs:
            self.logger.debug(f'Created subscription for channel {channel_name}')
            self.channel_subs[channel_name] = ChannelSubscription(channel=channel_name,
                                                                  engine=self)
        return self.channel_subs[channel_name]

    def schedule_update(self):
        now = time.time()
        self.next_periodic_read_time = {k: now for k in self.next_periodic_read_time}

    def start_update_thread(self):
        def _poll(cmdq: queue.Queue):
            self.logger.debug(f'Hello from simulation poll thread (id {threading.get_ident()})')
            t = time.time()
            #times = {k: t for k in self.devices}
            self.next_periodic_read_time = {k: t for k in self.devices}
            while True:
                # self.logger.debug(f'Poll loop running at {now=}')
                for dev in self.devices:
                    now = time.time()
                    if self.next_periodic_read_time[dev] < now:
                        val = self.devices[dev].read()
                        self.next_periodic_read_time[dev] += self.periods[dev]
                        if self.TRACE:
                            self.logger.debug(f'New value {val} for device ({dev}), next in (+{self.periods[dev]})s')

                        # Trigger devices
                        if dev in self.subscriptions:
                            self.subscriptions[dev].process_update(val)

                        # Trigger channels
                        for channel in self.device_channels[dev]:
                            if channel in self.channel_subs:
                                channel_value = self.channel_to_mapper[channel].process_read(channel)
                                self.channel_subs[channel].process_update(channel_value)
                try:
                    cmd = cmdq.get(timeout=0.01)
                    if cmd is None:
                        self.logger.debug(f'Goodbye from simulation poll thread')
                        break
                except queue.Empty:
                    pass

        self.cmdq = queue.Queue()
        self.logger.debug(f'Starting poll thread')
        th = threading.Thread(target=_poll,
                              name='sim_engine_poll',
                              args=(self.cmdq,))
        th.daemon = True
        th.start()
        self.is_running = True
        self.poll_thread = th

    def stop_update_thread(self):
        assert self.is_running
        self.cmdq.put(None)
        self.poll_thread.join(timeout=1.0)

        self.is_running = False
        self.cmdq = None
        self.poll_thread = None

    def read_device(self, device_name: str):
        assert device_name in self.devices
        self.logger.debug(f'Reading device {device_name}')
        value = self.devices[device_name].read()
        return value

    def read_channel(self, channel_name: str):
        assert channel_name in self.channels
        self.logger.debug(f'Reading channel {channel_name}')
        value = self.channel_to_mapper[channel_name].process_read(channel_name)
        return value

    def write_device(self, device_name: str, value: Any):
        self.devices[device_name].write(value)

    def write_channel(self, channel_name: str, value: Any):
        assert channel_name in self.channels
        self.logger.debug(f'Writing channel {channel_name}')
        self.channel_to_mapper[channel_name].process_write(channel_name, value)
