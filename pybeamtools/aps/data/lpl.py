class ELEMENTS:
    RG1_HZ_SLOW = ['L1:RG1:SC1:HZ', 'L1:RG1:SC2:HZ']
    RG1_HZ_FAST = ['L1:RG1:H3']
    L1_RG1_HZ = ['L1:H1', 'L1:H2']

    RG1_VL_SLOW = ['L1:RG1:SC1:VL', 'L1:RG1:SC2:VL']
    RG1_VL_FAST = ['L1:RG1:V3']
    L1_RG1_VL = ['L1:V1', 'L1:V2']

    RG1_QUADS_SLOW = ['L1:RG1:QM1', 'L1:RG1:QM2', 'L1:RG1:QM3']
    RG1_QUADS_FAST = ['L1:RG1:Q4']
    L1_RG1_QUADS = ['L1:Q1', 'L1:Q2']

    ALL_RG1 = RG1_HZ_SLOW + RG1_HZ_FAST + L1_RG1_HZ + RG1_VL_SLOW + RG1_VL_FAST + L1_RG1_VL + RG1_QUADS_SLOW + RG1_QUADS_FAST + L1_RG1_QUADS


    RG2_HZ = ['L1:RG2:SC2:HZ', 'L1:RG2:SC3:HZ']
    RG2_VL = ['L1:RG2:SC1:VL', 'L1:RG2:SC2:VL', 'L1:RG2:SC3:VL']
    RG2_QUADS = ['L1:RG2:QM1', 'L1:RG2:QM2', 'L1:RG2:QM3', 'L1:RG2:QM4']

    L1_RG2_HZ = ['L1:SC3:HZ', 'L1:SC4:HZ']
    L1_RG2_VL = ['L1:SC3:VL', 'L1:SC4:VL']
    L1_RG2_QUADS = ['L1:QM3', 'L1:QM4', 'L1:QM5']

    ALL_RG2 = RG2_HZ + RG2_VL + RG2_QUADS + L1_RG2_HZ + L1_RG2_VL + L1_RG2_QUADS


    LTP_HZ = ['LTP:H1', 'LTP:H2', 'LTP:H3', 'LTP:H4']
    LTP_VL = ['LTP:V1', 'LTP:V2', 'LTP:V3', 'LTP:V4']

    ALL_LTP = LTP_HZ + LTP_VL


    PHASES = ['L2:PHASE', 'L3:PHASE', 'L4:PHASE', 'L5:PHASE']
    OTHER = ['L4:TM:sledTrigAO']

    ALL = ALL_RG1 + ALL_RG2 + ALL_LTP + PHASES + OTHER

