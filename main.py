# main.py
import argparse
import numpy as np

from config.example_config import CONFIG
from depreciation.soyd import depreciation_schedule_soyd
from depreciation.ddb import depreciation_schedule_ddb
from finance.engine import run_dcf, scan_dcf_ror
from plotting.plots import (
    plot_cf, plot_ccf, plot_dcf, plot_dccf, plot_npv_scan
)


# ---------- helpers ----------
def build_sequences(cfg, R_scalar=None, COM_scalar=None):
    """Return 1-D float arrays for revenue and cost (length = periods)."""
    n = int(cfg["periods"])
    R_val  = cfg["R_scalar"]  if R_scalar  is None else R_scalar
    C_val  = cfg["COM_scalar"] if COM_scalar is None else COM_scalar
    R   = np.full(n, float(R_val), dtype=float)
    COM = np.full(n, float(C_val), dtype=float)
    return R, COM


def get_depreciation(cfg, method):
    """Return depreciation array (length = periods) for SOYD or DDB."""
    if method.lower() == "soyd":
        dk = depreciation_schedule_soyd(
            float(cfg["FCI_L1"]), float(cfg["FCI_L2"]), float(cfg["S"]),
            periods=int(cfg["periods"]),
            life_years=int(cfg["life_years"]),
            depr_start_idx=int(cfg["depr_start_idx"]),
        )
    elif method.lower() == "ddb":
        dk = depreciation_schedule_ddb(
            float(cfg["FCI_L1"]), float(cfg["FCI_L2"]), float(cfg["S"]),
            periods=int(cfg["periods"]),
            life_years=int(cfg["life_years"]),
            depr_start_idx=int(cfg["depr_start_idx"]),
            factor=2.0,
        )
    else:
        raise ValueError("Unknown depreciation method (use SOYD or DDB)")

    dk = np.asarray(dk, dtype=float).reshape(-1)
    if dk.size != int(cfg["periods"]):
        raise ValueError(
            f"Depreciation schedule length {dk.size} != periods {cfg['periods']}"
        )
    return dk


def to_scalar(x):
    """Convert 0-D / 1-element array or python number to float."""
    arr = np.asarray(x).ravel()
    if arr.size != 1:
        raise ValueError(f"Expected scalar value, got shape {arr.shape}")
    return float(arr[0])


# ---------- prompt for user input ----------
def prompt_user(cfg, default_method="SOYD"):
    """Interactively prompt for overrides if not provided via args."""
    print("Enter overrides (press Enter to use default):")

    def get_float(key, desc):
        val = input(f"{desc} (default: {cfg[key]}): ").strip()
        return float(val) if val else cfg[key]

    def get_int(key, desc):
        val = input(f"{desc} (default: {cfg[key]}): ").strip()
        return int(val) if val else cfg[key]

    def get_method(desc, default):
        val = input(f"{desc} (default: {default}): ").strip().upper()
        if val not in ["SOYD", "DDB", ""]:
            print("Invalid method. Using default.")
            return default
        return val if val else default

    method = get_method("Depreciation method (SOYD or DDB)", default_method)

    cfg["FCI_L1"] = get_float("FCI_L1", "Fixed capital investment L1")
    cfg["FCI_L2"] = get_float("FCI_L2", "Fixed capital investment L2")
    cfg["L"] = get_float("L", "Land cost")
    cfg["WC"] = get_float("WC", "Working capital")
    cfg["S"] = get_float("S", "Salvage value")
    cfg["intr"] = get_float("intr", "Discount rate")
    cfg["t"] = get_float("t", "Tax rate")
    cfg["R_scalar"] = get_float("R_scalar", "Per-period revenue (constant)")
    cfg["COM_scalar"] = get_float("COM_scalar", "Per-period operating costs (constant)")
    cfg["life_years"] = get_int("life_years", "Depreciation life in years")
    cfg["depr_start_idx"] = get_int("depr_start_idx", "Index to start depreciation")
    cfg["periods"] = get_int("periods", "Total number of periods")
    cfg["irr_scan_min"] = get_float("irr_scan_min", "Min IRR for DCFROR scan")
    cfg["irr_scan_max"] = get_float("irr_scan_max", "Max IRR for DCFROR scan")
    cfg["irr_scan_points"] = get_int("irr_scan_points", "Points for DCFROR scan")

    return cfg, method


