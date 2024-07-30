import os
from typing import Iterable

# print(os.environ.get('EPICS_PVA_ADDR_LIST', None))
# os.environ[
#     'EPICS_PVA_ADDR_LIST'] = 'c2ioc02.aps4.anl.gov pslmcam1.aps4.anl.gov pslmcam2.aps4.anl.gov bslmcam1.aps4.anl.gov  daq-dss02.aps4.anl.gov daq-dss04.aps4.anl.gov daq-dss06.aps4.anl.gov daq-dss08.aps4.anl.gov daq-dss10.aps4.anl.gov daq-dss11.aps4.anl.gov daq-dss14.aps4.anl.gov daq-dss16.aps4.anl.gov daq-dss18.aps4.anl.gov daq-dss20.aps4.anl.gov daq-dss21.aps4.anl.gov daq-dss24.aps4.anl.gov daq-dss26.aps4.anl.gov daq-dss28.aps4.anl.gov daq-dss30.aps4.anl.gov daq-dss31.aps4.anl.gov daq-dss34.aps4.anl.gov daq-dss36.aps4.anl.gov daq-dss37.aps4.anl.gov daq-dss40.aps4.anl.gov daq-qss02.aps4.anl.gov daq-qss11.aps4.anl.gov daq-qss21.aps4.anl.gov daq-qss31.aps4.anl.gov llrf-amc758-7.aps4.anl.gov rfdaqsrv-1.aps4.anl.gov'
# os.environ['EPICS_AR_PORT'] = '7002'

import time


def __std_new_ps(s, root):
    d = {'setpoint': f'{root}:PS:SetCurrentC',
         'readback': f'{root}:PS:MeasCurrentM',
         'external': f'{root}:DCCT:CurrentM',
         'voltage': f'{root}:PS:VoltageM',
         }
    if s is not None:
        d.update({
            'daqname': f'{root.replace(":", "").lower()}',
            'sector': s,
            'family': f'{root.split(":")[-1]}',
        })
    return d


def __ps_temp_1(root):
    return {
        'temp_buck': f'{root}:PS:BuckTempM',
        'temp_capacitor': f'{root}:PS:CapacitorTempM',
        'temp_magnet': f'{root}:TemperatureM',
        'temp_carrier': f'{root}:PS:CarrierTempM',
        'faults': f'{root}:PS:FaultsM',
        'water_leak': f'{root}:PS:WarningsM',
        'zero_setpoint': f'{root}:PS:ZeroSetpointM',
        'slew_ratem': f'{root}:PS:SlewRateM'
    }


def __ps_temp_2(root):
    return {
        'temp_buck': f'{root}:PS:CapacitorTempM',
        'temp_heatsink': f'{root}:PS:HeatSinkTempM',
        'temp_dampres': f'{root}:PS:DampResTempM',
        'fan1': f'{root}:PS:Fan1SpeedM',
        'fan2': f'{root}:PS:Fan2SpeedM',
    }


def __ps_temp_tdk(root):
    return {'temp_ambient': f'{root}:PS:AmbientTempM'}


def __ps_daq_source(root):
    sector = int(root[1:3])
    daqsector = sector - 1 if sector % 2 == 0 else sector
    daqsector = 40 if daqsector == -1 else daqsector
    return {'daq': f'S{daqsector:02d}-DAQPS', 'daqname': root.replace(':', '').lower()}


BTS_NEW_CORR_LIMIT = ncr = 15

BTS_CORRECTORS_H_SR = {}
for x in ['BTS:BH1', 'BTS:BH2']:
    BTS_CORRECTORS_H_SR[x] = {'setpoint': f'{x}:CurrentAO', 'readback': f'{x}:CurrentAI', 'limits': [-19, 19]}
for x in ['BTS:BSQ1H', 'BTS:BSQ5H', 'BTS:CQ1H', 'BTS:CQ3H', 'BTS:DQ1H']:
    BTS_CORRECTORS_H_SR[x] = {**__std_new_ps(None, x), **__ps_temp_2(x), 'limits': [-ncr, ncr]}

BTS_CORRECTORS_V_SR = {}
for x in ['BTS:BV1', 'BTS:BV2', 'BTS:BV3']:
    BTS_CORRECTORS_V_SR[x] = {'setpoint': f'{x}:CurrentAO', 'readback': f'{x}:CurrentAI', 'limits': [-19, 19]}
for x in ['BTS:BSQ2V', 'BTS:BSQ6V', 'BTS:CQ2V', 'BTS:DQ2V']:
    BTS_CORRECTORS_V_SR[x] = {**__std_new_ps(None, x), **__ps_temp_2(x), 'limits': [-ncr, ncr]}

BTS_CORRECTORS_SR = {**BTS_CORRECTORS_H_SR, **BTS_CORRECTORS_V_SR}

