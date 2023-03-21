import datetime
import time
from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd
import pytz

APS_TZ = pytz.timezone('America/Chicago')
SNAPSHOT_DIR = Path('/home/helios/oagData/SCR/snapshots')
REQUEST_PATH = Path('/home/helios/oagData/SCR/requestFiles')
SCR_CATEGORIES = ['LPL', 'LTS', 'PAR', 'PARBPM', 'Booster', 'SR']


def find_scr_files(categories: Union[str, List[str]], start: datetime.datetime, end: datetime.datetime) -> List[Path]:
    assert isinstance(start, datetime.datetime)
    assert isinstance(end, datetime.datetime)
    if isinstance(categories, str):
        categories = [categories]
    for c in categories:
        assert c in SCR_CATEGORIES

    local_start = APS_TZ.localize(start)
    local_end = APS_TZ.localize(end)

    all_saves = []
    for c in categories:
        p = SNAPSHOT_DIR / c
        valid_saves = list(p.glob(f'{c}2*.gz'))
        # print(valid_saves[:5])
        if len(valid_saves) == 0:
            continue

        format_string = f'{c}%Y-%j-%m%d-%H%M%S'
        dates = [APS_TZ.localize(datetime.datetime.strptime(str(s.name).split('.', 1)[0], format_string)) for s in
                 valid_saves]
        timestamps = np.array([d.timestamp() for d in dates])
        # print(dates[:5], timestamps[:5])

        mask = (timestamps > local_start.timestamp()) & (timestamps < local_end.timestamp())
        masked_saves = [v for v, m in zip(valid_saves, mask) if m]

        print(f'Cat {c} - found {len(masked_saves)} matching saves from {local_start} to {local_end}')
        # print(masked_saves[:5])
        all_saves += masked_saves
    return all_saves


def get_scr_request_file(c):
    assert c in SCR_CATEGORIES
    p = REQUEST_PATH / (c + '.req')
    assert p.is_file(), f'category {c} path {str(p)} does not exist???'
    return p


def get_scr_request_df(c):
    import pysdds
    p = get_scr_request_file(c)
    sdds = pysdds.read(p)
    assert sdds.n_pages == 1
    return sdds.columns_to_df(0)


def get_scr_controlname_list(c):
    import pysdds
    p = get_scr_request_file(c)
    sdds = pysdds.read(p)
    pvs = sdds.columns_dict['ControlName'].data[0]
    print(f'Found {len(pvs)} controls for {c} at {str(p)}')
    return list(pvs)


def save_scr(categories, path=None, timeout=5.0):
    import caproto
    from caproto.threading.client import Context, PV

    if isinstance(categories, str):
        categories = [categories]
    for c in categories:
        assert c in SCR_CATEGORIES

    if path is None:
        filepath = None
    else:
        assert isinstance(path, Path)
        if path.is_dir():
            name = f'df_scr_{"_".join(categories)}_{datetime.datetime.now().isoformat()}.h5'
            print(f'Auto generated file name: {name}')
            filepath = path / name
        elif path.is_file():
            raise IOError(f'File {path} already exists')
        elif not path.parent.exists():
            raise IOError(f'Parent directory {path.parent} does not exist')
        else:
            filepath = path

    pvnames = []
    for c in categories:
        pvnames += get_scr_controlname_list(c)

    ctx = Context()
    pvs: List[PV] = ctx.get_pvs(*pvnames, priority=1, timeout=timeout)
    pvs_connected: List[PV] = []
    time.sleep(1.0)
    for pv in pvs:
        try:
            pv.wait_for_search(timeout=timeout)
            pv.wait_for_connection(timeout=timeout)
            pvs_connected.append(pv)
        except caproto.CaprotoTimeoutError:
            print(f'Failed to connect to {pv.name}')
    print(f'Connected to {len(pvs_connected)}')

    results = {}
    for pv in pvs_connected:
        try:
            r = pv.read(data_type='time', timeout=1)
            if r.status.success != 1:
                raise Exception
            results[pv.name] = r
        except caproto.CaprotoTimeoutError as ex:
            print(f'Failed to get {pv} - timeout')
    print(f'Got results for {len(results)}')

    df = pd.DataFrame(index=pvnames)
    df['ControlName'] = pvnames
    df['value'] = np.nan
    df['timestamp'] = np.nan
    df['code'] = np.nan
    for k, v in results.items():
        df.loc[k, 'value'] = v.data[0]
        df.loc[k, 'timestamp'] = r.metadata.timestamp
        df.loc[k, 'code'] = r.status.code

    print(f'SCR of {categories} done')
    if filepath is not None:
        df.to_hdf(filepath)
    return df


