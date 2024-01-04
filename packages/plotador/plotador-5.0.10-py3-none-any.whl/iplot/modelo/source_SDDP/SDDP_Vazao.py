
from isddp.sddp import LeituraPersonalizadaSDDP
from iplot.modelo.EstruturasGerais import estruturasGerais
import pandas as pd

class dadosSDDP_Vazao(estruturasGerais):

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
        estruturasGerais.__init__(self)

    def vazaoAfluente(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_qafl_m3s.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_qafl_m3s.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qafl_m3s.csv").tabela[identificador]
    


    def vazaoIncremental(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_qincr_m3s.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_qincr_m3s.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qincr_m3s.csv").tabela[identificador]


    def vazaoIncremental_Serie(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_cen_SIN_qincr_m3s.csv").tabela
        if(identificador in self.listaSubmercados):
            df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_cen_sbm_qincr_m3s.csv").tabela
            df_novo = pd.DataFrame()
            df_novo["estagio"] = df["estagio"]
            df_novo["cenario"] = df["cenario"]
            df_novo["valor"] = df[identificador]
            return df_novo
        else:
            identificador = identificador.replace(" ", "")
            df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_cen_usi_qincr_m3s.csv").tabela
            df_novo = pd.DataFrame()
            df_novo["estagio"] = df["estagio"]
            df_novo["cenario"] = df["cenario"]
            df_novo["valor"] = df[identificador]
            return df_novo


    def vazaoDefluenteMinima(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return 0
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_min_defluencia_geral_m3s.csv").tabela[identificador]



    def vazaoDefluente(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_qdef_m3s.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_qdef_m3s.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qdef_m3s.csv").tabela[identificador]


    def vazaoTurbinada(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_qturb_m3s.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_qturb_m3s.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qturb_m3s.csv").tabela[identificador]
    

    def vazaoVertida(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_qvert_m3s.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_qvert_m3s.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_qvert_m3s.csv").tabela[identificador]
    
        







"""

    def getVazaoTurbinadaMaximaUsina(self):
        return self.qTURBMAX
    
    def getVazaoTurbinadaMinimaUsina(self):
        return self.qTURBMIN """
"""         self.wGHMAX = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Ger_max_disp_usi.csv").tabela[self.nomeUsina]
        self.qTURBMAX = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/turbinamento_maximo_usi.csv").tabela[self.nomeUsina]
        self.qTURBMIN = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/turbinamento_minimo_usi.csv").tabela[self.nomeUsina] """
