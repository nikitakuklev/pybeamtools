file = """
record(libera, "$(P):version") 
{
    info(MCII,  "mcii://$(D)/version")
}

record(libera, "$(P):triggers:t2:source_mon")
{
    info(MCII,  "mcii://$(D)/application.triggers.t2.source")
    field(SCAN, "I/O Intr")
}

record(libera, "$(P):calibration:ka_mon")
{
    info(MCII,  "mcii://$(D)/application.calibration.ka")
    field(SCAN, "I/O Intr")
    field(PREC, "3")
}

record(libera, "$(P):calibration:linear:kx_mon")
{
    info(MCII,  "mcii://$(D)/application.calibration.linear.x.k")
    field(SCAN, "I/O Intr")
}

record(libera, "$(P):hk:adc_sensitivity_mon") 
{
    info(MCII,  "mcii://$(D)/application.hk.adc_sensitivity")
    field(SCAN, "I/O Intr")
    field(DESC, "En/dis 6 dB gain on the ADC")
}

record(liberaSignal, "$(P):signals:adc") 
{
    info(MCII,  "mcii://$(D)/application.signals.adc")
    field(NGRP, 2048)
    field(ACQM, "Event")
    field(SCAN, "I/O Intr")
    field(DESC, "Raw ADC data")
}

record(liberaSignal, "$(P):signals:sp") 
{
    info(MCII,  "mcii://$(D)/application.signals.sp")
    field(SCAN, "I/O Intr")
    field(ACQM, "Stream")
    field(DESC, "Single-pass bunch-by-bunch data")
}

record(liberaSignal, "$(P):signals:sp:history")
{
    info(MCII,  "mcii://$(D)/application.signals.sp.history")
    field(NGRP, 8000)
    field(SCAN, "Passive")
    field(ACQM, "Now")
}

record(liberaSignal, "$(P):signals:event") 
{
    info(MCII,  "mcii://$(D)/application.signals.event")
    field(SCAN, "Passive")
}

record(libera, "$(P):ilk:limits:overflow:threshold_mon") 
{
    info(MCII,  "mcii://$(D)/application.interlock.limits.overflow.threshold")
    field(SCAN, "I/O Intr")
}
"""


def test_parser():
    from pybeamtools.utils.epics import EpicsDbParser
    p = EpicsDbParser()
    records = p.parse(file)
    assert len(records) == 10
    print(records)
