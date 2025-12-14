import argparse
import collections
import logging
import time

import caproto.threading.client
import numpy as np

from pybeamtools.controlsdirect import Accelerator

logger = logging.getLogger(__name__)


def compute_lifetime_exponential(
    times: np.ndarray,
    current_data: np.ndarray,
    offset: float = 0.0,
    normalized: bool = False,
    coupling: float | None = None,
    reference_current: float = 25.0,
    normalized_power: float = 2 / 3,
):
    # N = N0*exp(-lambda*t)
    # ln(N) = -lambda*t + ln(N0)
    # y = a*t+b
    # lifetime = 1/lambda = 1/-slope
    # normlifetime = lifetime * (current^2/3 / ref_current^2/3) * (1/sqrt(couplingratio))

    if len(current_data) < 2:
        raise ValueError("Error - not enough current datapoints")
    assert np.all(current_data > 0)
    if normalized:
        assert coupling is not None and coupling > 0
        assert reference_current > 0
    current_data += offset
    avg_current = current_data.mean()

    lncurrent = np.log(current_data)
    coef, cov = np.polyfit(times, lncurrent, 1, cov=True)  # cov
    stdev = np.sqrt(np.diag(cov))
    slope = coef[0]

    lifetime = -1 / slope / 3600
    # z2 = np.polyfit(times, current_data, 1)
    # logger.debug(f'Unnormalized lifetime is %.3f h (linear lifetime %.3f)', lifetime, -avg_current/z2[0]/3600)
    logger.debug("Unnormalized lifetime is %.3fh", lifetime)

    if normalized:
        normalized_lifetime = lifetime * (avg_current / reference_current) ** normalized_power
        normalized_lifetime = normalized_lifetime * np.sqrt(1.0) / np.sqrt(coupling)
        logger.debug(f"Normalized lifetime is {normalized_lifetime:.3f}h")
        print(normalized_lifetime)


def compute_lifetime_exponential_v2(
    times: np.ndarray, mat: np.ndarray, offset=None, clip_min: float = 1.0, inplace=True
) -> np.ndarray:
    # logging.warning(f'{(times, mat, offset, clip_min)=}')
    if clip_min is not None:
        if inplace:
            mat.clip(clip_min, None, out=mat)
        else:
            mat = np.clip(mat, clip_min, None)
    if offset is not None:
        if inplace:
            mat += offset[None, :]
        else:
            mat = mat + offset[None, :]
    lncurrent = np.log(mat)
    z = np.polynomial.polynomial.polyfit(times, lncurrent, 1)
    slopes = z[1, :]
    lifetimes = -1 / slopes / 3600
    return lifetimes


def lifetime_linear_fit(times: np.ndarray, mat: np.ndarray, offset=None, clip_min: float = 1.0) -> np.ndarray:
    if clip_min is not None:
        mat.clip(clip_min, None, out=mat)
    if offset is not None:
        mat += offset[None, :]
    lncurrent = np.log(mat)
    z = np.polynomial.polynomial.polyfit(times, lncurrent, 1)
    return z


class LifetimeMeasurer:
    def __init__(self, mode="relative_change", mode_kwargs=None):
        assert mode in ["relative_change", "absolute_change"]
        self.mode = mode
        self.mode_kwargs = mode_kwargs
        self.time_slices = []
        self.data_slices = []
        self.initial_current = None

    def update(self, time: np.ndarray, data: np.ndarray, aux_df=None):
        if self.initial_current is None:
            self.initial_current = data[0]
        if self.mode == "relative_change":
            threshold = self.initial_current * (1 - self.mode_kwargs["threshold"])
        elif self.mode == "absolute_change":
            threshold = self.initial_current - self.mode_kwargs["threshold"]
        # if current_data[-1] > threshold:
        #     raise ValueError(f'Error - too small current change {current_data[0]} -> {current_data[-1]}')

        return False


