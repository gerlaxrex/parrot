"""A utility module for plotting audio signals"""
# pylint: disable=C0103
import pydub


try:
    import matplotlib.pyplot as plt
    import numpy as np

    has_plotting = True
except ImportError:
    has_plotting = False


def plot_segment(segment: pydub.AudioSegment) -> None:
    """It plots the amplitude of a segment over time"""
    if not has_plotting:
        message = "parrot1[plotting] must be installed"
        raise ValueError(message)

    T = segment.duration_seconds
    f = segment.frame_rate

    t = np.arange(0, T, 1 / f)
    x = segment.get_array_of_samples()

    plt.plot(t, x)

    plt.xlabel("time [s]")
    plt.ylabel("amplitude")

    plt.show()