class SETPOINTS:
    RG1_MAP = {
        'L1:RG1:SC1:HZ': 'L1:RG1:SC1:HZ:CurrentAI',
        'L1:RG1:SC1:VL': 'L1:RG1:SC1:VL:CurrentAI',
        'L1:RG1:SC2:HZ': 'L1:RG1:SC2:HZ:CurrentAI',
        'L1:RG1:SC2:VL': 'L1:RG1:SC2:VL:CurrentAI',
        'L1:RG1:H3': 'L1:RG1:H3:SetDacCurrentC',
        'L1:RG1:V3': 'L1:RG1:V3:SetDacCurrentC',
        'L1:RG1:QM1': 'L1:RG1:QM1:CurrentAI',
        'L1:RG1:QM2': 'L1:RG1:QM2:CurrentAI',
        'L1:RG1:QM3': 'L1:RG1:QM3:CurrentAI',
        'L1:RG1:Q4': 'L1:RG1:Q4:SetDacCurrentC',
    }

    L1_RG1_MAP = {
        'L1:H1': 'L1:H1:SetDacCurrentC',
        'L1:V1': 'L1:V1:SetDacCurrentC',
        'L1:Q1': 'L1:Q1:SetDacCurrentC',
        'L1:Q2': 'L1:Q2:SetDacCurrentC',
        'L1:H2': 'L1:H2:SetDacCurrentC',
        'L1:V2': 'L1:V2:SetDacCurrentC'
    }

    RG2_MAP = {
        'L1:RG2:SC2:HZ': 'L1:RG2:SC2:HZ:CurrentAO',
        'L1:RG2:SC1:VL': 'L1:RG2:SC1:VL:CurrentAO',
        'L1:RG2:SC2:VL': 'L1:RG2:SC2:VL:CurrentAO',
        'L1:RG2:SC3:HZ': 'L1:RG2:SC3:HZ:CurrentAO',
        'L1:RG2:SC3:VL': 'L1:RG2:SC3:VL:CurrentAO',
        'L1:RG2:QM1': 'L1:RG2:QM1:CurrentAO',
        'L1:RG2:QM2': 'L1:RG2:QM2:CurrentAO',
        'L1:RG2:QM3': 'L1:RG2:QM3:CurrentAO',
        'L1:RG2:QM4': 'L1:RG2:QM4:CurrentAO',
    }

    L1_RG2_MAP = {
        'L1:SC3:HZ': 'L1:SC3:HZ:CurrentAO',
        'L1:SC3:VL': 'L1:SC3:VL:CurrentAO',
        'L1:QM3': 'L1:QM3:CurrentAO',
        'L1:QM4': 'L1:QM4:CurrentAO',
        'L1:QM5': 'L1:QM5:CurrentAO',
        'L1:SC4:HZ': 'L1:SC4:HZ:CurrentAO',
        'L1:SC4:VL': 'L1:SC4:VL:CurrentAO'
    }

    LTP = {
        'LTP:H1': 'LTP:H1:CurrentAO',
        'LTP:H2': 'LTP:H2:CurrentAO',
        'LTP:H3': 'LTP:H3:CurrentAO',
        'LTP:H4': 'LTP:H4:CurrentAO',
        'LTP:V1': 'LTP:V1:CurrentAO',
        'LTP:V2': 'LTP:V2:CurrentAO',
        'LTP:V3': 'LTP:V3:CurrentAO',
        'LTP:V4': 'LTP:V4:CurrentAO',
    }

    OTHER = {
        'L2:PHASE': 'L-K2:LLRF:DSP:FF_PhaseSetpointC',
        'L3:PHASE': 'L3:PP:phaseAdjAO',
        'L4:PHASE': 'L4:PP:phaseAdjAO',
        'L5:PHASE': 'L5:PP:phaseAdjAO',
        'L4:TM:sledTrigAO': 'L4:TM:sledTrigAO'
    }

    ALL = {**RG1_MAP, **RG2_MAP, **L1_RG1_MAP, **L1_RG2_MAP, **LTP, **OTHER}


class READBACKS:
    RG1_MAP = {
        'L1:RG1:SC1:HZ': 'L1:RG1:SC1:HZ:CurrentAI',
        'L1:RG1:SC1:VL': 'L1:RG1:SC1:VL:CurrentAI',
        'L1:RG1:QM1': 'L1:RG1:QM1:CurrentAI',
        'L1:RG1:SC2:HZ': 'L1:RG1:SC2:HZ:CurrentAI',
        'L1:RG1:SC2:VL': 'L1:RG1:SC2:VL:CurrentAI',
        'L1:RG1:QM2': 'L1:RG1:QM2:CurrentAI',
        'L1:RG1:QM3': 'L1:RG1:QM3:CurrentAI',
        'L1:RG1:Q4': 'L1:RG1:Q4:MeasCurrentM',
    }

    L1_RG1_MAP = {
        'L1:H1': 'L1:H1:MeasCurrentM',
        'L1:V1': 'L1:V1:MeasCurrentM',
        'L1:Q1': 'L1:Q1:MeasCurrentM',
        'L1:Q2': 'L1:Q2:MeasCurrentM',
        'L1:H2': 'L1:H2:MeasCurrentM',
        'L1:V2': 'L1:V2:MeasCurrentM'
    }

    RG2_MAP = {
        'L1:RG2:SC2:HZ': 'L1:RG2:SC2:HZ:CurrentAI',
        'L1:RG2:SC1:VL': 'L1:RG2:SC1:VL:CurrentAI',
        'L1:RG2:SC2:VL': 'L1:RG2:SC2:VL:CurrentAI',
        'L1:RG2:SC3:HZ': 'L1:RG2:SC3:HZ:CurrentAI',
        'L1:RG2:SC3:VL': 'L1:RG2:SC3:VL:CurrentAI',
        'L1:RG2:QM1': 'L1:RG2:QM1:CurrentAI',
        'L1:RG2:QM2': 'L1:RG2:QM2:CurrentAI',
        'L1:RG2:QM3': 'L1:RG2:QM3:CurrentAI',
        'L1:RG2:QM4': 'L1:RG2:QM4:CurrentAI',
    }

    L1_RG2_MAP = {
        'L1:SC3:HZ': 'L1:SC3:HZ:CurrentAI',
        'L1:SC3:VL': 'L1:SC3:VL:CurrentAI',
        'L1:QM3': 'L1:QM3:CurrentAI',
        'L1:QM4': 'L1:QM4:CurrentAI',
        'L1:QM5': 'L1:QM5:CurrentAI',
        'L1:SC4:HZ': 'L1:SC4:HZ:CurrentAI',
        'L1:SC4:VL': 'L1:SC4:VL:CurrentAI'
    }

    OTHER = {
        'L4:TM:sledTrigAO': 'L4:TM:sledTrigMonCC',
    }

    ALL = {**RG1_MAP, **RG2_MAP, **L1_RG1_MAP, **L1_RG2_MAP, **OTHER}


