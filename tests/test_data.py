from pybeamtools.aps.data import lpl


def test_data():
    for el in lpl.ELEMENTS.ALL:
        assert el in lpl.SETPOINTS.ALL

    for el in lpl.READBACKS.ALL:
        assert el in lpl.ELEMENTS.ALL

    for el in lpl.LIMITS.ALL:
        assert el in lpl.ELEMENTS.ALL
