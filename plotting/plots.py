import matplotlib.pyplot as plt
import numpy as np

def plot_bars_and_line(time, series, title, ylabel):
    plt.figure()
    for i in range(len(series)):
        plt.plot([time[i], time[i]], [0, series[i]], '-b', linewidth=8)
    plt.plot(time, series, 'o-r', linewidth=2)
    plt.xlim([-1, len(series)])
    plt.plot([-1, len(series)], [0, 0], '-k')
    plt.xlabel('Time')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()

def plot_cf(time, CF):
    plot_bars_and_line(time, CF, 'Cash Flow', 'CF')

def plot_ccf(time, CCF):
    plot_bars_and_line(time, CCF, 'Cumulative Cash Flow', 'CCF')

def plot_dcf(time, DCF):
    plot_bars_and_line(time, DCF, 'Discounted Cash Flow', 'DCF')

def plot_dccf(time, DCCF):
    plot_bars_and_line(time, DCCF, 'Discounted Cumulative Cash Flow', 'DCCF')

def plot_npv_scan(rates, npv_vec):
    plt.figure()
    plt.plot(rates, npv_vec, '-b')
    plt.xlabel('Discount rate')
    plt.ylabel('NPV')
    plt.title('NPV vs Discount Rate (DCFROR scan)')
    plt.tight_layout()
