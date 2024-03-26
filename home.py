import streamlit as st
from app.icusim import ICUSim, run_simulation
import simpy

def hide_menu():
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """, unsafe_allow_html=True)




# Inicio da Página
st.set_page_config(
    page_title="Simulação de UTI",
    #page_icon="img/favicon.png",
    layout="wide",
)

# hide deploy button and up menu
#hide_menu()

st.title("Simulação de UTI")

dias = st.slider("Dias de simulação", 30, 365, 30)
leitos = st.slider("Número de leitos", 1, 100, 10)

if st.button("Iniciar simulação"):
    #env = simpy.Environment()
    #sim = ICUSim(env)
    #env.process(sim.cria_paciente())
    #env.run(until=30*24)
    sim = run_simulation(dias = dias, leitos=leitos)

    st.write(f"Total de pacientes: {sim.total_pacientes}")
    st.write(f"Pacientes solicitações pendentes: {sim.pacientes_solicitacao}")
    st.write(f"Pacientes internados: {sim.pacientes_internados}")
    st.write(f"Pacientes atendidos: {sim.pacientes_atendidos}")
    st.write(f"Pacientes perdidos: {sim.pacientes_perdidos}")

    st.write(sim.lista_pacientes)
