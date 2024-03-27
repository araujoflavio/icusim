import streamlit as st
from app.icusim import ICUSim, run_simulation
#import simpy
import plotly.express as px

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

# Items a serem implementados
    # quande de pacientes por dia
    # tempo de internação
    # tempo máximo de espera




dias = st.slider("Dias de simulação", 30, 365, 30)
leitos = st.slider("Número de leitos", 1, 100, 10)
numero_simulacoes = st.slider("Número de simulações", 1, 1000, 1)

if st.button("Iniciar simulação"):
    #env = simpy.Environment()
    #sim = ICUSim(env)
    #env.process(sim.cria_paciente())
    #env.run(until=30*24)
    if numero_simulacoes>1:
        sim = []
        for i in range(numero_simulacoes):
            sim.append(run_simulation(dias = dias, leitos=leitos))

        lista_paciente_perdidos = [s.pacientes_perdidos for s in sim]
        fig = px.histogram(x=lista_paciente_perdidos, title="Histograma de pacientes perdidos")
        st.plotly_chart(fig)
    else:
        sim = run_simulation(dias = dias, leitos=leitos)
        st.write(f"Total de pacientes: {sim.total_pacientes}")
        st.write(f"Pacientes solicitações pendentes: {sim.pacientes_solicitacao}")
        st.write(f"Pacientes internados: {sim.pacientes_internados}")
        st.write(f"Pacientes atendidos: {sim.pacientes_atendidos}")
        st.write(f"Pacientes perdidos: {sim.pacientes_perdidos}")

        st.write(f"Pacintes perdidos {sim.pacientes_perdidos/sim.total_pacientes*100:0.2f} %")
        st.write(sim.lista_pacientes)
# itens para análise
    # total de pacientes
    # pacientes solicitados
    # pacientes internados
    # pacientes atendidos
    # pacientes perdidos

    # paciente dia da unidade
    # taxa de ocupação
    # tempo de internacao
    # tempo de espera - de admitidos e de perdidos
    # relacao de pacietes perdidos/total de pacientes solicitados