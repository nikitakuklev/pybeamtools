import numpy as np
from pybeamtools.physics.lifetime import LifetimeMeasureAdaptive


def _generate_fake_current_data(x, lifetime_hrs, I0, noise_sigma=1e-3, pow=2 / 3):
    lifetime_secs = lt0 = lifetime_hrs * 3600.0
    if pow == 1:
        I = I0 * np.exp(-x / lifetime_secs)
    elif pow == 2 / 3:
        # lifetime vs current
        # lt(I) = lt0 * (I0/I)^(2/3)
        # dI/dt = - I / lt(I) = - I^(5/3) / (I0^2/3*lt0)

        c = (3 / 2) ** (3 / 2)
        c0 = I0 ** (2 / 3) * lt0
        c1 = (c / I0) ** (2 / 3)
        I = c / ((c1 + x / c0) ** (3 / 2))
    else:
        raise Exception
    return I + noise_sigma * np.random.normal(size=len(x))


def test_ltm_adaptive():
    x = np.arange(0, 30, 0.5)  # seconds
    lifetime_hrs = 2.0
    I0 = 20.0  # mA
    noise_sigma = 1e-3
    y = _generate_fake_current_data(x, lifetime_hrs, I0, noise_sigma=noise_sigma, pow=1)
    ltm = LifetimeMeasureAdaptive(normalized_current=False, normalized_coupling=False)
    results = ltm.compute_lifetime(x, y)
    print(results)
    assert np.isclose(results[0], lifetime_hrs, atol=0.1)

    y = _generate_fake_current_data(x, lifetime_hrs, I0, noise_sigma=noise_sigma, pow=2 / 3)
    ltm = LifetimeMeasureAdaptive(normalized_current=True, current_ref=I0, normalized_coupling=False)
    results = ltm.compute_lifetime(x, y)
    print(results)
    assert np.isclose(results[1], lifetime_hrs, atol=0.1)

    x = np.arange(1000, 1000 + 30, 0.5)

    y = _generate_fake_current_data(x, lifetime_hrs, I0, noise_sigma=noise_sigma, pow=1)
    ltm = LifetimeMeasureAdaptive(normalized_current=False, normalized_coupling=False)
    results = ltm.compute_lifetime(x, y)
    print(results)
    assert np.isclose(results[1], lifetime_hrs, atol=0.1)
    assert np.isclose(results[0], lifetime_hrs, atol=0.1)

    y = _generate_fake_current_data(x, lifetime_hrs, I0, noise_sigma=noise_sigma, pow=2 / 3)
    ltm = LifetimeMeasureAdaptive(normalized_current=True, current_ref=I0, normalized_coupling=False)
    results = ltm.compute_lifetime(x, y)
    print(results)
    assert np.isclose(results[1], lifetime_hrs, atol=0.1)
    assert not np.isclose(results[0], lifetime_hrs, atol=0.1)
