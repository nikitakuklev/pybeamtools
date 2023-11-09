import tkinter
import tkinter
from .helpers import exec_with_tcl
tcl_instance = None

def init_interpreter():
    tcl = tkinter.Tcl()
    tcl.eval('set auto_path [linsert $auto_path 0 /usr/local/oag/apps/lib/Linux]')
    tcl.eval('proc exit {} {}')
    tcl.eval('APSStandardSetup')
    return tcl


def exec_with_tcl(fname, *args, **kwargs):
    if tcl_instance is None:
        tcl = init_interpreter()
    else:
        tcl = tcl_instance
    kwlist = list(args)
    for (k, v) in kwargs.items():
        kwlist.append(f'-{k}')
        kwlist.append(f'{v}')
    print(f'Executing {fname} with {kwlist}')
    return tcl.call(fname, *kwlist)