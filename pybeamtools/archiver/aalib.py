import tqdm.asyncio
import concurrent.futures
import requests
from datetime import datetime
import numpy as np
import pytz

AA_URL = "http://localhost:17665/mgmt/bpl"
DATA_URL = "http://localhost:17668/retrieval"


def split_list(l: list, n: int):
    return [l[i : i + n] for i in range(0, len(l), n)]


def chunker(seq, size):
    return (seq[pos : pos + size] for pos in range(0, len(seq), size))


def run_many_calls(func, arg_lists, maxcon, use_tqdm=False):
    maxcon = maxcon
    out = []

    def exec_func(args):
        return func(*args)

    import nest_asyncio

    nest_asyncio.apply()
    with concurrent.futures.ThreadPoolExecutor(max_workers=maxcon) as executor:
        futures = (executor.submit(exec_func, a) for a in arg_lists)
        # print([f for f in futures if not isinstance(f,asyncio.Future)])
        if use_tqdm:
            for future in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(arg_lists)):
                try:
                    data = future.result()
                    out.append(data)
                except Exception as exc:
                    raise exc
        else:
            for future in concurrent.futures.as_completed(futures):
                try:
                    data = future.result()
                    out.append(data)
                except Exception as exc:
                    raise exc
    return out


def convert_events_to_plot(x_array, y_array):
    j = 0
    xnew, ynew = np.zeros(len(x_array) * 2 - 1), np.zeros(len(x_array) * 2 - 1)
    xlast = ylast = None
    for x, y in zip(x_array, y_array):
        if j == 0:
            pass
        else:
            xnew[j], ynew[j] = x, ylast
            j += 1
        xnew[j], ynew[j] = x, y
        xlast, ylast = x, y
        j += 1
        # print(j,len(x_array)*2-2)
    assert j == len(x_array) * 2 - 1
    return xnew, ynew


