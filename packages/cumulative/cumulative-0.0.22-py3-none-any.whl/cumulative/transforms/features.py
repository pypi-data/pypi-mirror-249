import numpy as np
import pandas as pd
import scipy
from tsfel.feature_extraction.features import (
    abs_energy,
    auc,
    autocorr,
    average_power,
    calc_centroid,
    calc_max,
    calc_mean,
    calc_median,
    calc_min,
    calc_std,
    calc_var,
    distance,
    entropy,
    fundamental_frequency,
    human_range_energy,
    interq_range,
    kurtosis,
    max_frequency,
    max_power_spectrum,
    mean_abs_deviation,
    mean_abs_diff,
    mean_diff,
    median_abs_deviation,
    median_abs_diff,
    median_diff,
    median_frequency,
    negative_turning,
    neighbourhood_peaks,
    pk_pk_distance,
    positive_turning,
    rms,
    skewness,
    slope,
    spectral_centroid,
    spectral_decrease,
    spectral_distance,
    spectral_entropy,
    spectral_kurtosis,
    spectral_positive_turning,
    spectral_skewness,
    spectral_slope,
    spectral_spread,
    spectral_variation,
    sum_abs_diff,
    zero_cross,
)

from cumulative.transforms.transform import Transform


def feature_peaks(signal):
    attrs = {}
    peaks = scipy.signal.find_peaks(signal)
    attrs["peaks_count"] = peaks[0].shape[0]
    attrs["peaks_avg"] = signal[peaks[0]].mean() if attrs["peaks_count"] > 0 else 0
    return attrs


def feature_stats(signal):
    return {
        "len": signal.shape[0],
        "max": signal.max(),
        "min": signal.min(),
        "std": signal.std(),
        "mean": signal.mean(),
        "median": np.median(signal),
    }


def feature_tsfel(signal):

    # Features from tsfel. Some features have been ignored due to:
    # - more than one value returned (more work required for integration)
    # - not defined in some cases
    #
    # power_bandwidth
    # spectral_roll_off
    # mfcc
    # wavelet_abs_mean
    # wavelet_energy
    # wavelet_entropy
    # wavelet_std
    # wavelet_var
    # ecdf
    # ecdf_percentile
    # ecdf_percentile_count
    # ecdf_slope
    # fft_mean_coeff
    # hist
    # lpcc

    fs = 1
    return {
        "abs_energy": abs_energy(signal),
        "auc": auc(signal, fs),
        "autocorr": autocorr(signal),
        "average_power": average_power(signal, fs),
        "calc_centroid": calc_centroid(signal, fs),
        "calc_max": calc_max(signal),
        "calc_mean": calc_mean(signal),
        "calc_median": calc_median(signal),
        "calc_min": calc_min(signal),
        "calc_std": calc_std(signal),
        "calc_var": calc_var(signal),
        "distance": distance(signal),
        "entropy": entropy(signal),
        "fundamental_frequency": fundamental_frequency(signal, fs),
        "human_range_energy": human_range_energy(signal, fs),
        "interq_range": interq_range(signal),
        "kurtosis": kurtosis(signal),
        "max_frequency": max_frequency(signal, fs),
        "max_power_spectrum": max_power_spectrum(signal, fs),
        "mean_abs_deviation": mean_abs_deviation(signal),
        "mean_abs_diff": mean_abs_diff(signal),
        "mean_diff": mean_diff(signal),
        "median_abs_deviation": median_abs_deviation(signal),
        "median_abs_diff": median_abs_diff(signal),
        "median_diff": median_diff(signal),
        "median_frequency": median_frequency(signal, fs),
        "negative_turning": negative_turning(signal),
        "neighbourhood_peaks": neighbourhood_peaks(signal),
        "pk_pk_distance": pk_pk_distance(signal),
        "positive_turning": positive_turning(signal),
        "rms": rms(signal),
        "skewness": skewness(signal),
        "slope": slope(signal),
        "spectral_centroid": spectral_centroid(signal, fs),
        "spectral_decrease": spectral_decrease(signal, fs),
        "spectral_distance": spectral_distance(signal, fs),
        "spectral_entropy": spectral_entropy(signal, fs),
        "spectral_kurtosis": spectral_kurtosis(signal, fs),
        "spectral_positive_turning": spectral_positive_turning(signal, fs),
        "spectral_skewness": spectral_skewness(signal, fs),
        "spectral_slope": spectral_slope(signal, fs),
        "spectral_spread": spectral_spread(signal, fs),
        "spectral_variation": spectral_variation(signal, fs),
        "sum_abs_diff": sum_abs_diff(signal),
        "zero_cross": zero_cross(signal),
    }


class Features(Transform):
    def transform_row(self, row, src):

        signal = row[f"{src}.y"]
        attrs = {}
        attrs.update(feature_stats(signal))
        attrs.update(feature_peaks(signal))
        attrs.update(feature_tsfel(signal))

        return pd.Series(attrs)
