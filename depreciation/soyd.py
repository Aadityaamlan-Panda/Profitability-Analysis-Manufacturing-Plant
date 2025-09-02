import numpy as np

def depreciation_schedule_soyd(FCI_L1, FCI_L2, S, periods=13, life_years=7, depr_start_idx=3):
    """
    SOYD depreciation over 'life_years' applied from depr_start_idx to depr_start_idx+life_years-1.
    Remaining BV is fully depreciated at the next period (to mimic MATLAB else branch at i>=10).
    """
    dk = np.zeros(periods)
    base = FCI_L1 + FCI_L2 - S
    n = life_years
    soyd = n * (n + 1) / 2.0
    # Annual SOYD charges placed at indices depr_start_idx..depr_start_idx+n-1
    for k in range(n):
        year_idx = depr_start_idx + k
        if year_idx < periods:
            dk[year_idx] = base * (n - k) / soyd

    # Compute BV and write-off remaining at the first index after planned life if any remains
    bv = np.zeros(periods)
    bv0 = FCI_L1 + FCI_L2
    for i in range(periods):
        if i == 0:
            bv[i] = 0.0
        elif i == 1:
            bv[i] = 0.0
        elif i == 2:
            bv[i] = bv0
        else:
            bv[i] = max(bv[i-1] - dk[i], 0.0)

    # find first index after planned schedule with remaining BV and write it off
    tail_idx = depr_start_idx + n
    if tail_idx < periods and bv[tail_idx - 1] > 0:
        dk[tail_idx] = bv[tail_idx - 1]
        # update trailing BV vector (optional to return)
    return dk