class AAClient:
    CONNECTIONS = 5
    TIMEOUT = 10

    def __init__(self, aa_url=None, data_url=None):
        self.aa_url = aa_url or AA_URL
        self.data_url = data_url or DATA_URL

        self.s = s = requests.Session()
        s.trust_env = False
        s.verify = False

    def get_many_urls(self, urls):
        out = []

        def load_url(url, timeout):
            ans = self.s.get(url, timeout=timeout)
            return ans.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.CONNECTIONS) as executor:
            future_to_url = (executor.submit(load_url, url, self.TIMEOUT) for url in urls)
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)
        return out

    # def load_url(url, timeout):
    #     ans = requests.head(url, timeout=timeout)
    #     return ans.status_code

    def generic_bpl_request(self, bplURL=None, path=None, debug=False, emptyok=False, timeout=180, **kwargs):
        assert path is not None
        bplURL = bplURL or AA_URL
        url = bplURL + f"/{path}"
        if len(kwargs) > 0:
            resp = self.s.get(url, params=kwargs, timeout=timeout)
        else:
            resp = self.s.get(url, timeout=timeout)
        if debug:
            print("Url: {}".format(resp.url))
        resp.raise_for_status()
        try:
            # try:
            return resp.json()
        # except:
        #     #print(f'Backup parsing attempt of {resp.status_code=} {resp.text=}')
        #     return json.loads(resp.text.strip())
        except ValueError as e:
            if resp.text == "" and emptyok:
                return None
            print(f"URL {resp.url}: empty response {resp.text=}!")
            print(e)
            return None

    def generic_bpl_post(self, bplURL=None, path=None, data=None, debug=False, **kwargs):
        assert path is not None
        bplURL = bplURL or AA_URL
        url = bplURL + f"/{path}"
        if len(kwargs) > 0:
            resp = self.s.post(url, data=data, params=kwargs)
        else:
            resp = self.s.post(url, data=data)
        if debug:
            print("Url: {} | data {}".format(resp.url, data))
        resp.raise_for_status()
        return resp.json()

    def generic_bpl_post_json(self, bplURL=None, path=None, json=None, debug=False, **kwargs):
        assert path is not None
        bplURL = bplURL or AA_URL
        url = bplURL + f"/{path}"
        if len(kwargs) > 0:
            resp = self.s.post(url, json=json, params=kwargs, timeout=(1, 300))
        else:
            resp = self.s.post(url, json=json, timeout=(1, 300))
        if debug:
            print(f"Url: {resp.url} | json {json} | resp {resp.text}")
        if resp.status_code != 200:
            print(resp.url)
            print(json)
            print(resp.text)
            resp.raise_for_status()
        try:
            rr = resp.json()
            return rr
        except:
            print(f"FAILED TO DECODE JSON RESPONSE {resp}:")
            print(resp.text)
            raise

    def getAllExpandedPVNames(self, debug=False):
        return self.generic_bpl_request(path="getAllExpandedPVNames", debug=debug)

    def modifyMetaFields(self, pv, command, debug=False):
        # Access using: http://mgmt_url/bpl/modifyMetaFields - Modify the fields (HIHI, LOLO etc) being archived as part
        # of the PV. PV needs to be paused first. pv The real name of the pv. command A command is a verb followed by a
        # list of fields, all of them comma separated. Possible verbs are add, remove and clear. For example add,ADEL,
        # MDEL will add the fields ADEL and MDEL if they are not already present. clear clears all the fields. You can
        # have any number of commands.
        assert command.split(",")[0] in ["add", "remove", "clear"]
        return self.generic_bpl_request(path="modifyMetaFields", debug=debug, pv=pv, command=command)

    def getAllPVs(self, limit=-1, debug=False):
        return self.generic_bpl_request(path="getAllPVs", debug=debug, limit=limit)

    def getPausedPVsReport(self, debug=False):
        return self.generic_bpl_request(path="getPausedPVsReport", debug=debug)

    def getPausedPVs(self, debug=False):
        data = self.generic_bpl_request(path="getPausedPVsReport", debug=debug)
        return [x["pvName"] for x in data]

    def getPVStatus(self, pv_list: list[str], debug=False):
        # Get the status of a PV. pv The name(s) of the pv for which status is to be determined. If a pv is not being
        # archived, you should get back a simple JSON object with a status string of "Not being archived." You can
        # also pass in GLOB wildcards here and multiple PVs as a comma separated list. If you have more PVs that can
        # fit in a GET, send the pv's as a CSV pv=pv1,pv2,pv3 as the body of a POST.

        """
        Return example:
        {
            "lastRotateLogs": "Never",
            "pvName": "S01A:FH1:PS:MeasCurrentM",
            "connectionState": "true",
            "lastEvent": "Oct/07/2024 18:38:10 CDT",
            "samplingPeriod": "0.03",
            "isMonitored": "true",
            "connectionLastRestablished": "Never",
            "connectionFirstEstablished": "Oct/07/2024 13:38:18 CDT",
            "connectionLossRegainCount": "0",
            "status": "Being archived",
            "appliance": "appliance0",
            "pvNameOnly": "S01A:FH1:PS:MeasCurrentM"
          }
        """
        if isinstance(pv_list, str):
            pv_list = [pv_list]
        assert len(pv_list) < 100, f'Bad pv list length: {len(pv_list)} too long'
        return self.generic_bpl_request(path="getPVStatus", debug=debug, pv=",".join(pv_list))

    def consolidatePVData(self, pv, storage, debug=False, timeout=360):
        # Consolidate the data for this PV until the specified store. The PV needs to be paused first. pv The name of
        # the pv. storage The name of the store until which we'll consolidate data. This is typically a string like
        # STS or MTS. To get a list of names of stores for a PV, please see /getStoresForPV
        return self.generic_bpl_request(
            path="consolidateDataForPV", debug=debug, pv=pv, timeout=timeout, storage=storage
        )

    def getStoresForPV(self, pv, debug=False):
        # Gets the names and definitions of the data stores for this PV. Every store in a PV's typeinfo is expected
        # to have a name - this is typically "name=STS" or something similar. This call returns the names of all the
        # stores for a PV with their URI representations as a dictionary. pv The name of the pv.
        return self.generic_bpl_request(path="getStoresForPV", debug=debug, pv=pv)

    def modifyStoreURLForPV(self, pv, storage, plugin_url, debug=False):
        # http://mgmt_url/bpl/modifyStoreURLForPV - Changes the store for this particular PV. Note this only changes
        # the PVTypeInfo; it does not change any data/files so one could lose data using this call. pv The name of
        # the pv storage The name of the store to change ( for example, MTS ) plugin_url The new URL specification
        # for this store; this is what you would have used in the policy file and is something that can be understood
        # by StoragePluginURLParser.
        return self.generic_bpl_request(
            path="modifyStoreURLForPV", debug=debug, pv=pv, storage=storage, plugin_url=plugin_url
        )

    def putPVTypeInfo(self, pv, typeinfo_dict, override=False, createnew=False, debug=False):
        # Access using: http://mgmt_url/bpl/putPVTypeInfo - Updates the typeinfo for the specified PV. Note this
        # merely updates the typeInfo. It does not have any logic to react to changes in the typeinfo. That is,
        # don't assume that the PV is automatically paused just because you changed the isPaused to true. This is
        # meant to be used in conjuction with other BPL to implement site-specific BPL in external code (for example,
        # python). This can also be used to add PVTypeInfo's into the system; support for this is experimental. The
        # new PVTypeInfo's are automatically paused before adding into the system. Logically, you have to specify at
        # least one of override or createnew. pv The name of the pv. override If the PVTypeInfo for this PV already
        # exists, do you want to update it or return an error? By default, this is false. createnew If the PVTypeInfo
        # for this PV does not exist, do you want to create a new one or return an error? By default, this is false.
        assert isinstance(pv, str) and 1 <= len(pv) <= 70, f"Bad pv name: {pv}"
        assert isinstance(typeinfo_dict, dict)
        return self.generic_bpl_post_json(
            path="putPVTypeInfo", debug=debug, pv=pv, json=typeinfo_dict, override=override, createnew=createnew
        )

    def getPVTypeInfo(self, pv, debug=False):
        # Access using: http://mgmt_url/bpl/getPVTypeInfo - Get the type info for a given PV. In the archiver
        # appliance terminology, the PVTypeInfo contains the various archiving parameters for a PV. pv The name of
        # the pv.
        return self.generic_bpl_request(path="getPVTypeInfo", debug=debug, pv=pv)

    def getMetaGets(self, debug=False):
        return self.generic_bpl_request(path="getMetaGets", debug=debug)

    def removeAlias(self, pv, aliasname, debug=False):
        # Access using: http://mgmt_url/bpl/removeAlias - Remove an alias for the specified PV. This is only
        # supported for PVs who have completed their archive PV workflow. pv The real name of the pv. aliasname The
        # alias name of the pv.
        return self.generic_bpl_request(path="removeAlias", debug=debug, pv=pv, aliasname=aliasname)

    def getAllAliases(self, debug=False):
        # Access using: http://mgmt_url/bpl/getAllAliases - Get all the aliases in the cluster and the PV's they are
        # mapped to.
        return self.generic_bpl_request(path="getAllAliases", debug=debug)

    def changeArchivalParams(self, pv, samplingperiod, samplingmethod, debug=False):
        # Access using: http://mgmt_url/bpl/changeArchivalParameters - Change the archival parameters for a PV.
        # pv The name of the pv.
        # samplingperiod The new sampling period in seconds.
        # samplingmethod The new sampling method For now, this is one of SCAN or MONITOR.
        assert samplingmethod in ["SCAN", "MONITOR"]
        assert isinstance(samplingperiod, str)
        return self.generic_bpl_request(
            path="changeArchivalParameters",
            debug=debug,
            pv=pv,
            samplingperiod=samplingperiod,
            samplingmethod=samplingmethod,
            emptyok=True,
        )

    def pausePVs(self, pv_list, debug=False, split=20000):
        chunks = split_list(pv_list, split)
        responses = []
        for c in chunks:
            responses.extend(self.generic_bpl_post(path="pauseArchivingPV", debug=debug, data={"pv": ",".join(c)}))
        return responses

    def resumePVs(self, pv_list, debug=False, split=20000):
        chunks = split_list(pv_list, split)
        responses = []
        for c in chunks:
            responses.extend(self.generic_bpl_post(path="resumeArchivingPV", debug=debug, data={"pv": ",".join(c)}))
        return responses

        # data={'pv':','.join(pv_list)}
        # return generic_bpl_post(path='resumeArchivingPV', debug=debug, data=data)

    def deletePV(self, pv, deletedata=False, debug=False):
        return self.generic_bpl_request(path="deletePV", deleteData=deletedata, debug=debug, pv=pv)

    def abortArchivingPV(self, pv, debug=False):
        return self.generic_bpl_request(path="abortArchivingPV", debug=debug, pv=pv)

    def archivePV(self, pv_params_list, debug=False):
        assert isinstance(pv_params_list, list)
        for el in pv_params_list:
            assert isinstance(el, dict)
            assert set(el.keys()).issubset({"pv", "samplingperiod", "samplingmethod"})
        return self.generic_bpl_post_json(path="archivePV", debug=debug, json=pv_params_list)

    def archivePVSimple(self, pv_list, debug=False):
        assert isinstance(pv_list, list)
        pvd = []
        for el in pv_list:
            pvd.append({"pv": el})
        return self.generic_bpl_post_json(path="archivePV", debug=debug, json=pvd)

    # def archivePV(bplURL, pvParams, debug=False):
    #     bplURL = bplURL or AA_URL
    #     url = bplURL + '/archivePV'
    #     assert isinstance(pvParams, list)
    #     for el in pvParams:
    #         assert isinstance(el, dict)
    #         assert set(el.keys()).issubset({'pv','samplingperiod','samplingmethod'})
    #     headers = {'Content-type': 'application/json'}
    #     resp = s.post(url, json=pvParams, headers=headers)
    #     if debug: print('Url: {}'.format(resp.url))
    #     resp.raise_for_status()
    #     return resp # if debug else resp.json()['status']

    def getData(self, pv, start, stop, debug=False):
        url = DATA_URL + "/data/getData.json"
        tstart = start.isoformat().replace("+00:00", "Z")
        tstop = stop.isoformat().replace("+00:00", "Z")
        resp = self.s.get(url, params={"pv": pv, "from": tstart, "to": tstop}, timeout=(0.5, 10))
        if debug:
            print("Url: {}".format(resp.url))
        resp.raise_for_status()
        return resp.json()

    def getDataJSON(self, dataURL, pvParams, debug=False, headers=None):
        dataURL = dataURL or DATA_URL
        headers = headers or {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
        }
        url = dataURL + "/data/getData.json"
        resp = self.s.get(url, params=pvParams, timeout=(0.5, 10), headers=headers)
        if debug:
            print("Url: {}".format(resp.url))
        resp.raise_for_status()
        return resp.json()

    def get_data(
        self,
        pv: str,
        start: datetime,
        end: datetime,
        cut_x=True,
        offset_to_start=True,
        as_datetime=False,
        convert_events=False,
        debug=False,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Get data from AA in a format suitable for plotting

        cut_x: remove events before start
        offset_to_start: subtract start timestamp from x values
        as_datetime: instead of floats, return datetimes on x axis
        convert_events: add 'phantom' points in betwen events to plot lines like a staircase, in same style as CSS.

        :return: time and data numpy arrays
        """
        local_tz = pytz.timezone("America/Chicago")
        start = start.astimezone(pytz.utc)
        end = end.astimezone(pytz.utc)
        try:
            jdata = self.getDataJSON(
                DATA_URL,
                {
                    "pv": pv,
                    "from": start.isoformat().replace("+00:00", "Z"),
                    "to": end.isoformat().replace("+00:00", "Z"),
                },
                debug=debug,
            )
            if len(jdata) == 0:
                return None
            elif len(jdata) > 1:
                raise Exception(f"PV {pv} returned multiple json results???")
            jdata = jdata[0]
        except Exception as ex:
            print(f"Failed {pv}")
            raise ex
        values = np.array([v["val"] for v in jdata["data"]])
        times = np.array([v["secs"] + v["nanos"] / 1.0e9 for v in jdata["data"]])
        del jdata
        if cut_x:
            mask = (times > start.timestamp()) & (times < end.timestamp())
            values = values[mask]
            times = times[mask]
        if as_datetime:
            times = np.array(
                [datetime.utcfromtimestamp(t).replace(tzinfo=pytz.utc).astimezone(local_tz) for t in times]
            )
            if offset_to_start:
                times -= start
        else:
            if offset_to_start:
                times -= start.timestamp()
            if convert_events:
                times, values = convert_events_to_plot(times, values)
        return times, values

    # def raw_data_url(self, url: str):
    #     return self.getDataJSON(url, headers={'Accept': 'application/json, text/javascript, */*; q=0.01',
    #                                           'Accept-Encoding': 'gzip, deflate'
    #                                           })
