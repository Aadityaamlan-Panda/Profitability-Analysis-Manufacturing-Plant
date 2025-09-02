import numpy as np

def depreciation_schedule_ddb(FCI_L1, FCI_L2, S, periods=13, life_years=7, depr_start_idx=3, factor=2.0):
    """
    Double-declining balance over 'life_years' starting at depr_start_idx.
    Converts to straight-line if needed to avoid under/over-depreciation.
    Remaining BV after planned life is written off at next period (like MATLAB else branch).
    """
    dk = np.zeros(periods)
    cost = FCI_L1 + FCI_L2
    salvage = S
    life = life_years
    start = depr_start_idx
    end = start + life - 1
    rate = factor / life

    bv = np.zeros(periods)
    for i in range(periods):
        if i == 0:
            bv[i] = 0.0
        elif i == 1:
            bv[i] = 0.0
        elif i == 2:
            bv[i] = cost
        else:
            bv[i] = max(bv[i-1] - dk[i], 0.0)

    for k in range(life):
        idx = start + k
        if idx >= periods:
            break
        # DDB charge
        current_bv = bv[idx-1] if idx > 0 else cost
        ddb_charge = current_bv * rate
        # Ensure we don't go below salvage over remaining years
        remaining_years = life - k
        sl_cap = max((current_bv - salvage) / remaining_years, 0.0)
        charge = min(ddb_charge, sl_cap)
        charge = max(charge, 0.0)
        dk[idx] = charge
        # update BV forward
        for j in range(idx, periods):
            if j == idx:
                bv[j] = max(bv[j-1] - dk[j], 0.0)
            elif j > idx:
                # will continue when future dk assigned; here we avoid full recompute
                break

    # Write-off remaining BV right after planned life
    tail_idx = start + life
    if tail_idx < periods and bv[tail_idx - 1] > 0:
        dk[tail_idx] = bv[tail_idx - 1]
    return dk
