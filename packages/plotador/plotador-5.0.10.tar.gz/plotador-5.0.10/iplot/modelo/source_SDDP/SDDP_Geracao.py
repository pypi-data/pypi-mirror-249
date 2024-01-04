
from isddp.sddp import LeituraPersonalizadaSDDP
import pandas as pd
from iplot.modelo.EstruturasGerais import estruturasGerais

class dadosSDDP_Geracao(estruturasGerais):

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP
        self.__gHidr = None
        estruturasGerais.__init__(self)
    


    def geracaoTermica(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_gerter_MW.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_gerter_MW.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_gerter_MW.csv").tabela[identificador]

        
    def geracaoHidreletrica(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_gerhid_MW.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_gerhid_MW.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            df = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_gerhid_MW.csv").tabela
            if(identificador in df.columns.tolist()):
                print("Usina existe no dataFrame do SDDP")
                self.__gHidr = df[identificador]
            else:
                print("Usina não existe no dataFrame  do SDDP")
                pd.set_option('display.max_rows', df.shape[0]+1)
                print(df.columns.tolist())
                print(identificador)
                exit(1)
            return self.__gHidr





