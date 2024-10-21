import collections
import logging
import time

import numpy as np


class LifetimeCallback:
    add_msum_field = True

    def __init__(self,
                 lifetime_processors: dict[str, tuple[int, int]],
                 lower_limit: float = None,
                 upper_limit: float = None,
                 max_diff_from_first_sample_threshold: float = None,
                 max_diff_from_first_sample_count: int = None,
                 no_beam_threshold: float = None,
                 no_beam_count: int = None,
                 debug=False,
                 ):
        self.results = {}
        for k, v in lifetime_processors.items():
            self.results[k] = collections.deque(maxlen=100)
        self.counter = 0
        self.lifetime_processors = lifetime_processors
        self.result_last = {}
        self.result_combined = {k: {} for k in self.lifetime_processors.keys()}
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.log_with_print = False
        assert isinstance(lower_limit, (float, int, type(None))), f"Invalid {lower_limit=}"
        assert isinstance(upper_limit, (float, int, type(None))), f"Invalid {upper_limit=}"
        self.lower_limit = float(lower_limit)
        self.upper_limit = float(upper_limit)
        assert isinstance(max_diff_from_first_sample_threshold, (float, int, type(None)))
        assert isinstance(max_diff_from_first_sample_count, (int, type(None)))
        self.max_diff_from_first_sample_threshold = max_diff_from_first_sample_threshold
        self.max_diff_from_first_sample_count = max_diff_from_first_sample_count
        assert isinstance(no_beam_threshold, (float, int, type(None)))
        assert isinstance(no_beam_count, (int, type(None)))
        self.no_beam_threshold = no_beam_threshold
        self.no_beam_count = no_beam_count

    def ldebug(self, msg):
        if self.debug:
            self.logger.debug(msg, stacklevel=2)

    def reset_counters(self):
        self.counter = 0

    def __call__(self, streamer, data: dict, st_name: str, trig_counter: int = -1):
        from pybeamtools.physics.lifetime import compute_lifetime_exponential_v2

        cnt = self.counter
        updates = {}

        # if self.debug:
        #    print(f"Processing S{sector} {cnt=} from {streamer=}")
        for metric, metric_config in self.lifetime_processors.items():
            trig_cnt, frame_cnt = metric_config
            if cnt > 0 and cnt % trig_cnt == 0:
                mat, times, tags = streamer.get_latest_buffers(frame_cnt)

                if mat is not None:
                    # Check first vs later samples to detect reinjection
                    if self.max_diff_from_first_sample_threshold is not None:
                        diff = mat[1:, :] - mat[0:1, :]
                        maxdiff = np.max(diff, axis=0)
                        n_exceeded = np.sum(diff > self.max_diff_from_first_sample_threshold, axis=0)
                        fail_cnt = np.sum(n_exceeded > 0)
                        # fail_cnt = 0
                        # for col in range(mat.shape[1]):
                        #     diff = mat[1:, col] - mat[0, col]
                        #     n_exceeded = np.sum(diff > self.max_diff_from_first_sample_threshold)
                        #     if n_exceeded > 0:
                        #         self.ldebug(f"Reinjection detected for {st_name=} {metric=} {col=}")
                        #         fail_cnt += 1
                        #     if fail_cnt > self.max_diff_from_first_sample_count:
                        #         break
                        if fail_cnt > self.max_diff_from_first_sample_count:
                            self.logger.warning(f"Reinjection {fail_cnt=}/{self.max_diff_from_first_sample_count=} "
                                                f"exceeded for {st_name=} {metric=} {maxdiff=} | not "
                                                f"processing")
                            continue

                    # Check if all values are above the threshold to detect no beam
                    if self.no_beam_threshold is not None:
                        n_below_threshold = np.sum(np.median(mat, axis=0) < self.no_beam_threshold)
                        if n_below_threshold > self.no_beam_count:
                            self.logger.warning(f"No beam detected for {st_name=} {metric=} - {n_below_threshold=} "
                                                f"{self.no_beam_threshold=}")
                            continue

                    lts = compute_lifetime_exponential_v2(times, mat)

                    # df = pd.DataFrame(lts[None, :], columns=streamer.keys, index=[time.time()])
                    # self.results[k][sector].append(df)
                    individual_raw = {streamer.keys[i]: lts[i] for i in range(len(streamer.keys))}
                    # median_lt = np.median(lts)
                    individual = {}
                    if self.lower_limit is not None:
                        for k, v in individual_raw.items():
                            individual[k] = max(v, self.lower_limit)
                    else:
                        individual = individual_raw

                    if self.upper_limit is not None:
                        for k, v in individual.items():
                            individual[k] = min(v, self.upper_limit)

                    updates[metric] = {
                        "timestamp": time.time(),
                        "raw": individual,
                    }
                    if self.add_msum_field:
                        updates[metric]["msum"] = {streamer.keys[i]: np.mean(mat, axis=0)[i] for i in range(len(streamer.keys))}
                    self.result_combined[metric].update(updates[metric])
                    self.ldebug(
                            f"LTCB trig [{st_name=}] [{metric=}]: {mat.shape=} @ " f"{updates[metric]['timestamp']}"
                    )
                else:
                    self.ldebug(f"LTCB trig [{st_name=}] [{metric=}]: NO DATA")
        self.result_last = updates

        self.counter += 1
        self.ldebug(f"LTCB {cnt=} result [{st_name=}] = {self.result_last}")
        # return self.result_combined
        return self.result_last


