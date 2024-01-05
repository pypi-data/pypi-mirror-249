
from isddp.sddp import LeituraPersonalizadaSDDP
from isddp.sddp import Convergencia

class dadosSDDP_Convergencia():

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
    

    @property
    def zinf(self):
        return Convergencia.read(self.caminhoSDDP+"/sddpconv.csv").tabelaConvergencia["zinf"]
    @property
    def iter(self):
        return Convergencia.read(self.caminhoSDDP+"/sddpconv.csv").tabelaConvergencia["iter"]
    @property
    def cpuTime(self):
        c_time = Convergencia.read(self.caminhoSDDP+"/sddpconv.csv").valorTotalCPUTime
        print("SDDP: ", c_time)
        return c_time