# ---------- main ----------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", default="SOYD",
                        help="Depreciation method: SOYD or DDB")
    parser.add_argument("--no_plots", action="store_true",
                        help="Skip matplotlib charts")

    # Optional overrides for CONFIG parameters
    parser.add_argument("--FCI_L1", type=float, help="Fixed capital investment L1")
    parser.add_argument("--FCI_L2", type=float, help="Fixed capital investment L2")
    parser.add_argument("--L", type=float, help="Land cost")
    parser.add_argument("--WC", type=float, help="Working capital")
    parser.add_argument("--S", type=float, help="Salvage value")
    parser.add_argument("--intr", type=float, help="Discount rate")
    parser.add_argument("--t", type=float, help="Tax rate")
    parser.add_argument("--R_scalar", type=float, help="Per-period revenue (constant)")
    parser.add_argument("--COM_scalar", type=float, help="Per-period operating costs (constant)")
    parser.add_argument("--life_years", type=int, help="Depreciation life in years")
    parser.add_argument("--depr_start_idx", type=int, help="Index to start depreciation")
    parser.add_argument("--periods", type=int, help="Total number of periods")
    parser.add_argument("--irr_scan_min", type=float, help="Min IRR for DCFROR scan")
    parser.add_argument("--irr_scan_max", type=float, help="Max IRR for DCFROR scan")
    parser.add_argument("--irr_scan_points", type=int, help="Points for DCFROR scan")

    args = parser.parse_args()

    # Start with base CONFIG and override with provided args
    cfg = CONFIG.copy()
    if args.FCI_L1 is not None:
        cfg["FCI_L1"] = args.FCI_L1
    if args.FCI_L2 is not None:
        cfg["FCI_L2"] = args.FCI_L2
    if args.L is not None:
        cfg["L"] = args.L
    if args.WC is not None:
        cfg["WC"] = args.WC
    if args.S is not None:
        cfg["S"] = args.S
    if args.intr is not None:
        cfg["intr"] = args.intr
    if args.t is not None:
        cfg["t"] = args.t
    if args.R_scalar is not None:
        cfg["R_scalar"] = args.R_scalar
    if args.COM_scalar is not None:
        cfg["COM_scalar"] = args.COM_scalar
    if args.life_years is not None:
        cfg["life_years"] = args.life_years
    if args.depr_start_idx is not None:
        cfg["depr_start_idx"] = args.depr_start_idx
    if args.periods is not None:
        cfg["periods"] = args.periods
    if args.irr_scan_min is not None:
        cfg["irr_scan_min"] = args.irr_scan_min
    if args.irr_scan_max is not None:
        cfg["irr_scan_max"] = args.irr_scan_max
    if args.irr_scan_points is not None:
        cfg["irr_scan_points"] = args.irr_scan_points

    # Interactively prompt for user input (overrides args and CONFIG)
    cfg, method = prompt_user(cfg, default_method=args.method)

    # 1) build input sequences
    R_seq, COM_seq = build_sequences(cfg)
    dk_seq = get_depreciation(cfg, method)

    # 2) run DCF engine
    results = run_dcf(
        R_seq=R_seq,
        COM_seq=COM_seq,
        dk_seq=dk_seq,
        intr=float(cfg["intr"]),
        t=float(cfg["t"]),
        FCI_L1=float(cfg["FCI_L1"]),
        FCI_L2=float(cfg["FCI_L2"]),
        WC=float(cfg["WC"]),
        S=float(cfg["S"]),
        L=float(cfg["L"]),
    )

    # 3) DCFROR scan
    rates, npv_vec, DCFROR = scan_dcf_ror(
        results["CF"],
        irr_min=float(cfg["irr_scan_min"]),
        irr_max=float(cfg["irr_scan_max"]),
        points=int(cfg["irr_scan_points"]),
    )

    # 4) safely coerce KPIs to floats
    NPV       = to_scalar(results["NPV"])
    CCP       = to_scalar(results["CCP"])
    CCR       = to_scalar(results["CCR"])
    CCR_d     = to_scalar(results["CCR_d"])
    PBP       = results["PBP"]                     # may be inf
    ROROI     = to_scalar(results["ROROI"])
    ROROI_d   = to_scalar(results["ROROI_d"])
    DCFROR_val = None if DCFROR is None else float(DCFROR)

    # 5) print summary
    print(f"Method: {method.upper()}")
    print(f"NPV: {NPV:.4f}")
    print(f"CCP (final CCF): {CCP:.4f}")
    print(f"CCR: {CCR:.6f}")
    print(f"CCR_d: {CCR_d:.6f}")
    print(f"PBP: {'inf' if np.isinf(PBP) else f'{PBP:.4f}'}")
    print(f"ROROI: {ROROI:.6f}")
    print(f"ROROI_d: {ROROI_d:.6f}")
    print(f"DCFROR (approx): {('%.6f' % DCFROR_val) if DCFROR_val else 'None'}")

    # 6) optional plots
    if not args.no_plots:
        plot_cf(results["time"],  results["CF"])
        plot_ccf(results["time"], results["CCF"])
        plot_dcf(results["time"], results["DCF"])
        plot_dccf(results["time"], results["DCCF"])
        plot_npv_scan(rates, npv_vec)
        import matplotlib.pyplot as plt
        plt.show()


if __name__ == "__main__":
    main()