BTS_CORRECTORS_H_BOOSTER = {}
for x in ['BTS:AH1', 'BTS:AH2', 'BTS:AH3']:
    BTS_CORRECTORS_H_BOOSTER[x] = {'setpoint': f'{x}:CurrentAO', 'readback': f'{x}:CurrentAI', 'limits': [-5, 5]}

BTS_CORRECTORS_V_BOOSTER = {
    'BTS:AV1': {'setpoint': 'BTS:AV1:CurrentAO', 'readback': 'BTS:AV1:CurrentAI', 'limits': [-5, 5]},
    'BTS:AV2': {'setpoint': 'BTS:AV2:CurrentAO', 'readback': 'BTS:AV2:CurrentAI', 'limits': [-5, 5]},
    'BTS:AV3': {'setpoint': 'BTS:AV3:CurrentAO', 'readback': 'BTS:AV3:CurrentAI', 'limits': [-5, 5]},
}

BTS_CORRECTORS_BOOSTER = {**BTS_CORRECTORS_H_BOOSTER, **BTS_CORRECTORS_V_BOOSTER}

BTS_QUADS_BOOSTER = {
    'BTS:AQ1': {'setpoint': 'BTS:AQ1:PS:SetCurrentC', 'readback': 'BTS:AQ1:PS:SetCurrentM', 'limits': [0, 50]},
    'BTS:AQ2': {'setpoint': 'BTS:AQ2:PS:SetCurrentC', 'readback': 'BTS:AQ2:PS:SetCurrentM', 'limits': [0, 50]},
    'BTS:AQ3': {'setpoint': 'BTS:AQ3:PS:SetCurrentC', 'readback': 'BTS:AQ3:PS:SetCurrentM', 'limits': [0, 50]},
    'BTS:AQ4': {'setpoint': 'BTS:AQ4:PS:SetCurrentC', 'readback': 'BTS:AQ4:PS:SetCurrentM', 'limits': [0, 50]},
    'BTS:AQ5': {'setpoint': 'BTS:AQ5:PS:SetCurrentC', 'readback': 'BTS:AQ5:PS:SetCurrentM', 'limits': [0, 50]},
}