class LifetimeMeasureAdaptive:
    def __init__(
        self,
        channel_current: str = "APSU:MMPS2:DCCT1:beamC-Calc",
        channel_coupling: str = "S:VID1:filteredCoupling",
        max_time: float = 25.0,
        min_time: float = 10.0,
        min_current_change: float = 0.0002,
        max_current_change: float = 0.0006,
        relative_change_mode: bool = True,
        normalized_current: bool = True,
        normalized_coupling: bool = False,
        normalized_power: float = 2 / 3,
        current_ref: float = 25.0,
    ):
        self.channel = channel_current
        self.channel_coupling = channel_coupling
        self.pvs = {}
        self.subs = {}
        self.acc = Accelerator.get_singleton()

        assert max_time > min_time
        assert max_current_change > min_current_change
        assert isinstance(relative_change_mode, bool)
        assert isinstance(normalized_current, bool)
        assert isinstance(normalized_coupling, bool)

        self.max_time = max_time
        self.min_time = min_time
        self.min_current_change = min_current_change
        self.max_current_change = max_current_change
        self.relative_change_mode = relative_change_mode
        self.normalized_current = normalized_current
        self.normalized_coupling = normalized_coupling
        self.normalized_power = normalized_power
        self.current_ref = current_ref

    def setup_data_collection(self):
        """Set up EPICS monitoring for pv"""
        self.acc.ensure_monitored(self.channel)
        if self.normalized_coupling:
            self.acc.ensure_monitored(self.channel_coupling)

    def get_pv_data(self, pv, t1, t2=None):
        t2 = t2 or time.time()
        times, current_data = self.acc.get_buffer_data_slice(self.channel, start=t1, end=t2, store_local_time=True)
        return times, current_data

    def measure(self):
        t_start = time.time()
        delta = lambda: time.time() - t_start

        self.setup_data_collection()

        while True:
            if delta() < self.min_time:
                time.sleep(0.1)
                continue

            if delta() > self.max_time:
                logger.debug(f"Stopping in {delta():.2f}s due to exceeding max time")
                break

            times, current_data = self.get_pv_data(self.channel, t_start)
            assert len(current_data) > 0

            if len(current_data) == 1:
                time.sleep(0.1)
                continue

            if self.relative_change_mode:
                threshold = current_data[0] * (1 - self.max_current_change)
            else:
                threshold = current_data[0] - self.max_current_change
            if current_data[-1] < threshold:
                logger.debug(f"Stopping in {delta():.2f}s due to exceeding current loss {current_data[0] - threshold}")
                break

        t_elapsed = delta()

        times, current_data = self.get_pv_data(self.channel, t_start)
        logger.debug(f"Got {len(current_data)} current points in {t_elapsed:.2f}s")

        lifetime, avg_current, ltstdev = self.compute_raw_lifetime(times, current_data)

        normalized_lifetime = lifetime
        if self.normalized_coupling:
            times2, coupling_data = self.get_pv_data(self.channel_coupling, t_start)
            if len(coupling_data) < 2:
                raise ValueError(f"Error - not enough coupling datapoints")
            logger.debug(f"Got {len(coupling_data)} coupling points in {t_elapsed:.2f}s")
            avg_coupling = coupling_data.mean()
            logger.debug(f"Average coupling is {avg_coupling:.3f}")
            normalized_lifetime = normalized_lifetime * np.sqrt(1.0) / np.sqrt(avg_coupling)
            logger.debug(f"Normalized coupling lifetime is {normalized_lifetime:.3f}h")

        if self.normalized_current:
            logger.debug(f"Normalizing by current ^ {self.normalized_power:.3f} to {self.current_ref:.3f}mA")
            normalized_lifetime = normalized_lifetime * (avg_current / self.current_ref) ** self.normalized_power
            logger.debug(f"Normalized current lifetime is {normalized_lifetime:.3f}h")

        return float(lifetime), float(normalized_lifetime), float(np.mean(current_data))

    def compute_raw_lifetime(self, times: np.ndarray, current_data: np.ndarray):
        # N = N0*exp(-lambda*t)
        # ln(N) = -lambda*t + ln(N0)
        # y = a*t+b
        # lifetime = 1/lambda = 1/-slope
        # normlifetime = lifetime * (current^2/3 / ref_current^2/3) * (1/sqrt(couplingratio))
        if len(current_data) < 2:
            raise ValueError(f"Error - not enough current datapoints")
        assert np.all(current_data > 0)
        avg_current = current_data.mean()
        logger.debug(f"Average current is %.3f", avg_current)

        if self.relative_change_mode:
            threshold = current_data[0] * (1 - self.min_current_change)
        else:
            threshold = current_data[0] - self.min_current_change
        if current_data[-1] > threshold:
            raise ValueError(f"Error - too small current change {current_data[0]} -> {current_data[-1]}")

        lncurrent = np.log(current_data)
        z, cov = np.polyfit(times, lncurrent, 1, cov=True)  # cov
        stdev = np.sqrt(np.diag(cov))[0]
        slope = z[0]

        lifetime = -1 / slope / 3600
        stdev_lifetime = stdev / (slope**2) / 3600
        # z2 = np.polyfit(times, current_data, 1)
        # logger.debug(f'Unnormalized lifetime is %.3f h (linear lifetime %.3f)', lifetime, -avg_current/z2[0]/3600)
        logger.debug(f"Unnormalized lifetime is %.3fh", lifetime)
        return float(lifetime), float(avg_current), float(stdev_lifetime)

    def compute_lifetime(self, times: np.ndarray, current_data: np.ndarray):
        lifetime, avg_current, ltstdev = self.compute_raw_lifetime(times, current_data)

        normalized_lifetime = lifetime
        if self.normalized_coupling:
            raise Exception

        if self.normalized_current:
            logger.debug(f"Normalizing by current ^ {self.normalized_power:.3f} to {self.current_ref:.3f}mA")
            normalized_lifetime = normalized_lifetime * (avg_current / self.current_ref) ** self.normalized_power
            logger.debug(f"Normalized current lifetime is {normalized_lifetime:.3f}h")
            ltstdev = ltstdev * (avg_current / self.current_ref) ** self.normalized_power

        return float(lifetime), float(normalized_lifetime), float(np.mean(current_data)), float(ltstdev)


def lifetime_cli():
    logger = logging.getLogger(__name__)
    logging.basicConfig()
    logging.getLogger("caproto").propagate = False

    parser = argparse.ArgumentParser()
    parser.add_argument("-current", type=str, default="APSU:MMPS2:DCCT1:beamC-Calc", help="current channel PV")
    parser.add_argument("-minchange", type=float, default=0.0002, help="min fractional/abs current change")
    parser.add_argument("-maxchange", type=float, default=0.0006, help="max fractional/abs current change")
    parser.add_argument("-changemode", action="store_true", default=True)
    parser.add_argument("-tmax", type=float, default=25.0)
    parser.add_argument("-tmin", type=float, default=10.0)
    parser.add_argument("-cref", type=float, default=25.0)
    parser.add_argument("-norm", action="store_true", default=True)
    parser.add_argument("-normpow", type=float, default=2 / 3)
    parser.add_argument("-verbose", action="store_true", default=False)
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logging.disable()

    ltm = LifetimeMeasureAdaptive(
        channel_current=args.current,
        max_time=args.tmax,
        min_time=args.tmin,
        min_current_change=args.minchange,
        max_current_change=args.maxchange,
        relative_change_mode=args.changemode,
        normalized_current=args.norm,
        current_ref=args.cref,
        normalized_power=args.normpow,
    )
