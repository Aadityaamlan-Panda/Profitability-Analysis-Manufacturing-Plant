CONFIG = {
    "FCI_L1": 175.0,
    "FCI_L2": 125.0,
    "L": 10.0,
    "WC": 20.0,
    "S": 10.0,
    "intr": 0.08,   # discount rate
    "t": 0.25,      # tax rate
    # Scalar revenue and COM per period (periods 0..12); first 3 will be ignored for ops
    "R_scalar": 110.0,
    "COM_scalar": 30.0,
    # Depreciation horizon mapping: indices 3..9 carry annual depreciation; >=10 write-off remaining BV
    "life_years": 7,         # useful life for planned depreciation years
    "depr_start_idx": 3,     # first operating year index (0-based) for depreciation charges
    "periods": 13,
    # DCFROR scan range
    "irr_scan_min": 0.05,
    "irr_scan_max": 0.30,
    "irr_scan_points": 10000,
}