class ScalarLifetimeCallback(LifetimeCallback):
    add_msum_field = False
    def __call__(self, streamer, data: dict, st_name: str, trig_counter: int = -1):
        from pybeamtools.physics.lifetime import compute_lifetime_exponential_v2

        cnt = self.counter
        updates = {}

        # if self.debug:
        #    print(f"Processing S{sector} {cnt=} from {streamer=}")
        for metric, metric_config in self.lifetime_processors.items():
            trig_cnt, frame_cnt = metric_config
            if cnt > 0 and cnt % trig_cnt == 0:
                mat, times, tags = streamer.get_latest_buffers(frame_cnt)
                if mat is not None:
                    mat = mat.astype(np.float64)

                    # Check first vs later samples to detect reinjection
                    if self.max_diff_from_first_sample_threshold is not None:
                        diff = mat[1:, :] - mat[0:1, :]
                        maxdiff = np.max(diff, axis=0)
                        n_exceeded = np.sum(diff > self.max_diff_from_first_sample_threshold, axis=0)
                        fail_cnt = np.sum(n_exceeded > 0)
                        if fail_cnt > self.max_diff_from_first_sample_count:
                            self.logger.warning(f"Reinjection {fail_cnt=}/{self.max_diff_from_first_sample_count=} "
                                                f"exceeded for {st_name=} {metric=} {maxdiff=} | not "
                                                f"processing")
                            continue

                    # Check if all values are above the threshold to detect no beam
                    if self.no_beam_threshold is not None:
                        n_below_threshold = np.sum(np.median(mat, axis=0) < self.no_beam_threshold)
                        if n_below_threshold > self.no_beam_count:
                            self.logger.warning(f"No beam detected for {st_name=} {metric=} - {n_below_threshold=} "
                                                f"{self.no_beam_threshold=}")
                            continue

                    lts = compute_lifetime_exponential_v2(times, mat, clip_min=1e-6, inplace=True)

                    # df = pd.DataFrame(lts[None, :], columns=streamer.keys, index=[time.time()])
                    # self.results[k][sector].append(df)
                    individual_raw = {streamer.keys[i]: lts[i] for i in range(len(streamer.keys))}
                    # median_lt = np.median(lts)
                    individual = {}
                    if self.lower_limit is not None:
                        for k, v in individual_raw.items():
                            individual[k] = max(v, self.lower_limit)
                    else:
                        individual = individual_raw

                    if self.upper_limit is not None:
                        for k, v in individual.items():
                            individual[k] = min(v, self.upper_limit)

                    updates[metric] = {
                        "timestamp": time.time(),
                        "raw": individual,
                    }
                    if self.add_msum_field:
                        updates[metric]["msum"] = {streamer.keys[i]: np.mean(mat, axis=0)[i] for i in range(len(streamer.keys))}
                    self.result_combined[metric].update(updates[metric])
                    self.ldebug(
                            f"LTCB trig [{st_name=}] [{metric=}]: {mat.shape=} @ " f"{updates[metric]['timestamp']}"
                    )
                else:
                    self.ldebug(f"LTCB trig [{st_name=}] [{metric=}]: NO DATA")
        self.result_last = updates

        self.counter += 1
        self.ldebug(f"LTCB {cnt=} result [{st_name=}] = {self.result_last}")
        # return self.result_combined
        return self.result_last

    # def __call__(self, streamer, data: dict, st_name: str, trig_counter: int = -1):
    #     from pybeamtools.physics.lifetime import compute_lifetime_exponential_v2
    #
    #     cnt = self.counter
    #     updates = {}
    #
    #     for metric, metric_config in self.lifetime_processors.items():
    #         trigcnt, avgcnt = metric_config
    #         if cnt > 0 and cnt % trigcnt == 0:
    #             values, times, tags = streamer.get_latest_buffers(avgcnt)
    #             if values is not None:
    #                 if values.ndim != 1:
    #                     raise ValueError(f'Expected 1D array, got {values=}')
    #                 values = values.clip(1e-6, None)
    #                 mat = values[:, None]
    #
    #                 # Check first vs later samples to detect reinjection
    #                 if self.max_diff_from_first_sample_threshold is not None:
    #                     diff = mat[1:, :] - mat[0:1, :]
    #                     maxdiff = np.max(diff, axis=0)
    #                     n_exceeded = np.sum(diff > self.max_diff_from_first_sample_threshold, axis=0)
    #                     fail_cnt = np.sum(n_exceeded > 0)
    #                     if fail_cnt > self.max_diff_from_first_sample_count:
    #                         self.logger.warning(f"Reinjection {fail_cnt=}/{self.max_diff_from_first_sample_count=} "
    #                                             f"exceeded for {st_name=} {metric=} {maxdiff=} | not "
    #                                             f"processing")
    #                         continue
    #
    #                 # Check if all values are above the threshold to detect no beam
    #                 if self.no_beam_threshold is not None:
    #                     n_below_threshold = np.sum(np.median(mat, axis=0) < self.no_beam_threshold)
    #                     if n_below_threshold > self.no_beam_count:
    #                         self.logger.warning(f"No beam detected for {st_name=} {metric=} - {n_below_threshold=} "
    #                                             f"{self.no_beam_threshold=}")
    #                         continue
    #
    #                 lts = compute_lifetime_exponential_v2(times, mat)
    #                 assert len(lts) == 1, f'BAD LIFETIME {lts=} {mat.shape=} {times.shape=} {tags=}'
    #                 individual = lts[0]
    #                 if not np.isfinite(individual):
    #                     individual = 0.0
    #                 if self.lower_limit is not None:
    #                     individual = max(individual, self.lower_limit)
    #                 updates[metric] = {
    #                     "timestamp": time.time(),
    #                     "raw": individual,
    #                     #"msum": {streamer.keys[i]: np.mean(mat, axis=0)[i] for i in range(len(streamer.keys))}
    #                 }
    #                 self.result_combined[metric].update(updates[metric])
    #                 self.ldebug(
    #                         f"LTCB trig [{st_name=}] [{metric=}]: {values.shape=} @ " f"{updates[metric]['timestamp']}"
    #                 )
    #             else:
    #                 self.ldebug(f"LTCB trig [{st_name=}] [{metric=}]: NO DATA")
    #     self.result_last = updates
    #
    #     self.counter += 1
    #     self.ldebug(f"LTCB {cnt=} result [{st_name=}] = {self.result_last}")
    #     return self.result_last
