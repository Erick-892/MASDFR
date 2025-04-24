import streamlit as st

# Valores base
D_M = (4300 * 100) / 90
R_T = (2500 * 100) / 105

# Diccionarios de recargos / descuentos
daños_materiales = {
    8: -0.10,
    6: -0.05,
    5: 0.00,
    4: 0.05,
    2: 0.10
}

robo_total = {
    14: -0.10,
    12: -0.05,
    10: 0.00,
    8: 0.05,
    6: 0.10
}

# Funciones
def Prima_DM(deducibleDM, DM=D_M):
    recargo_descuento = daños_materiales.get(deducibleDM)
    if recargo_descuento is None:
        return None
    return DM * (1 + recargo_descuento)

def Prima_RT(deducibleRT, RT=R_T):
    recargo_descuento = robo_total.get(deducibleRT)
    if recargo_descuento is None:
        return None
    return RT * (1 + recargo_descuento)

def Prima_RC(SA_RC, RC=500000):
    PrimaRC = 1200
    Exceso_RC = 50000
    Precio_excesos = 50
    if SA_RC == RC:
        return PrimaRC
    elif SA_RC > RC:
        Num_excesos = (SA_RC - RC) / Exceso_RC
        return PrimaRC + (Num_excesos * Precio_excesos)

def Prima_GM(SA_GM, GM=100000):
    PrimaGM = 400
    Exceso_GM = 10000
    Precio_excesos = 20
    if SA_GM == GM:
        return PrimaGM
    elif SA_GM > GM:
        Num_excesos = (SA_GM - GM) / Exceso_GM
        return PrimaGM + (Num_excesos * Precio_excesos)

def Prima_Total(deducibleDM, deducibleRT, SA_RC, SA_GM):
    a = Prima_DM(deducibleDM)
    b = Prima_RT(deducibleRT)
    c = Prima_RC(SA_RC)
    d = Prima_GM(SA_GM)

    if None in (a, b, c, d):
        return None, a, b, c, d

    Total = a + b + c + d
    return Total, a, b, c, d

# --- STREAMLIT APP ---
st.title("Calculadora de prima para un seguro de autos")

# Entradas
deducibleDM = st.selectbox("Selecciona deducible de Daños Materiales (%)", list(daños_materiales.keys()))
deducibleRT = st.selectbox("Selecciona deducible de Robo Total (%)", list(robo_total.keys()))
SA_RC = st.number_input("Suma Asegurada para Responsabilidad Civil", value=500000, step=50000)
SA_GM = st.number_input("Suma Asegurada para Gastos Médicos", value=100000, step=10000)

if st.button("Calcular Prima Total"):
    total, a, b, c, d = Prima_Total(deducibleDM, deducibleRT, SA_RC, SA_GM)
    if total is not None:
        st.success(f"Prima de DM: ${a:,.2f}")
        st.success(f"Prima de RT: ${b:,.2f}")
        st.success(f"Prima de RC: ${c:,.2f}")
        st.success(f"Prima de GM: ${d:,.2f}")
        st.markdown("---")
        st.header(f"💰 Prima neta: ${total:,.2f}")
    else:
        st.error("Revisa que los deducibles o las sumas aseguradas ingresados sean válidos.")