BTS_QUADS_SR = {
    'BTS:BQ1': {'setpoint': 'BTS:BQ1:PS:SetCurrentC', 'readback': 'BTS:BQ1:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:BQ2': {'setpoint': 'BTS:BQ2:PS:SetCurrentC', 'readback': 'BTS:BQ2:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:BQ3': {'setpoint': 'BTS:BQ3:PS:SetCurrentC', 'readback': 'BTS:BQ3:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:BQ4': {'setpoint': 'BTS:BQ4:PS:SetCurrentC', 'readback': 'BTS:BQ4:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:BQ5': {'setpoint': 'BTS:BQ5:PS:SetCurrentC', 'readback': 'BTS:BQ5:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:CQ1': {'setpoint': 'BTS:CQ1:PS:SetCurrentC', 'readback': 'BTS:CQ1:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:CQ2': {'setpoint': 'BTS:CQ2:PS:SetCurrentC', 'readback': 'BTS:CQ2:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:CQ3': {'setpoint': 'BTS:CQ3:PS:SetCurrentC', 'readback': 'BTS:CQ3:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:DQ1': {'setpoint': 'BTS:DQ1:PS:SetCurrentC', 'readback': 'BTS:DQ1:PS:SetCurrentM', 'limits': [0, 150]},
    'BTS:DQ2': {'setpoint': 'BTS:DQ2:PS:SetCurrentC', 'readback': 'BTS:DQ2:PS:SetCurrentM', 'limits': [0, 150]},
}

BTS_DIPOLES_BOOSTER = {
    'BTS:AB': {'setpoint': 'BTS:AB:CurrentAO', 'readback': 'BTS:AB:CurrentAI'},
}

BTS_BPMS = {
    'BTS:DPV1': {'sum': 'BTS:DPV1:SumM'},
    'BTS:DPV2': {'sum': 'BTS:DPV2:SumM'}
}

SR_SINGLE_PASS = {
    'S39CP0': {'sum': 'S39C:P0:sp.Sum'},
    'S40AP1': {'sum': 'S40A:P1:sp.Sum'},
    'S40AP0': {'sum': 'S40A:P0:sp.Sum'}
}

SR_BPMS = {}
for bpmnum, s in enumerate([40] + list(range(1, 40))):
    for j, (l, t) in enumerate([('A', f'P{i}') for i in range(0, 7)] + [('B', f'P{i}') for i in range(0, 7)]):
        root = 'S{i:02d}{l}:{t}'.format(i=s, l=l, t=t)
        if root == 'S39B:P1':
            root2 = 'S39C:P0'
        # if root == 'S39B:P1':
        #     root2 = 'S39B:P0'
        else:
            root2 = root
        SR_BPMS[root] = {'spx': f'{root2}:sp.X',
                         'spy': f'{root2}:sp.Y',
                         'spsum': f'{root2}:sp.Sum',
                         'orbitx': f'{root2}:x:SampledM',
                         'orbitx1s': f'{root2}:x:LowPass1sM',
                         'orbity': f'{root2}:y:SampledM',
                         'orbity1s': f'{root2}:y:LowPass1sM',
                         'orbiterrorx': f'{root2}:x:SampledErrorM',
                         'orbiterrory': f'{root2}:y:SampledErrorM',
                         'sa_x_mean': f'{root2}:stat:sa:x_mean',
                         'sa_y_mean': f'{root2}:stat:sa:y_mean',
                         'sa_x_std': f'{root2}:stat:sa:x_std',
                         'sa_y_std': f'{root2}:stat:sa:y_std',
                         'sa_x': f'{root2}:sa.X',
                         'sa_y': f'{root2}:sa.Y',
                         'sa_sum': f'{root2}:sa.Sum',
                         'sa_va': f'{root2}:sa.Va',
                         'sa_vb': f'{root2}:sa.Vb',
                         'sa_vc': f'{root2}:sa.Vc',
                         'sa_vd': f'{root2}:sa.Vd',
                         'off_x_sp': f'{root2}:off_x_sp',
                         'off_y_sp': f'{root2}:off_y_sp',
                         'maxadc': f'{root2}:maxadc',
                         'attenuation': f'{root2}:agc:att_mon',
                         'power_level': f'{root2}:agc:power_level_sp',
                         'power_level_mon': f'{root2}:agc:power_level_mon',
                         'agc': f'{root2}:agc:enabled_sp',
                         'agc_mon': f'{root2}:agc:enabled_mon',
                         'id': bpmnum * 12 + j,
                         'sector': s,
                         'family': t,
                         'real_bpm': root2
                         }
        daqsector = s - 1 if s % 2 == 0 else s
        if t.lower in ['bp5, bp6']:
            daqsector -= 1
        if root == 'S39B:P1':
            SR_BPMS[root]['daqname'] = 's{i:02d}{l}{t}'.format(i=39, l='c', t='p0')
        else:
            SR_BPMS[root]['daqname'] = 's{i:02d}{l}{t}'.format(i=s, l=l.lower(), t=t.lower())

SR_BPMS_DAQ_TO_NAME = {v['daqname']: x for x, v in SR_BPMS.items()}
SR_BPMS_DAQ_TO_ID = {v['id']: x for x, v in SR_BPMS.items()}
# S01A:P0 - no BPM
# S34A:P5 - Stored Beam Monitor
# S36A:P5 - Stored Beam Monitor
# S36B:P0 - no BPM
# S37B:P0 - no BPM
# S38B:P3 - TFB
# S38B:P0 - LFB & Libera rack (will it be connected?)
# S39A:P0 - TFB
# S39A:P2 - TFB
# S39A:P3 - LFB
SR_BPMS_UNAVAILABLE = ['S01A:P0', 'S34A:P5', 'S36A:P5', 'S36B:P0', 'S37B:P0', 'S38B:P3', 'S38B:P0', 'S39A:P0',
                       'S39A:P2', 'S39A:P3']

SR_SEPTUM = {'S39-IS1': {'setpoint': 'S39-IES:IS1:SetVoltageC', 'readback': 'S39-IES:IS1:MeasVoltageM',
                         'limits': [1300, 1350]
                         }
             }

SR_TIMING = {
    'S39-IES-Delay': {'setpoint': 'S39-IES:IK1:PosDelayC', 'readback': None, 'limits': [255, 275]}
}

SR_INJ_KICKERS = {
    'S39-IES:IK1': {'setpoint': 'S39-IES:IK1:PS:VoltageC', 'readback': 'S39-IES:IK1:PS:VoltageM',
                    'limits': [21000, 26995]
                    },
    'S39-IES:IK2': {'setpoint': 'S39-IES:IK2:PS:VoltageC', 'readback': 'S39-IES:IK2:PS:VoltageM',
                    'limits': [21000, 26995]
                    },
    'S39-IES:IK3': {'setpoint': 'S39-IES:IK3:PS:VoltageC', 'readback': 'S39-IES:IK3:PS:VoltageM',
                    'limits': [21000, 26995]
                    },
}

SR_SEXTUPOLES = {}
for i in range(1, 41):
    for l, t in [('A', 'S1'), ('A', 'S2'), ('A', 'S3'), ('B', 'S3'), ('B', 'S2'), ('B', 'S1')]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_SEXTUPOLES[root] = {**__std_new_ps(i, root), **__ps_temp_1(root), 'limits': [0, 100]}

SR_QUADS = {}
for i in range(1, 41):
    for l, t in [('A', 'Q1'), ('A', 'Q2'), ('A', 'Q3'), ('A', 'Q6'), ('A', 'Q7'), ('A', 'Q4'), ('A', 'Q5'), ('A', 'Q8'),
                 ('B', 'Q1'), ('B', 'Q2'), ('B', 'Q3'), ('B', 'Q6'), ('B', 'Q7'), ('B', 'Q4'), ('B', 'Q5'),
                 ('B', 'Q8')]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_QUADS[root] = {**__std_new_ps(i, root), **__ps_temp_1(root), 'limits': [0, 200], **__ps_daq_source(root)}

SR_SKEW_QUADS = {}
for i in range(1, 41):
    for l, t in [('A', 'SQ1'), ('A', 'SQ2'),
                 ('B', 'SQ1'), ('B', 'SQ2'), ]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_SKEW_QUADS[root] = {**__std_new_ps(i, root), **__ps_temp_2(root), 'limits': [-15, 15],
                               **__ps_daq_source(root)
                               }

SR_QUAD_TRIMS = {}
for i in range(1, 41):
    for l, t, m in [('A', 'Q4T', 8), ('A', 'Q5T', 8), ('A', 'Q8T', 6),
                    ('B', 'Q4T', 8), ('B', 'Q5T', 8), ('B', 'Q8T', 6)]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_QUAD_TRIMS[root] = {**__std_new_ps(i, root), **__ps_temp_2(root), 'limits': [-m, m], **__ps_daq_source(root)}

SR_DIPOLE_TRIMS = {}
for i in range(1, 41):
    for l, t in [('A', 'M4T'), ('A', 'M3T'), ('B', 'M3T')]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_DIPOLE_TRIMS[root] = {**__std_new_ps(i, root), **__ps_temp_2(root), 'limits': [-15, 15],
                                 **__ps_daq_source(root)
                                 }

SR_DIPOLES = {}
for i in range(1, 41):
    for l, t in [('A', 'M4'), ('A', 'M3'), ('B', 'M3')]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_DIPOLES[root] = {**__std_new_ps(i, root), **__ps_temp_1(root), 'limits': [0, 300]}

BTS_BESOCM = {
    'BTS:BESOCM': {'readback': 'BTS:BESOCM:A:DATA:Beam:QM'}
}

SR_CORRECTORS_V = {}
for i in range(1, 41):
    for l, t, m in [('A', 'V1', 12), ('A', 'FV1', 15), ('A', 'FV2', 15), ('A', 'V7', 9), ('A', 'V8', 6),
                    ('B', 'V7', 9), ('B', 'V1', 12), ('B', 'V8', 6), ('B', 'FV1', 15), ('B', 'FV2', 15), ]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_CORRECTORS_V[root] = {**__std_new_ps(i, root), **__ps_temp_2(root), 'limits': [-m, m],
                                 **__ps_daq_source(root)
                                 }

SR_CORRECTORS_H = {}
for i in range(1, 41):
    for l, t, m in [('A', 'H1', 12), ('A', 'FH1', 15), ('A', 'FH2', 15), ('A', 'H7', 9),
                    ('B', 'H7', 9), ('B', 'H1', 12), ('B', 'FH1', 15), ('B', 'FH2', 15)]:
        root = 'S{i:02d}{l}:{t}'.format(i=i, l=l, t=t)
        SR_CORRECTORS_H[root] = {**__std_new_ps(i, root), **__ps_temp_2(root), 'limits': [-m, m],
                                 **__ps_daq_source(root)
                                 }

SR_ALL_CORRECTORS_H = {**SR_CORRECTORS_H, **SR_DIPOLE_TRIMS, **SR_QUAD_TRIMS}
SR_ALL_CORRECTORS_V = {**SR_CORRECTORS_V}
SR_ALL_CORRECTORS = {**SR_ALL_CORRECTORS_H, **SR_ALL_CORRECTORS_V}

SR_CORRECTORS_FAMILIES = ['H1', 'H7', 'V1', 'V7', 'V8', 'FH1', 'FV1', 'FH2', 'FV2', 'Q4T', 'Q5T', 'Q8T', 'M3T', 'M4T',
                          'SQ1', 'SQ2']

EVENT_119 = 'S-MT:ManDAQTrig1CodeC.PROC'
EVENT_120 = 'S-MT:ManDAQTrig2CodeC.PROC'
EVENT_119_CNT = 'MCR-MT:EVR1:ManDAQTrig1CntM'
EVENT_120_CNT = 'MCR-MT:EVR1:ManDAQTrig2CntM'

EVENT_45_STRIG_CNT = 'MCR-MT:EVR1:STrigCntM'
EVENT_62_SINJTRIG_CNT = 'MCR-MT:EVR1:SInjTrigCntM'
EVENT_60_PRETRIG_CNT = 'MCR-MT:EVR1:SPreTrigCntM'
EVENT_125_GPS1PPS_NUM = 125
EVENT_125_GPS1PPS_CNT = 'MCR-MT:EVR1:GPS1ppsCntM'

PHYSICS_FSTBT = (352055282 / 1296)

# value = event code
MRF_SEND_EVENT = 'MCR-MT:EVM3-SoftEvt:EvtCode-SP'

DAQPS_FIELD_DCCT = 'extCurRdbk'

LFC_AFG1_WF1 = 'S39C:LFC:AFG1:ReadWfCh1C'
LFC_AFG1_WF1_TIME = 'S39C:LFC:AFG1:DispTimeAxisWfCh1M'
LFC_AFG1_WF2 = 'S39C:LFC:AFG1:ReadWfCh2C'
LFC_AFG1_WF2_TIME = 'S39C:LFC:AFG1:DispTimeAxisWfCh2M'
LFC_AFG1_WF1LOAD = 'S39C:LFC:AFG1:LoadWfSeqCh1C.PROC'
LFC_AFG1_WF2LOAD = 'S39C:LFC:AFG1:LoadWfSeqCh2C.PROC'

LFC_AFG2_WF1 = 'S39C:LFC:AFG2:ReadWfCh1C'
LFC_AFG2_WF1_TIME = 'S39C:LFC:AFG2:DispTimeAxisWfCh1M'
LFC_AFG2_WF2 = 'S39C:LFC:AFG2:ReadWfCh2C'
LFC_AFG2_WF2_TIME = 'S39C:LFC:AFG2:DispTimeAxisWfCh2M'
LFC_AFG2_WF1LOAD = 'S39C:LFC:AFG2:LoadWfSeqCh1C.PROC'
LFC_AFG2_WF2LOAD = 'S39C:LFC:AFG2:LoadWfSeqCh2C.PROC'

SR_OTHER = {
    'SR:PHASE': {'setpoint': 'BRF:S:PS1:Ch0_1AO', 'readback': None, 'limits': [-180, 180]}
}

SR_RF_OFFSET = {'setpoint': 'A014-IETS:BTC:SROffsetFreqC'}

SR_H_CLAW_RUNNING = 'S:RC:OrbitControlLawXC.RUN'
SR_H_CLAW_SUSPEND = 'S:RC:OrbitControlLawXC.SUSP'
SR_V_CLAW_RUNNING = 'S:RC:OrbitControlLawYC.RUN'
SR_V_CLAW_SUSPEND = 'S:RC:OrbitControlLawYC.SUSP'

BTS_ALL = {**BTS_CORRECTORS_H_SR, **BTS_CORRECTORS_V_SR, **BTS_CORRECTORS_H_BOOSTER,
           **BTS_CORRECTORS_V_BOOSTER, **BTS_QUADS_BOOSTER, **BTS_QUADS_SR, **BTS_DIPOLES_BOOSTER,
           **SR_SEPTUM, **SR_CORRECTORS_V, **SR_CORRECTORS_H, **SR_TIMING, **SR_INJ_KICKERS, **SR_OTHER,
           **SR_SEXTUPOLES, **SR_QUADS, **SR_QUAD_TRIMS, **SR_SKEW_QUADS, **SR_DIPOLE_TRIMS, **SR_DIPOLES
           }
SR_PS_ALL = {**BTS_ALL}
SR_ALL = {**SR_BPMS, **SR_PS_ALL}
SR = SR_ALL
BTS_ALL_READBACKS_MAP = {v['setpoint']: v['readback'] for k, v in SR_PS_ALL.items()}
SP_TO_NAME = {v['setpoint']: k for k, v in SR_PS_ALL.items()}
SP_TO_RB = {x['setpoint']: x['readback'] for x in SR_PS_ALL.values()}


###

# lattice aux

def ps_split_by_family(power_supply_list: list[str]) -> dict[str, list[str]]:
    lists_by_family = {f: [] for f in SR_CORRECTORS_FAMILIES}
    cnt = 0
    for f in SR_CORRECTORS_FAMILIES:
        for ps in power_supply_list:
            if ":" + f in ps:
                ll = lists_by_family.get(f, [])
                ll.append(ps)
                lists_by_family[f] = ll
                cnt += 1
    return lists_by_family


def ps_filter_by_sector(power_supply_list: list[str], sectors: Iterable[int]):
    ll = []
    for ps in power_supply_list:
        s = int(ps[1:3])
        if s in sectors:
            ll.append(ps)
    return ll


###
import fnmatch
import pvaccess as pva
import numpy as np


def get_pva(name):
    c = pva.Channel(name, pva.PVA)
    data = c.get('')
    return data


def apply_delta_change(knobdb, knob, w):
    knobdict = knobdb[knob]
    pvnames = list(knobdict.keys())
    # initial_vals = acc.read_all_now(pvnames)
    # final_vals = {k:(knob[k]+initial_vals[k][0])*w for k in pvnames}
    final_vals = {k: (knobdict[k]) * w for k in pvnames}
    return final_vals
    # print(final_vals)


def get_knob_pvs(knobdb, knobs):
    st = set()
    for k in knobs:
        knob = knobdb[k]
        pvs = list(knob.keys())
        st = st.union(set(pvs))
    return list(st)


def sr_suspend_orbit_control_laws():
    acc.write({SR_H_CLAW_SUSPEND: 1, SR_V_CLAW_SUSPEND: 1})


def compute_knob_output(initial_input, knobdb, knob_weights):
    real_vals = {}
    for k, v in knob_weights.items():
        new_vals = apply_delta_change(knobdb, k, v)
        for k2, v2 in new_vals.items():
            if k2 in real_vals:
                real_vals[k2] += v2
            else:
                real_vals[k2] = v2

    final_vals = {k: initial_input[k] + real_vals[k] for k in real_vals}
    return final_vals


def knob_mult(k1, w):
    return {k: v * w for k, v in k1.items()}


def knob_filter(k1, k2, fun, limits=None):
    real_vals = {}
    all_pvs = set(list(k1.keys()) + list(k2.keys()))
    for k in all_pvs:
        v1 = k1.get(k, 0.0)
        v2 = k2.get(k, 0.0)
        vf = fun(v1, v2)
        if limits is not None and k in limits:
            if limits[k][0] is not None and vf < limits[k][0]:
                raise Exception(f'Lower bound breach for {k} at {vf} ({limits=})')
            elif limits[k][1] is not None and vf > limits[k][1]:
                raise Exception(f'Upper bound breach for {k} at {vf} ({limits=})')
        real_vals[k] = vf
    return real_vals


def knob_diff(k1, k2):
    """ return vals in k2 that are different from k1 """
    all_pvs = set(list(k1.keys()) + list(k2.keys()))
    final_vals = {}
    for k in all_pvs:
        v1 = k1.get(k, None)
        v2 = k2.get(k, None)
        if v1 is not None and v2 is not None and v1 == v2:
            continue
        else:
            if v2 is not None:
                final_vals[k] = v2

    return final_vals


def get_bpm_sum():
    sumdata = get_pva('S-DAQTBT:InjectionTrajectory100turns')['sum']
    return sumdata


def add_knobs(k1, k2):
    all_keys = set(k1.keys()).union(set(k2.keys()))
    result = {}
    for k in all_keys:
        result[k] = k1.get(k, 0.0) + k2.get(k, 0.0)
    return result


def setup_combined_opt(direct_vars: list, knob_vars: list, knobdb, pvdb):
    direct_sp = [pvdb[x]['setpoint'] for x in direct_vars]
    knob_pvs = get_knob_pvs(knobdb, knob_vars)


from pybeamtools.controlsdirect.clib import Accelerator

acc = Accelerator.get_singleton(default_monitor=False)


def set_sp_threshold(t):
    d = {}
    for s in range(1, 41):
        for b in ['A', 'B']:
            for n in range(1, 7):
                d[f'S{s:02d}{b}:P{n}:sp:adc_thr_sp'] = t
    remap = {'S39B:P1:sp:adc_thr_sp': 'S39B:P0:sp:adc_thr_sp', 'S39B:P0:sp:adc_thr_sp': 'S39C:P0:sp:adc_thr_sp'}
    d = {remap.get(k, k): v for k, v in d.items()}
    acc.write(d)


acc.pvacache = {}


def kvpva(s):
    r = acc.pvacache.get(s, None)
    if r is None:
        r = pva.Channel(s, pva.PVA)
        acc.pvacache[s] = r
    return r


def get_cache():
    for s in range(1, 40, 2):
        c = kvpva(f'S{s:02d}-DAQTBT:Subset4:Data')


def save_all_bpms(mode='Subset3', sectors=None, fields=None):
    bpm_data = {}
    sectors = sectors or list(range(1, 40, 2))
    fields = fields or ['x', 'y', 'sum']
    for s in sectors:
        c = kvpva(f'S{s:02d}-DAQTBT:{mode}:Data')
        data = c.get()
        datafields = list(data.keys())
        for bpm in datafields:
            if bpm.startswith('s') and len(bpm) == 6:
                bpm_data[bpm] = {}
                for f in fields:
                    bpm_data[bpm][f] = data[bpm][f].copy()
        del data
    return bpm_data


DAQ_KNOWN_BAD_BPMS = ['s01ap0', 's34ap5', 's36ap5', 's36bp0', 's37bp0', 's38bp0', 's38bp3', 's39ap0', 's39ap2',
                      's39ap3']


def save_all_bpms_matrix(mode='Subset3', sectors=None, field='sum', debug=True):
    sectors = sectors or list(range(1, 40, 2))
    sectors = sorted(list(set([s for s in sectors if s % 2 == 1] + [s - 1 for s in sectors if s % 2 == 0])))
    # all_sectors = {s: [s,s+1] for s in sectors}
    arrays = []
    bpms = []
    f = field
    roots = [['ap5', 'ap6', 'bp6', 'bp5', 'bp4', 'bp3', 'bp2', 'bp1', 'bp0'],
             ['ap0', 'ap1', 'ap2', 'ap3', 'ap4', 'ap5', 'ap6',
              'bp6', 'bp5', 'bp4', 'bp3', 'bp2', 'bp1', 'bp0'],
             ['ap0', 'ap1', 'ap2', 'ap3', 'ap4']
             ]
    for s in sectors:
        daqs = get_daq_sector(s)
        c = kvpva(f'S{daqs:02d}-DAQTBT:{mode}:Data')
        fstrl = []
        for si, rl in zip(range(s - 1, s + 2), roots):
            if si == 39:
                rl = rl.copy()
                rl.remove('bp1')
            # print(si,rl)
            if si == 0:
                si = 40
            fstr = ', '.join([f's{si:02d}{r}.{field}' for r in rl])
            fstrl.append(fstr)
        fstr = ', '.join(fstrl)
        # print(fstr)
        data = c.get(f'field({fstr})')
        # print(len(data.keys()), data.keys())
        datafields = list(data.keys())
        for bpm in datafields:
            if bpm.startswith('s') and len(bpm) == 6:
                arr = data[bpm][f]
                if len(arr) > 0:
                    arrays.append(arr)
                    bpms.append(bpm)
                else:
                    if debug:
                        if bpm not in DAQ_KNOWN_BAD_BPMS:
                            print(f'Bad bpm {bpm}')
        del data
    if len(arrays) == 0:
        return None, []
    mat = np.column_stack(arrays)
    del arrays
    bpm_names = [SR_BPMS_DAQ_TO_NAME[x] for x in bpms]
    return mat, bpm_names


def save_bpms_matrix_single_sector(mode='Raw', s=1, field='sum', ignore_errors=True):
    arrays = []
    bpms = []
    f = field
    c = kvpva(f'S{s:02d}-DAQTBT:{mode}:Data')
    struct = c.getIntrospectionDict()
    found_fields = [x for x in struct.keys() if x[0] == 's' and len(x) == 6]
    fstr = ', '.join(found_fields + ['time'])
    data = c.get(f'field({fstr})')
    datafields = list(data.keys())
    for bpm in datafields:
        if bpm.startswith('s') and len(bpm) == 6:
            arr = data[bpm][f]
            if len(arr) > 0:
                arrays.append(arr)
                bpms.append(bpm)
            else:
                if not ignore_errors:
                    print(f'Bad bpm {bpm}')
    collection_time = data['time'].copy()
    del data
    if len(arrays) == 0:
        return None, []
    mat = np.column_stack(arrays)
    del arrays
    bpm_names = [SR_BPMS_DAQ_TO_NAME[x] for x in bpms]
    return mat, bpm_names, collection_time


def get_bpm_field_string(mode='Raw', s=1, field='sum'):
    c = kvpva(f'S{s:02d}-DAQTBT:{mode}:Data')
    struct = c.getIntrospectionDict()
    found_fields = [x for x in struct.keys() if x[0] == 's' and len(x) == 6]
    fields = [f'{x}.{field}' for x in found_fields]
    fstr = ', '.join(fields)
    return f'field({fstr})'


def get_ps_field_string(c, field='extCurRdbk', extra=None):
    struct = c.getIntrospectionDict()
    found_fields = [x for x in struct.keys() if x[0] == 's' and x not in ['startTimestamp', 'secondsPastEpoch']]
    fields = [f'{x}.{field}' for x in found_fields]
    if extra is not None:
        fields += extra
    fstr = ', '.join(fields)
    return fstr


def get_daq_sector(s):
    if s == 40:
        return 39
    elif s % 2 == 0:
        return s - 1
    else:
        return s


def daq_ps_name_to_standard(name):
    assert fnmatch.fnmatch(name, 's??[abc]*'), f'Bad name {name}'
    if name[3] in ['a', 'b', 'c']:
        n = name[:4].upper()
        n += ':'
        n += name[4:].upper()
        return n
    else:
        raise


def save_ps_matrix_sector(mode='Raw', s=1, iterations=10, field='extCurRdbk'):
    bpms_master = None
    first = 0
    last = None
    matrices = []
    times = []
    cnt = 0

    c = kvpva(f'S{s:02d}-DAQPS:{mode}:Data')
    time.sleep(0.01)
    while cnt < iterations:
        arrays = []
        bpms = []
        # print(c.getName(), c.getIntrospectionDict())
        # schema = c.getIntrospectionDict()
        data = c.get().toDict()
        collection_time = data['time'].copy()
        # print(data)
        while not c.isConnected():
            time.sleep(0.01)

        datafields = list(data.keys())
        for bpm in datafields:
            if bpm in ['startTimestamp', 'secondsPastEpoch']:
                continue
            if bpm.startswith('s') or bpm.startswith('m'):  ## and bpm[3] in ['a','b','c']:
                if field not in data[bpm]:
                    raise ValueError(f'Bad structure {bpm}')
                arr = data[bpm][field].copy()
                if len(arr) > 0:
                    arrays.append(arr)
                    bpms.append(bpm)
                else:
                    print((
                              f'Bad PS {bpm} for field {field}, have {data[bpm].keys()}, {[len(data[bpm][k]) for k in data[bpm].keys()]}'))
        if len(arrays) == 0:
            return None
        mat = np.column_stack(arrays)
        del arrays
        bpm_names = [daq_ps_name_to_standard(x) for x in bpms]
        tfirst = data['firstSampleNumber']
        tlast = data['lastSampleNumber']
        if tfirst == first:
            assert tlast == last
            # print(f'Already have {tfirst}')
            continue
        else:
            if last is not None:
                assert tfirst == last + 1, f'Lost data {tfirst=} {tlast=} {first=} {last=}'
                assert bpm_names == bpms_master, f'Different data {bpm_names} {bpms_master}'
            else:
                bpms_master = bpm_names
            matrices.append(mat)
            times.append(collection_time)
            last = tlast
            first = tfirst
            cnt += 1

    return np.vstack(matrices), bpms_master, np.hstack(times)


def save_all_ps_matrix(mode='Raw', sectors=None, field='extCurRdbk'):
    sectors = sectors or list(range(1, 40, 2))
    # sectors_daq = 
    # for s in sectors:
    #     if s % 2 == 1:
    #         s -= 1
    arrays = []
    bpms = []
    for s in sectors:
        c = kvpva(f'S{s:02d}-DAQPS:{mode}:Data')
        fstr = get_ps_field_string(c, field=field, extra=['time'])
        data = c.get(fstr).toDict()
        collection_time = data['time'].copy()
        # print(data)
        # while not c.isConnected():
        #     time.sleep(0.01)

        # data = c.get().toDict()
        datafields = list(data.keys())
        for bpm in datafields:
            if bpm.startswith('s') and bpm[3] in ['a', 'b', 'c']:
                if field not in data[bpm]:
                    raise ValueError(f'Bad structure {bpm}')
                arr = data[bpm][field].copy()
                if len(arr) > 0:
                    arrays.append(arr)
                    bpms.append(bpm)
                    # print(f'GOOD PS {bpm} for field {field}')
                else:
                    # d = c.get(f'field({bpm}.{field})')
                    # print(d)
                    # arr = d[bpm][field]
                    # if len(arr) > 0:
                    #     arrays.append(arr)
                    #     bpms.append(bpm)
                    #     print(f'GOOD PS {bpm} for field {field}')
                    # else:
                    print((
                              f'Bad PS {bpm} for field {field}, have {data[bpm].keys()}, {[len(data[bpm][k]) for k in data[bpm].keys()]}'))
        del data
    if len(arrays) == 0:
        return None, []
    mat = np.column_stack(arrays)
    del arrays
    bpm_names = [daq_ps_name_to_standard(x) for x in bpms]
    return mat, bpm_names, collection_time  # , data['firstSampleNumber'], data['lastSampleNumber']


def set_daq_plugin_user(pid, evtid, presamples=10, postsamples=10000, daqroot='DAQTBT'):
    assert 1 <= pid <= 5 and isinstance(pid, int) and isinstance(evtid, int)
    d = {}
    for s in range(1, 40, 2):
        root = f'S{s:02d}-{daqroot}:Subset{pid}'
        d[f'{root}:TriggerEventC'] = evtid
        d[f'{root}:PreTriggerSamplesC'] = presamples
        d[f'{root}:PostTriggerSamplesC'] = postsamples
        d[f'{root}:EnableCallbacksC'] = 1
    acc.write(d)


def set_daqtbt_plugin(pid, evtid, presamples=0, postsamples=10000):
    set_daq_plugin_user(pid, evtid, presamples, postsamples)


def set_daqps_plugin(pid, evtid, presamples=0, postsamples=10000):
    set_daq_plugin_user(pid, evtid, presamples, postsamples, daqroot='DAQPS')


def config_delay(source=45, target=119, delay=600000):
    acc.write({'MCR-MT:EVR1-DlyGen6:Evt:Trig0-SP': source,
               'MCR-MT:EVM3-TrigEvt6:EvtCode-SP': target,
               'MCR-MT:EVR1-DlyGen6:Delay-SP': delay
               })