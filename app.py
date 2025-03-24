# app.py
# MIT License
# Copyright (c) 2023 Your Name

import streamlit as st
import math

def calculate_heat_exchanger():
    st.title("Shell & Tube Heat Exchanger Design Calculator")
    st.markdown("---")
    
    with st.expander("Hot Fluid Properties", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            hot_flow_rate = st.number_input("Flow rate (kg/h)", min_value=0.0, value=5000.0, key='hot_flow')
            hot_cp = st.number_input("Specific heat (kJ/kg°C)", min_value=0.0, value=4.2, key='hot_cp')
            hot_in_temp = st.number_input("Inlet temperature (°C)", value=120.0, key='hot_in')
        with col2:
            hot_out_temp = st.number_input("Outlet temperature (°C)", value=80.0, key='hot_out')
            hot_density = st.number_input("Density (kg/m³)", min_value=0.0, value=980.0, key='hot_rho')
            hot_viscosity = st.number_input("Viscosity (Pa·s)", min_value=0.0, value=0.0004, format="%.4f", key='hot_visc')

    with st.expander("Cold Fluid Properties", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            cold_flow_rate = st.number_input("Flow rate (kg/h)", min_value=0.0, value=8000.0, key='cold_flow')
            cold_cp = st.number_input("Specific heat (kJ/kg°C)", min_value=0.0, value=4.18, key='cold_cp')
            cold_in_temp = st.number_input("Inlet temperature (°C)", value=20.0, key='cold_in')
        with col2:
            cold_out_temp = st.number_input("Outlet temperature (°C)", value=60.0, key='cold_out')
            cold_density = st.number_input("Density (kg/m³)", min_value=0.0, value=1000.0, key='cold_rho')
            cold_viscosity = st.number_input("Viscosity (Pa·s)", min_value=0.0, value=0.00089, format="%.4f", key='cold_visc')

    with st.expander("Tube Configuration", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            tube_od = st.number_input("Outer diameter (m)", min_value=0.0, value=0.0254, format="%.4f")
            tube_id = st.number_input("Inner diameter (m)", min_value=0.0, value=0.0221, format="%.4f")
            tube_length = st.number_input("Tube length (m)", min_value=0.0, value=5.0)
        with col2:
            tube_pitch = st.number_input("Tube pitch (m)", min_value=0.0, value=0.032, format="%.3f")
            tube_passes = st.number_input("Number of tube passes", min_value=1, value=4)
            tube_k = st.number_input("Material conductivity (W/m°C)", min_value=0.0, value=50.0)

    with st.expander("Shell Configuration", expanded=False):
        shell_type = st.selectbox("Shell type", ['E', 'F', 'G'], index=0)
        baffle_cut = st.slider("Baffle cut (%)", 0, 50, 25) / 100
        baffle_spacing = st.number_input("Baffle spacing (m)", min_value=0.0, value=0.5)

    with st.expander("Design Parameters", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            U_assumed = st.number_input("Initial U assumption (W/m²°C)", min_value=0.0, value=800.0)
        with col2:
            FT = st.number_input("LMTD correction factor", min_value=0.0, max_value=1.0, value=0.9)

    if st.button("Calculate", type="primary"):
        try:
            # Perform calculations
            Q = (hot_flow_rate/3600) * hot_cp * 1000 * (hot_in_temp - hot_out_temp)
            
            ΔT1 = hot_in_temp - cold_out_temp
            ΔT2 = hot_out_temp - cold_in_temp
            LMTD = (ΔT1 - ΔT2) / math.log(ΔT1/ΔT2) if ΔT1 != ΔT2 else ΔT1
            ΔTm = FT * LMTD
            A_required = Q / (U_assumed * ΔTm)

            # Tube count
            tube_area = (math.pi/4) * tube_id**2
            tubes_per_pass = (cold_flow_rate/3600) / (cold_density * tube_area * 1.5)
            num_tubes = math.ceil(tubes_per_pass) * tube_passes

            # Bundle diameter
            K1 = 0.175 if tube_passes == 4 else 0.158
            n1 = 2.285 if tube_passes == 4 else 2.263
            bundle_dia = tube_od * (num_tubes/K1) ** (1/n1)
            shell_dia = bundle_dia + 0.092

            # Heat transfer coefficients
            tube_velocity = (cold_flow_rate/3600) / (cold_density * tube_area * tube_passes)
            Re_tube = cold_density * tube_velocity * tube_id / cold_viscosity
            Pr_tube = cold_cp * 1000 * cold_viscosity / (cold_flow_rate/3600)  # Simplified for demo
            
            # Shell-side calculations
            cross_flow_area = (tube_pitch - tube_od)/tube_pitch * shell_dia * baffle_spacing
            shell_velocity = (hot_flow_rate/3600) / (hot_density * cross_flow_area)
            
            # Display results
            st.success("Calculation Complete!")
            
            with st.expander("Results Summary", expanded=True):
                st.markdown(f"""
                **Heat Duty:** {Q/1e6:.2f} MW  
                **LMTD:** {LMTD:.1f} °C  
                **Corrected ΔT:** {ΔTm:.1f} °C  
                **Required Area:** {A_required:.1f} m²  

                **Number of Tubes:** {num_tubes}  
                **Bundle Diameter:** {bundle_dia:.3f} m  
                **Shell Diameter:** {shell_dia:.3f} m  

                *Note: Detailed coefficients and pressure drops require full implementation.*
                """)
                
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")

if __name__ == "__main__":
    calculate_heat_exchanger()
