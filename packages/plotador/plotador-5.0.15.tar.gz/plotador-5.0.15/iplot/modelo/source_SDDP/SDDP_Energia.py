
from isddp.sddp import LeituraPersonalizadaSDDP
import pandas as pd
from iplot.modelo.EstruturasGerais import estruturasGerais

class dadosSDDP_Energia(estruturasGerais):

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
        estruturasGerais.__init__(self)



    def earm(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_enearm_MW.csv").tabela["valor"] 
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_enearm_MW.csv").tabela[identificador]
        else:
            return 0

    def earpf(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            return 0
        else:
            return 0

    def enevert(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_enever_MW.csv").tabela["valor"] 
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_enever_MW.csv").tabela[identificador]
        else:
            return 0
        
    

    def enaflu(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_enaflu_MW.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_enaflu_MW.csv").tabela[identificador]
        else:
            return 0

    
    def enaflu_Serie(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_cen_SIN_enaflu_MW.csv").tabela
        if(identificador in self.listaSubmercados):
            df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_cen_sbm_enaflu_MW.csv").tabela
            df_novo = pd.DataFrame()
            df_novo["estagio"] = df["estagio"]
            df_novo["cenario"] = df["cenario"]
            df_novo["valor"] = df[identificador]
            return df_novo
        else:
            return 0