class LIMITS:
    RG1_MAP = {
        'L1:RG1:SC1:HZ': [-2, 2],
        'L1:RG1:SC1:VL': [-2, 2],
        'L1:RG1:SC2:HZ': [-2, 2],
        'L1:RG1:SC2:VL': [-2, 2],
        'L1:RG1:H3': [-2, 2],
        'L1:RG1:V3': [-2, 2],
        'L1:RG1:QM1': [-2, 2],
        'L1:RG1:QM2': [-2, 2],
        'L1:RG1:QM3': [-2, 2],
        'L1:RG1:Q4': [-2, 2],

    }

    ALL = {**RG1_MAP}


class PRESETS:
    RG2_L1 = {
        'L1:SC3:HZ:CurrentAO': [-2, 2],
        'L1:SC3:VL:CurrentAO': [-2, 2],
        'L1:QM3:CurrentAO': [-2, 2],
        'L1:QM4:CurrentAO': [-2, 2],
        'L1:QM5:CurrentAO': [-2, 2],
        'L1:SC4:HZ:CurrentAO': [-2, 2],
        'L1:SC4:VL:CurrentAO': [-2, 2]
    }

    RG2_QUADS = {
        'L1:RG2:QM1:CurrentAO': [-2, 2],
        'L1:RG2:QM2:CurrentAO': [-2, 2],
        'L1:RG2:QM3:CurrentAO': [-2, 2],
        'L1:RG2:QM4:CurrentAO': [-2, 2],
    }

    RG2_CORRECTORS = {
        'L1:RG2:SC1:VL:CurrentAO': [-2, 2],
        'L1:RG2:SC2:HZ:CurrentAO': [-2, 2],
        'L1:RG2:SC2:VL:CurrentAO': [-2, 2],
        'L1:RG2:SC3:HZ:CurrentAO': [-2, 2],
        'L1:RG2:SC3:VL:CurrentAO': [-2, 2],
    }

    L2 = {
        'L2:SC1:HZ:PS:setCurrentAO': [-2, 2],
        'L2:SC1:VL:PS:setCurrentAO': [-2, 2],
        'L2:SC2:HZ:PS:setCurrentAO': [-2, 2],
        'L2:SC2:VL:PS:setCurrentAO': [-2, 2],
        'L2:SC3:HZ:PS:setCurrentAO': [-2, 2],
        'L2:SC3:VL:PS:setCurrentAO': [-2, 2],
        'L2:SC4:HZ:PS:setCurrentAO': [-2, 2],
        'L2:SC4:VL:PS:setCurrentAO': [-2, 2],
    }

    L3 = {
        'L3:SM:SC1:HZ:PS:setCurrentAO': [-2, 2],
        'L3:SM:SC1:VL:PS:setCurrentAO': [-2, 2],
    }

    par_traj_knob = {
        'L4:TM:sledTrigAO': [-0.7, -0.6],
        'LTP:H4:CurrentAO': [-2, 2],  # extra, not in par eff opt
        'LTP:H3:CurrentAO': [-2, 2],
        'LTP:H2:CurrentAO': [-2, 2],
        'LTP:H1:CurrentAO': [-2, 2],
        'LTP:V4:CurrentAO': [-2, 2],  # extra, not in par eff opt
        'LTP:V3:CurrentAO': [-2, 2],
        'LTP:V2:CurrentAO': [-2, 2],
        'LTP:V1:CurrentAO': [-2, 2],
    }

    PHASES = {
        'L-K2:LLRF:DSP:FF_PhaseSetpointC': [-200, 160],
        # 'L3:PP:phaseAdjAO': [4.0, 9.0],
        'L4:PP:phaseAdjAO': [-1.5, 10.0],
        'L5:PP:phaseAdjAO': [-1.5, 10.0],
    }
