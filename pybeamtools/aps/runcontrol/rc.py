import os
import getpass
import time

from pybeamtools.controlsdirect import Accelerator

import socket

print(socket.gethostname())


class RunControlClient:
    def __init__(self, record='OAG170RC', desc='Py Run Control', timeout=5):
        self.record = record
        self.acc = Accelerator.get_singleton()
        self.desc = desc
        self.timeout = timeout
        self.last_hb_time = None

    # Resume = 0
    # Suspend = 1

    # Run = 0
    # Abort = 1
    def start(self):
        base = self.record
        data = {'.USER': getpass.getuser(), '.DESC': self.desc, '.HOST': socket.gethostname(),
                '.PID': str(os.getpid()), '.MSG': 'PyRC startup', '.STRT': time.ctime(),
                '.SUSP': 0, '.ABRT': 0, '.HBT': self.timeout, '.SEM': 0
                }
        for k, v in data.items():
            self.acc.write({base + k: v})
            print(f'{base + k} = {v}')
        self.heartbeat()

    def heartbeat(self):
        tnow = time.time()
        if self.last_hb_time is None or tnow - self.last_hb_time > 1:
            self.acc.write({self.record: 1.0})
            self.last_hb_time = tnow

    def msg(self, msg):
        self.acc.write({self.record + '.MSG': msg + ' @ ' + time.ctime()})

    def check_suspend(self):
        return self.acc.read(self.record + '.SUSP') == 1

    def check_abort(self):
        return self.acc.read(self.record + '.ABRT') == 1
