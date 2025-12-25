# TODO

## Completed Implementation Steps:

- Visualization: A script to generate the RC vs. SD plot with Ba_eff bands + your 9 data points (matplotlib → save to /plots/). [Implemented as plot_rc_sd.py]
- Automation: Python script to read CartridgeData.csv → compute predictions → output to Predictions.csv. [Implemented as compute_predictions.py]
- Implement Core Scripts in /scripts/: calculate_charge.py, compute_ba_eff.py, plot_rc_sd.py, requirements.txt added.
- Script to parse GRT .propellant XML files → CSV table (Ba, a0, etc.). [Implemented as parse_grt_prop.py]
- Script to parse GRT cartridge data → CSV (effective volume, bullet info, etc.). [Implemented as parse_grt_cartridge.py with unit conversions]

## Remaining Implementation Steps:

- Plotting script: Generate banded propellant selection graph (RC vs. SD with wide diagonal sloping bands in rainbow colors, like modernized Powley Computer; needs refinement for exact style and bands).
- Charge predictor function.
- Source calibrated GRT parameters (Ba, a0, z1/z2, bulk density, Qex, k) for additional propellants like RL26, N560, H4831SC, and ultra-slow models.
- Refine Relative Capacity (RC) for Bullet Seating Displacement: Current RC ≈ eff_case_vol / bore_capacity_per_inch is a good approximation, but bullet seating depth can reduce usable case volume by 5–15% in short-throat or heavy-bullet configurations (e.g., .308 Win with 190gr SMKs, or 6.5 Creedmoor with 140–147gr ELD-Ms). Also, it would be nice to keep track of statistics for fired case volume to seated projectile effective volume for possible calculation shortcuts.
- Prototype a Simple Tool: Short-term: Google Sheets or Excel version mirroring core calculations (inputs: cartridge dims, bullet weight/SD, barrel length → outputs: predicted charge, RC, recommended Ba_eff band). Longer-term: Streamlit or Gradio app for interactive selector.