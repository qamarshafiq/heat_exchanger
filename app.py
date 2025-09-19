import math
import streamlit as st

st.title("Shell-and-Tube Heat Exchanger Design")

# =============================================
# INPUT PARAMETERS (From Example 12.2)
# =============================================
st.header("Input Parameters")

# Fluid properties - Hot Fluid(Shell Side)
st.subheader("Hot Fluid Properties (Shell Side)")
col1, col2 = st.columns(2)
with col1:
    m_oil = st.number_input('Hot Fluids Flow Rate (Kg/s)', value=6.25, help="e.g., 22500/3600 = 6.25")
    T_oil_in = st.number_input('Inlet Temperature [°C]', value=200.0)
    T_oil_out = st.number_input('Outlet Temperature [°C]', value=40.0)
    Cp_oil = st.number_input('Specific heat [J/kg°C]', value=2280.0)
with col2:
    rho_oil = st.number_input('Density [kg/m³]', value=850.0)
    mu_oil = st.number_input('Viscosity [Pa·s]', value=0.34e-3, format="%.2e")
    k_oil = st.number_input('Thermal conductivity [W/m°C]', value=0.134)

# Fluid properties - Cold Fluid (Tube Side)
st.subheader("Cold Fluid Properties (Tube Side)")
col1, col2 = st.columns(2)
with col1:
    T_water_in = st.number_input('Inlet temperature [°C]', value=30.0)
    T_water_out = st.number_input('Outlet temperature [°C]', value=50.0)
    rho_water = st.number_input('Density [kg/m³]', value=992.0)
with col2:
    mu_water = st.number_input('Viscosity [Pa·s]', value=0.671e-3, format="%.2e")
    k_water = st.number_input('Thermal conductivity [W/m°C]', value=0.634)
    Cp_water = st.number_input('Specific heat [J/kg°C]', value=4180.0)

# Pressure Drops
DP_max = st.number_input('Max allowed pressure drop [Pa]', value=100e3, help="100 kN/m²")
hf= st.number_input("Enter the Value of Jh Graph ref. 12.24",value=0.0045,format="%.5f",help="0.0045")
# Tube geometry (From Example 12.2 design)
st.subheader("Tube Geometry")
col1, col2 = st.columns(2)
with col1:
    tube_OD = st.number_input('Outer Diameter (m)', value=0.02000, format="%.5f", help="20.00 mm = 0.02000 m")
    tube_ID = st.number_input('Inner Diameter (m)', value=0.01600, format="%.5f", help="16 mm = 0.01600 m")
with col2:
    tube_length = st.number_input('Tube Length (m)', value=5.0)
    pitch = st.number_input('Pitch (m)', value=1.25 * 0.01905, format="%.5f", help="1.25 * tube_OD")

# Tube arrangement data
data = {
    "triangular": {
        1: {"K1": 0.319, "n1": 2.142},
        2: {"K1": 0.249, "n1": 2.207},
        4: {"K1": 0.175, "n1": 2.285},
        6: {"K1": 0.0743, "n1": 2.499},
        8: {"K1": 0.0365, "n1": 2.675},
    },
    "square": {
        1: {"K1": 0.215, "n1": 2.207},
        2: {"K1": 0.156, "n1": 2.291},
        4: {"K1": 0.158, "n1": 2.263},
        6: {"K1": 0.0402, "n1": 2.617},
        8: {"K1": 0.0331, "n1": 2.643},
    }
}

# Tube arrangement inputs
st.subheader("Tube Arrangement")
pitch_type = st.selectbox("Pitch type", ["triangular", "square"])
num_passes = st.selectbox("Number of tube passes", [1, 2, 4, 6, 8])

if pitch_type in data and num_passes in data[pitch_type]:
    K1 = data[pitch_type][num_passes]["K1"]
    n1 = data[pitch_type][num_passes]["n1"]
else:
    st.error("Invalid pitch type or number of passes")

# Material properties
thermal_conductivity = {
    "aluminium": 202,
    "brass (70 cu, 30 zn)": 97,
    "copper": 388,
    "nickel": 62,
    "cupro-nickel (10% ni)": 45,
    "monel": 30,
    "stainless steel (18/8)": 16,
    "steel": 45,
    "titanium": 16
}

