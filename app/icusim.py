import simpy
import random

class ICUSim():
    def __init__(self, env, leitos) -> None:

        self.LEITOS = leitos
        self.TEMPO_MAX_ESPERA = 48
        self.TEMPO_INTERNACAO = [2*24, 10*24]

        self.env = env
        self.total_pacientes = 0
        self.pacientes_solicitacao = 0
        self.pacientes_internados = 0
        self.pacientes_atendidos = 0
        self.pacientes_perdidos = 0
        self.lista_pacientes = {}

        self.leitos = simpy.Resource(self.env, capacity=self.LEITOS)

    def paciente(self, nome, tempo_max_espera, tempo_internacao):
        
        # tempo de chegada do paciente
        t0 = self.env.now
        self.adiciona_paciente(nome, t0=t0)
        
        with self.leitos.request() as req:
            yield req
            # tempo de possibilidade de vaga
            t1 = self.env.now
            if t1 - t0 < tempo_max_espera:
                # critério para internação
                self.pacientes_solicitacao -= 1
                self.adiciona_paciente(nome, t0=t0, t1=t1)
                self.pacientes_internados += 1
                yield self.env.timeout(tempo_internacao)
                
                # tempo de saida do paciente
                t2 = self.env.now
                self.pacientes_internados -= 1
                self.pacientes_atendidos += 1
            else:
                # critério para perda internação na uti
                self.pacientes_solicitacao -= 1
                self.pacientes_perdidos += 1
                t2 = -1

            self.adiciona_paciente(nome, t0=t0, t1=t1, t2=t2)
    
    def cria_paciente(self):
        paciente_nome = 0
        
        while True:
            self.total_pacientes += 1
            self.pacientes_solicitacao += 1
            # sorteia tempo para chegada de um novo paciente entre 2 a 12 hs
            yield self.env.timeout(random.randint(2, 12))
            
            tempo_internacao = random.randint(self.TEMPO_INTERNACAO[0], self.TEMPO_INTERNACAO[1])       
            self.env.process(self.paciente(paciente_nome, self.TEMPO_MAX_ESPERA, tempo_internacao))
            
            paciente_nome += 1

    def adiciona_paciente(self, nome, t0, t1=None, t2=None):
        self.lista_pacientes[nome] = {'t0': t0, 't1': t1, 't2': t2}

def run_simulation(dias, leitos):
    env = simpy.Environment()
    sim = ICUSim(env, leitos)
    env.process(sim.cria_paciente())
    env.run(until=dias*24)

    return sim    


if __name__ == '__main__':
    env = simpy.Environment()
    sim = ICUSim(env  leitos=10)
    env.process(sim.cria_paciente())
    env.run(until=30*24)

    print(f"Total de pacientes: {sim.total_pacientes}")
    print(f"Pacientes solicitações pendentes: {sim.pacientes_solicitacao}")
    print(f"Pacientes internados: {sim.pacientes_internados}")
    print(f"Pacientes atendidos: {sim.pacientes_atendidos}")
    print(f"Pacientes perdidos: {sim.pacientes_perdidos}")
    

    perdas = []
    for i in range(50):
        env = simpy.Environment()
        sim = ICUSim(env, leitos=10)
        env.process(sim.cria_paciente())
        env.run(until=30*24)
        perdas.append(sim.pacientes_perdidos)
    print(f"Perdas: {perdas}")