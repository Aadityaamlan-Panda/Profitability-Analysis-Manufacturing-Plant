# finance/metrics.py
import numpy as np

# ---------- utilities -------------------------------------------------
def _vec(a):
    """Ensure input is a 1-D float array."""
    return np.asarray(a, dtype=float).reshape(-1)

# ---------- basic cumulative helpers ---------------------------------
def cumulative(arr):
    arr = _vec(arr)
    out = np.empty_like(arr)
    run = 0.0
    for i, v in enumerate(arr):
        run += float(v)
        out[i] = run
    return out

def discount(arr, intr):
    arr = _vec(arr)
    return np.array([arr[i] / (1.0 + intr) ** i for i in range(len(arr))],
                    dtype=float)

def discounted_cumulative(arr, intr):
    return cumulative(discount(arr, intr))

# ---------- KPI calculations -----------------------------------------
def compute_payback(CCF, FCI_net, base_idx: int = 2):
    """
    Simple payback period measured from base_idx.
    Returns float('inf') when cumulative cash flow never reaches FCI_net.
    """
    CCF = _vec(CCF)
    delta = CCF - CCF[base_idx]               # position vs initial outlay
    mark = next((i - 1 for i in range(base_idx, len(CCF))
                 if delta[i] >= FCI_net), None)
    if mark is None or mark + 1 >= len(CCF):
        return float("inf")

    frac = (FCI_net - delta[mark]) / (delta[mark + 1] - delta[mark])
    return float((mark - base_idx) + frac)

def compute_ccr(CCF, DCCF):
    """
    Cash-cost return ratios (CCR and discounted CCR_d).
    Always returns two python floats.
    """
    CCF, DCCF = _vec(CCF), _vec(DCCF)
    ccp   = float(CCF[-1])
    ccr   = 1.0 + ccp / (-float(CCF[2]))
    ccr_d = 1.0 + ccp / (-float(DCCF[2]))
    return float(ccr), float(ccr_d)

def compute_roroi(CCF, DCCF, WC, L, FCI_net, FCI_netd, intr, time):
    """
    ROROI and discounted ROROI_d, based on slope between index 2 and last year.
    Both outputs are python floats.
    """
    CCF, DCCF, time = map(_vec, (CCF, DCCF, time))
    span = time[-1] - time[2]                    # years between points

    slope_cash   = (CCF[-1]  - CCF[2]  - WC - L) / span
    slope_disc   = (DCCF[-1] - DCCF[2] -
                    (WC - L) / (1.0 + intr) ** 12) / span

    roroi   = slope_cash / FCI_net  - 1.0 / 12.0
    roroi_d = slope_disc / FCI_netd - 1.0 / 12.0
    return float(roroi), float(roroi_d)