material = st.selectbox("Tube material", list(thermal_conductivity.keys()))
k_wall = thermal_conductivity[material]

# Fouling factors
st.subheader("Fouling Factors")
fluid_factors = {
    "River Water": 0.0002,
    "Sea Water": 0.00065,
    "Cooling Water (Towers)": 0.000235,
    "Towns Water (Soft)": 0.00025,
    "Towns Water (Hard)": 0.00075,
    "Steam Condensate": 0.000435,
    "Steam (Oil Free)": 0.00175,
    "Steam (Oil Traces)": 0.00035,
    "Refrigerated Brine": 0.00025,
    "Air And Industrial Gases": 0.00015,
    "Flue Gases": 0.00035,
    "Organic Vapors": 0.0002,
    "Organic Liquids": 0.0002,
    "Light Hydrocarbons": 0.0002,
    "Heavy Hydrocarbons": 0.0005,
    "Boiling Organics": 0.0004
}

col1, col2 = st.columns(2)
with col1:
    hot_fluid = st.selectbox("Hot fluid", list(fluid_factors.keys()))
with col2:
    cold_fluid = st.selectbox("Cold fluid", list(fluid_factors.keys()))

Rd_oil = fluid_factors[hot_fluid]
Rd_water = fluid_factors[cold_fluid]

