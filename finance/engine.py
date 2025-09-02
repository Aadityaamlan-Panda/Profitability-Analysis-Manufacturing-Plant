import numpy as np
from .metrics import cumulative, discounted_cumulative, discount, compute_payback, compute_ccr, compute_roroi

def run_dcf(R_seq, COM_seq, dk_seq, intr, t, FCI_L1, FCI_L2, WC, S, L):
    """
    Executes cash flow logic across 13 periods with:
    - period 0: -L
    - period 1: -FCI_L1
    - period 2: -FCI_L2 - WC
    - periods 3..: operating CF = (R - COM - dk)*(1 - t) + dk
    - final period adds terminal (1-t)*S + WC + L
    """
    # Ensure arrays
    R_seq = np.asarray(R_seq, dtype=float)
    COM_seq = np.asarray(COM_seq, dtype=float)
    dk_seq = np.asarray(dk_seq, dtype=float)
    n = len(R_seq)
    assert n == len(COM_seq) == len(dk_seq), "R_seq, COM_seq, dk_seq must have same length"

    CF = np.zeros(n, dtype=float)

    # Initial investment and WC timing (use indexed assignments!)
    CF[0] = -L
    CF[1] = -FCI_L1
    CF[2] = -FCI_L2 - WC

    # Operating cash flows
    for i in range(3, n):
        op = R_seq[i] - COM_seq[i] - dk_seq[i]
        CF[i] = op * (1.0 - t) + dk_seq[i]

    # Terminal flows at final period
    CF[-1] += (1.0 - t) * S + WC + L

    DCF = discount(CF, intr)
    CCF = cumulative(CF)
    DCCF = cumulative(DCF)

    NPV = DCCF[-1]
    CCP = CCF[-1]
    FCI_net = FCI_L1 + FCI_L2
    FCI_netd = FCI_L1 / (1.0 + intr) + FCI_L2 / ((1.0 + intr) ** 2)

    time = np.linspace(0, n - 1, n)

    PBP = compute_payback(CCF, FCI_net, base_idx=2)
    CCR, CCR_d = compute_ccr(CCF, DCCF)
    ROROI, ROROI_d = compute_roroi(CCF, DCCF, WC, L, FCI_net, FCI_netd, intr, time)

    return {
        "CF": CF,
        "DCF": DCF,
        "CCF": CCF,
        "DCCF": DCCF,
        "NPV": NPV,
        "CCP": CCP,
        "FCI_net": FCI_net,
        "FCI_netd": FCI_netd,
        "PBP": PBP,
        "CCR": CCR,
        "CCR_d": CCR_d,
        "ROROI": ROROI,
        "ROROI_d": ROROI_d,
        "time": time
    }

def scan_dcf_ror(CF, irr_min=0.05, irr_max=0.30, points=10000):
    """
    DCFROR scan: compute NPV vs discount rate and find a zero crossing via linear interpolation.
    """
    CF = np.asarray(CF, dtype=float)
    rates = np.linspace(irr_min, irr_max, points)
    npv_vec = np.zeros_like(rates)
    for j, r in enumerate(rates):
        disc = np.array([CF[i] / ((1.0 + r) ** i) for i in range(len(CF))], dtype=float)
        npv_vec[j] = disc.sum()

    DCFROR = None
    for j in range(len(rates) - 1):
        if npv_vec[j] > 0.0 and npv_vec[j + 1] < 0.0:
            x1, x2 = rates[j], rates[j + 1]
            y1, y2 = npv_vec[j], npv_vec[j + 1]
            DCFROR = x1 + (x1 - x2) / (y1 - y2) * (-y1)
            break

    return rates, npv_vec, DCFROR
