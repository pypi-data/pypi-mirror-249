
from isddp.sddp import LeituraPersonalizadaSDDP
from iplot.modelo.EstruturasGerais import estruturasGerais
import pandas as pd

class dadosSDDP_Volume(estruturasGerais):

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
        estruturasGerais.__init__(self)

    def volumeIncremental(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_vincr_hm3.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_vincr_hm3.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_vincr_hm3.csv").tabela[identificador]


    
    def volumeIncremental_Serie(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_cen_SIN_vincr_hm3.csv").tabela
        if(identificador in self.listaSubmercados):
            df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_cen_sbm_vincr_hm3.csv").tabela
            df_novo = pd.DataFrame()
            df_novo["estagio"] = df["estagio"]
            df_novo["cenario"] = df["cenario"]
            df_novo["valor"] = df[identificador]
            return df_novo
        else:
            df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_cen_usi_vincr_hm3.csv").tabela
            df_novo = pd.DataFrame()
            df_novo["estagio"] = df["estagio"]
            df_novo["cenario"] = df["cenario"]
            df_novo["valor"] = df[identificador]
            return df_novo
        



    def volumeDefluente(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_vdef_hm3.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_vdef_hm3.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_vdef_hm3.csv").tabela[identificador]

    def volumeTurbinado(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_vturb_hm3.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_vturb_hm3.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_vturb_hm3.csv").tabela[identificador]
        
    def volumeVertido(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_vvert_hm3.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_vvert_hm3.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_vvert_hm3.csv").tabela[identificador]
        
    
    def volumeAfluente(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_vafl_hm3.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_vafl_hm3.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_vafl_hm3.csv").tabela[identificador]
    

    def valorAgua(self, identificador):
        if(identificador is None):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]


        if(identificador in self.listaSubmercados):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/pi_agua_per_kreaishm3.csv").tabela[identificador]

    def valorAguaI(self, identificador):
        if(identificador is None):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]


        if(identificador in self.listaSubmercados):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]
        else:
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]