# =============================================
# THERMAL CALCULATIONS
# =============================================
if st.button("Calculate"):
    st.header("Calculation Results")
    
    # Heat duty calculation
    Q = m_oil * Cp_oil * (T_oil_in - T_oil_out)
    st.subheader(f"Heat duty: {Q/1000:.2f} kW")
    
    # Cooling water flow rate
    m_water = Q / (Cp_water * (T_water_out - T_water_in))
    st.write(f'Cooling water flow rate: {m_water:.5f} kg/s')
    
    # Temperature difference calculations
    delta_T1 = T_oil_in - T_water_out
    delta_T2 = T_oil_out - T_water_in
    LMTD = (delta_T1 - delta_T2) / math.log(delta_T1 / delta_T2) if delta_T1 != delta_T2 else delta_T1
    st.write(f'LMTD: {LMTD:.5f} °C')
    
    # Correction factor
    R = (T_oil_in - T_oil_out) / (T_water_out - T_water_in)
    S = (T_water_out - T_water_in) / (T_oil_in - T_water_in)
    Ft = 0.94  # Assumed from Figure 12.20
    delta_Tm = Ft * LMTD
    st.write(f'Delta Tm: {delta_Tm:.5f} °C')
    
    # U assumed values
    u_assumed = {
        ('water', 'water'): 1150,
        ('organic solvents', 'organic solvents'): 200,
        ('light oils', 'light oils'): 250,
        ('heavy oils', 'heavy oils'): 175,
        ('gases', 'gases'): 30,
        ('organic solvents', 'water'): 500,
        ('light oils', 'water'): 625,
        ('heavy oils', 'water'): 180,
        ('gases', 'water'): 160,
    }
    
    # Simplified U assumption
    U_assumed = 500  # Default value
    st.write(f'Assumed Overall Coefficient: {U_assumed} W/m²°C')
    
    # Provisional area
    A_provisional = Q / (U_assumed * delta_Tm)
    st.write(f'Provisional Area: {A_provisional:.5f} m²')
    
    # Number of tubes
    tube_surface_area = math.pi * tube_OD * tube_length
    N_tubes = math.ceil(A_provisional / tube_surface_area)
    st.write(f'Number of Tubes: {N_tubes}')
    
    # Tube passes configuration
    N_passes = num_passes
    tubes_per_pass = N_tubes / N_passes
    st.write(f'Tubes per Pass: {tubes_per_pass:.5f}')
    
    # =============================================
    # TUBE-SIDE CALCULATIONS (Water)
    # =============================================
    st.subheader("Tube-Side Calculations")
    
    # Flow area calculation
    flow_area_tube = (math.pi * (tube_ID ** 2) / 4) * tubes_per_pass
    velocity_water = m_water / (rho_water * flow_area_tube)
    st.write(f'Tube-Side Velocity: {velocity_water:.5f} m/s')
    
    # Reynolds number
    Re_water = (rho_water * velocity_water * tube_ID) / mu_water
    st.write(f'Tube-Side Reynolds Number: {Re_water:.5f}')
    
    # Heat transfer coefficient
    Pr_water = (Cp_water * mu_water) / k_water
    Nu_water = 0.023 * Re_water ** 0.8 * Pr_water ** 0.4
    h_water = Nu_water * k_water / tube_ID
    st.write(f'Tube-Side Heat Transfer Coefficient: {h_water:.5f} W/m²°C')
    
    # Pressure drop calculation
    f_tube = 0.0014 + 0.125 * Re_water ** -0.32
    DP_tube = N_passes * (4 * f_tube * (tube_length / tube_ID) * (rho_water * velocity_water ** 2 / 2) 
                         + 2.5 * (rho_water * velocity_water ** 2 / 2))
    st.write(f'Tube-Side Pressure Drop: {DP_tube / 1000:.5f} kPa')
    
    # =============================================
    # SHELL-SIDE CALCULATIONS (Oil)
    # =============================================
    st.subheader("Shell-Side Calculations")
    
    # Bundle diameter estimation
    bundle_dia = tube_OD * (N_tubes / K1) ** (1 / n1)
    st.write(f'Bundle Diameter: {bundle_dia:.5f} m')
    
    # Shell diameter with clearance
    bundle_dia_mm = bundle_dia * 1000
    if bundle_dia_mm < 300:
        clearance_mm = 56
    elif bundle_dia_mm < 600:
        clearance_mm = 92
    else:
        clearance_mm = 111
    
    clearance = clearance_mm / 1000
    shell_dia = bundle_dia + clearance
    st.write(f'Shell Diameter: {shell_dia:.5f} m')
    
    # Baffle configuration
    baffle_spacing = shell_dia / 5
    st.write(f'Baffle Spacing: {baffle_spacing:.5f} m')
    
    # Cross-flow area calculation
    cross_area = ((pitch - tube_OD) / pitch) * shell_dia * baffle_spacing
    st.write(f'Cross-Flow Area: {cross_area:.5f} m²')
    
    # Shell-side velocity
    velocity_oil = m_oil / (rho_oil * cross_area)
    st.write(f'Shell-Side Velocity: {velocity_oil:.5f} m/s')
    
    # Equivalent diameter calculation
    de = (1.10 / tube_OD) * (pitch ** 2 - 0.917 * tube_OD ** 2)
    st.write(f'Equivalent Diameter: {de:.5f} m')
    
    # Reynolds number calculation
    Re_oil = (rho_oil * velocity_oil * de) / mu_oil
    st.write(f'Shell-Side Reynolds Number: {Re_oil:.5f}')
    
    # Heat transfer coefficient
    jh = 4.5e-3
    Pr_oil = (Cp_oil * mu_oil) / k_oil
    Nu_oil = jh * Re_oil * Pr_oil ** (1/3)
    h_oil = Nu_oil * k_oil / de
    st.write(f'Shell-Side Heat Transfer Coefficient: {h_oil:.5f} W/m²°C')
    
    # Pressure drop calculation
    f_shell = 0.12
    DP_shell = (4 * f_shell) * (shell_dia / de) * (tube_length / baffle_spacing) * (rho_oil * velocity_oil ** 2 / 2)
    st.write(f'Shell-Side Pressure Drop: {DP_shell / 1000:.5f} kPa')
    
    # =============================================
    # OVERALL COEFFICIENT CALCULATION
    # =============================================
    st.subheader("Overall Heat Transfer Coefficient")
    
    # Thermal resistances
    R_oil = (1 / h_oil) + Rd_oil
    R_wall = (tube_OD * math.log(tube_OD / tube_ID)) / (2 * k_wall)
    R_water = (tube_OD / tube_ID) * (1 / h_water + Rd_water)
    
    R_total = R_oil + R_wall + R_water
    U_calculated = 1 / R_total
    st.write(f'Calculated Overall Coefficient: {U_calculated:.5f} W/m²°C')
    st.write(f'Assumed Overall Coefficient: {U_assumed} W/m²°C')
    st.write(f'Thanks')
