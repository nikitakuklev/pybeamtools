par = {
    'It:P1IKtrig2ParIpAO': [1.3-0.1, 1.3+0.1],
    'It:P2IKtrig2ParIpAO': [1.195-0.1, 1.195+0.1],
    'It:LinacTrig2ParIpAO': [11.38-0.05, 11.38+0.05],
    'P1IK:VoltageSetSendAO': [20,22.5],
    'P2IK:VoltageSetSendAO': [20,22.5]
}

par_rbmap = {
    'It:P1IKtrig2ParIpAO': 'It:P1IKtrig2ParIpAO',
    'It:P2IKtrig2ParIpAO': 'It:P2IKtrig2ParIpAO',
    'It:LinacTrig2ParIpAO': 'It:LinacTrig2ParIpAO',
    'P1IK:VoltageSetSendAO':'P1IK:VoltageSetSendAO',
    'P2IK:VoltageSetSendAO':'P2IK:VoltageSetSendAO'
}

par_traj_knob_rbmap = {
    'L4:TM:sledTrigAO': 'L4:TM:sledTrigMonCC',
    'LTP:H4:CurrentAO': 'LTP:H4:CurrentAI',
    'LTP:H3:CurrentAO': 'LTP:H3:CurrentAI',
    'LTP:H2:CurrentAO': 'LTP:H2:CurrentAI',
    'LTP:H1:CurrentAO': 'LTP:H1:CurrentAI',
    'LTP:V4:CurrentAO': 'LTP:V4:CurrentAI',
    'LTP:V3:CurrentAO': 'LTP:V3:CurrentAI',
    'LTP:V2:CurrentAO': 'LTP:V2:CurrentAI',
    'LTP:V1:CurrentAO': 'LTP:V1:CurrentAI',
}

all_rb = {**par_rbmap}