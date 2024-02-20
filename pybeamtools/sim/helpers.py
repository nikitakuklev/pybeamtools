def read_fresh(self, pvs_read, timeout=1.0, now=None, min_readings=1, max_readings=None,
               reduce='mean', include_timestamps=False, use_buffer=True
               ):
    """ Read next PV update or timeout """
    if now is None:
        now = time.time()  # Assume roughly synced with IOC
    t_start = time.perf_counter()
    assert min_readings is not None and min_readings >= 1
    assert max_readings is None or max_readings >= min_readings
    if max_readings is None:
        max_readings = min_readings
    if not isinstance(pvs_read, list):
        pvs_read = [pvs_read]
    values = [None] * len(pvs_read)
    for i, pv in enumerate(pvs_read):
        if use_buffer:
            responses = self.get_buffer_data(pv.name, start=now)
        else:
            responses = []
        if max_readings is not None and len(responses) > max_readings:
            responses = responses[-max_readings:]
        # print(f'PV {pv.name}: got {len(responses)} buffered responses of {min_readings}')
        while len(responses) < min_readings:
            r = pv.read(data_type='time', timeout=timeout)
            if r.metadata.timestamp > now:
                if len(responses) > 0:
                    if responses[-1].metadata.timestamp == r.metadata.timestamp:
                        # print(f'PV {pv.name}: stale read at ts {r.metadata.timestamp}')
                        pass
                    else:
                        assert r.status.success == 1
                        responses.append(r)
                        # print(f'PV {pv.name}: fresh read {r.data} at ts {r.metadata.timestamp} ({len(responses)} of {min_readings})')
                else:
                    assert r.status.success == 1
                    responses.append(r)
            if time.perf_counter() - t_start > timeout:
                raise Exception(
                        f'PV {pv.name} read timed out at {time.time()} (record time {r.metadata.timestamp})')
            # print(f'Continuing PV read {pv.name} at {time.time()} (record time {r.metadata.timestamp})')
            time.sleep(0.01)

        data = np.vstack([r.data for r in responses])
        timestamps = np.vstack([r.metadata.timestamp for r in responses])
        if reduce == 'mean':
            value = np.mean(data, axis=0)
            timestamp = np.mean(timestamps, axis=0)
        elif reduce == 'median':
            value = np.median(data, axis=0)
            timestamp = np.median(timestamps, axis=0)
        elif reduce is None:
            value = data
            timestamp = timestamps
        else:
            raise Exception(f'{reduce=} ???')
        if include_timestamps:
            values[i] = (timestamp, value)
        else:
            values[i] = value
    return values

def set_and_verify_multiple(self, pvdict, timeout=1.0, readback_kwargs=None,
                            readback_delay_min=None,
                            readback_delay_max=None
                            ):
    """ Set PVs and verify readbacks if available """
    from caproto.threading.client import Batch
    kv = self.kv
    df = self.df
    readback_delay_min = readback_delay_min or self.DELAY_AFTER_WRITE
    readback_delay_max = readback_delay_max or self.READBACK_OK_TIMEOUT
    assert self.df is not None
    readback_kwargs = readback_kwargs or dict(min_readings=1)
    assert all(k in df.index for k in pvdict.keys())
    t_start = time.perf_counter()
    for (pvn, value) in pvdict.items():
        pv_input = kv[pvn]
        pv_read = df.loc[pv_input.name, 'pv_readback']
        low = df.loc[pv_input.name, 'low']
        high = df.loc[pv_input.name, 'high']
        atol = df.loc[pv_input.name, 'atol']
        if np.isnan(atol):
            raise Exception(f'Please provide tolerance for {pvn}')
        assert not np.isnan(low) and not np.isnan(high)
        assert low <= value <= high, f'PV {pv_input} value {value} outside {low}<->{high}'
        assert atol < np.abs(
                high - low), f'PV {pv_input} tolerance {atol} larger than limit range {low}<->{high}'
        # val = pv_read.read().data[0]
        # if np.isclose(val, value, atol=atol, rtol=0):
        #     #del pvdict[pvn]
        #     pass

    with Batch(timeout=timeout) as b:
        for (pvn, value) in pvdict.items():
            pv_input = self.kv[pvn]
            r = b.write(pv_input, value)
            # assert r.status.success == 1

    time.sleep(readback_delay_min)
    now = time.time()
    values = {}
    last_read = {}
    while len(values) < len(pvdict):
        # print(f'set outer loop {len(values)=}')
        for (pvn, value) in pvdict.items():
            if pvn in values:
                continue
            # print(f'set loop {pvn=}')
            pv_input = self.kv[pvn]
            pv_read = df.loc[pv_input.name, 'pv_readback']
            if pv_read is None:
                continue
            atol = df.loc[pv_input.name, 'atol']
            val = self.read_fresh(pv_read, timeout=timeout, now=now, **readback_kwargs)[0]
            last_read[pvn] = val
            if np.all(np.isclose(val, value, atol=atol, rtol=0)):
                values[pvn] = val
        # print(f'set outer loop 2 {len(values)=} {last_read=}')
        if time.perf_counter() - t_start > readback_delay_max:
            for (pvnl, valuel) in pvdict.items():
                pv_inputl = self.kv[pvnl]
                atoll = df.loc[pv_inputl.name, 'atol']
                print(
                        f'{pvnl:20}: {valuel=} {last_read[pvnl]=} {(valuel - last_read[pvnl])=} {atoll=}')
            raise IOError(
                    f'Setting {pv_input.name} failed - readback {pv_read.name} ({val}) bad (want {value})')
        time.sleep(0.1)

    t_spent = time.perf_counter() - t_start
    if self.READBACK_TOTAL_SET_TIME_MIN is not None:
        t_sleep = max(self.DELAY_AFTER_RB, self.READBACK_TOTAL_SET_TIME_MIN - t_spent)
        time.sleep(t_sleep)
    return values


def set_and_verify(self, pv_write, value, timeout=1.0):
    """ Set PV and verify readback is within tolerance """
    self.set_and_verify_multiple(dict(pv_write=value))


