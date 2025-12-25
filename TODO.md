# TODO

## Next Implementation Steps:

- Script to parse GRT .propellant XML files → CSV table (Ba, a0, etc.).
- Plotting script: RC vs. bullet weight with color-coded Ba_eff bands + original data points.
- Charge predictor function.
- Visualization: A script to generate the RC vs. SD plot with Ba_eff bands + your 9 data points (matplotlib → save to /plots/).
- Automation: Python script to read CartridgeData.csv → compute predictions → output to Predictions.csv.
- Source calibrated GRT parameters (Ba, a0, z1/z2, bulk density,
- Refine Relative Capacity (RC) for Bullet Seating Displacement: Current RC ≈ eff_case_vol / bore_capacity_per_inch is a good approximation, but bullet seating depth can reduce usable case volume by 5–15% in short-throat or heavy-bullet configurations (e.g., .308 Win with 190gr SMKs, or 6.5 Creedmoor with 140–147gr ELD-Ms). Also, it would be nice to keep track of statistics for fired case volume to seated projectile effective volume for possible calculation shortcuts.
- Implement Core Scripts in /scripts/: Since the folder is now touched in recent commits, let's populate it with modular Python scripts. Suggestions: calculate_charge.py (load CartridgeData.csv, compute eff_case_vol, eff_barrel_length, ER, predict charge_mass); compute_ba_eff.py (batch process propellant CSV to add Ba_eff column); plot_rc_sd.py (generate RC vs. SD scatter with Ba_eff bands). Use pandas, numpy, matplotlib; add requirements.txt if needed.
- Prototype a Simple Tool: Short-term: Google Sheets or Excel version mirroring core calculations. Longer-term: Streamlit or Gradio app for interactive selector.