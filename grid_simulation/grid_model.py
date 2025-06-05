import pandapower as pp

# Create an empty network
net = pp.create_empty_network()

# Add buses
b1 = pp.create_bus(net, vn_kv=11.0, name="Main Grid")
b2 = pp.create_bus(net, vn_kv=0.4, name="PV Bus")

# Add line connecting main grid to PV bus
pp.create_line(net, from_bus=b1, to_bus=b2, length_km=0.5, std_type="NAYY 4x50 SE")

# Add external grid connection
pp.create_ext_grid(net, bus=b1)

# Add solar PV (static generator)
pp.create_sgen(net, bus=b2, p_mw=0.2, q_mvar=0, name="Rooftop Solar")

# Add load (building)
pp.create_load(net, bus=b2, p_mw=0.1, q_mvar=0, name="Building Load")

# Run power flow
pp.runpp(net)

# Print results
print("Bus Voltage Magnitudes (p.u.):")
print(net.res_bus.vm_pu)
print("\nLine Loading (%):")
print(net.res_line.loading_percent)