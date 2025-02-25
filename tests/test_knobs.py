from pybeamtools.controls.knobs import Group, Knob, KnobManager
import logging

logger = logging.getLogger(__name__)


def test_calcs():
    g = Group("test", {"a": 1.0, "b": 2.0})
    g2 = Group("test2", {"a2": 3.0, "b2": 4.0})
    g3 = Group("test3", {"a": 5.0, "b3": -6.0})
    k1 = Knob("k1", {g2: 1.0, g: 2.0})
    k2 = Knob("k2", {g3: 1.0, g: 3.0})

    k1c = k1.get_channel_coefficients()
    k2c = k2.get_channel_coefficients()

    assert k1c == {'a': 2.0, 'b': 4.0, 'a2': 3.0, 'b2': 4.0}
    assert k2c == {'a': 8.0, 'b': 6.0, 'b3': -6.0}

    km = KnobManager(knobs=[k1, k2], groups=[g, g2, g3])
    groups = km.compute_groups({"k1": 1.0, "k2": 2.0})
    assert groups == {'test': 8.0, 'test2': 1.0, 'test3': 2.0}

    channels = km.compute_channels({"k1": 1.0, "k2": 2.0})
    assert channels == {'a': 18.0, 'b': 16.0, 'a2': 3.0, 'b2': 4.0, 'b3': -12.0}
