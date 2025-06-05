import pandapower as pp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Initialize the network
net = pp.create_empty_network()

# Create buses
bus_slack = pp.create_bus(net, vn_kv=11, name="Slack Bus")
bus_pv = pp.create_bus(net, vn_kv=11, name="PV Bus")
bus_hydro = pp.create_bus(net, vn_kv=11, name="Hydro Bus")
bus_load = pp.create_bus(net, vn_kv=11, name="Load Bus")

# Lines
pp.create_line_from_parameters(net, from_bus=bus_slack, to_bus=bus_pv, length_km=0.1,
                               r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4)
pp.create_line_from_parameters(net, from_bus=bus_pv, to_bus=bus_hydro, length_km=0.1,
                               r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4)
pp.create_line_from_parameters(net, from_bus=bus_hydro, to_bus=bus_load, length_km=0.1,
                               r_ohm_per_km=0.1, x_ohm_per_km=0.1, c_nf_per_km=10, max_i_ka=0.4)

# Grid connection
pp.create_ext_grid(net, bus=bus_slack, vm_pu=1.02, name="Grid Connection")

# Generators
pp.create_sgen(net, bus=bus_pv, p_mw=0.1, q_mvar=0.0, name="PV Generator")
pp.create_sgen(net, bus=bus_hydro, p_mw=0.2, q_mvar=0.0, name="Hydro Generator")

# Load
pp.create_load(net, bus=bus_load, p_mw=0.15, q_mvar=0.05, name="Village Load")

# Run power flow
pp.runpp(net)

# Save results
pp.to_json(net, "model/simulated_grid.json")

# Simulate 24h PV and Load profiles
time_index = [datetime(2024, 6, 1, hour=h) for h in range(24)]
pv_profile = [max(0, np.sin(np.pi * (h - 6) / 12)) * 0.1 for h in range(24)]
load_profile = [0.12 + 0.05 * np.sin(np.pi * h / 12) for h in range(24)]

df_profiles = pd.DataFrame({
    "datetime": time_index,
    "pv_power_mw": pv_profile,
    "load_power_mw": load_profile
})
df_profiles.to_csv("data/pv_load_profiles.csv", index=False)

# Plot
plt.figure(figsize=(10, 5))
plt.plot(time_index, pv_profile, label="PV Power (MW)")
plt.plot(time_index, load_profile, label="Load Power (MW)")
plt.xlabel("Time")
plt.ylabel("Power (MW)")
plt.title("Simulated PV and Load Profiles")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("plots/pv_load_plot.png")
