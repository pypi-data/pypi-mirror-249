
import pandas as pd
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
import sys
sys.path.append("/home/david/git/inewave_teste")
from inewave.newave import Pmo
from iplot.modelo.EstruturasGerais import estruturasGerais

class dadosNewave_Vazao(estruturas, estruturasGerais):

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        estruturas.__init__(self, caminhoNewave)
        estruturasGerais.__init__(self)
        self.__qDefluenteMinimo = None

    def vazaoIncremental(self, identificador):
        if(identificador is None):
            df = self.leSINRetornaDataFrameCenarioMedio("QINC_SIN_EST.parquet.gzip")
            return df/2.63    
        if(identificador in self.listaSubmercados):
            df = self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "QINC_SBM_EST.parquet.gzip")
            return df/2.63
        else:
            return self.leUsinaRetornaDataFrameCenarioMedio(identificador, "QINC_UHE_EST.parquet.gzip")


    def vazaoIncremental_Serie(self, identificador):
        if(identificador is None):
            df = self.leSINRetornaDataFrameCenariosValidos("QINC_SIN_EST.parquet.gzip")  
            df["valor"] = df["valor"]/2.63
            #print(df)
            return df
        if(identificador in self.listaSubmercados):
            df = self.leSubmercadoRetornaDataFrameCenariosValidos(identificador, "QINC_SBM_EST.parquet.gzip")
            df["valor"] = df["valor"]/2.63
            return df
        else:
            return self.leUsinaRetornaDataFrameCenariosValidos(identificador, "QINC_UHE_EST.parquet.gzip")


    def vazaoTurbinada(self, identificador):
        text = " "
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("QTUR_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "QTUR_SBM_EST.parquet.gzip")
        else:
            return self.leUsinaRetornaDataFrameCenarioMedio(identificador, "QTUR_UHE_EST.parquet.gzip")




        
    def vazaoDefluente(self, identificador):
        if(identificador is None):
            vazaoTurb = self.vazaoTurbinada(identificador).tolist()
            vazaoVert = self.vazaoVertida(identificador).tolist()
            vazaoDef = []
            for i in range(len(vazaoTurb)):
                vazaoDef.append(vazaoTurb[i]+ vazaoVert[i])
            df = pd.DataFrame({"valor": vazaoDef})
            return df["valor"]
            #df = self.leSINRetornaDataFrameCenarioMedio("QDEF_SIN_EST.parquet.gzip")
            #return df/2.63
        if(identificador in self.listaSubmercados):
            #df = self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "QDEF_SBM_EST.parquet.gzip")
            #return df/2.63
            vazaoTurb = self.vazaoTurbinada(identificador).tolist()
            vazaoVert = self.vazaoVertida(identificador).tolist()
            vazaoDef = []
            for i in range(len(vazaoTurb)):
                vazaoDef.append(vazaoTurb[i]+ vazaoVert[i])
            df = pd.DataFrame({"valor": vazaoDef})
            return df["valor"]
        else:
            #return self.leUsinaRetornaDataFrameCenarioMedio(identificador, "QDEF_UHE_EST.parquet.gzip")
            vazaoTurb = self.vazaoTurbinada(identificador).tolist()
            vazaoVert = self.vazaoVertida(identificador).tolist()
            vazaoDef = []
            for i in range(len(vazaoTurb)):
                vazaoDef.append(vazaoTurb[i]+ vazaoVert[i])
            df = pd.DataFrame({"valor": vazaoDef})
            return df["valor"]


    def vazaoAfluente(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("QAFL_SIN_EST.parquet.gzip")/2.63 
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "QAFL_SBM_EST.parquet.gzip")/2.63 
        else:
            return self.leUsinaRetornaDataFrameCenarioMedio(identificador, "QAFL_UHE_EST.parquet.gzip")


    def vazaoDefluenteMinima(self, identificador):
        if(identificador is None):
            df = pd.DataFrame({"valor":[0]})
            return [0]
        if(identificador in self.listaSubmercados):
            return [0]
        else:
            return [0]
            df = Pmo.read(self.caminhoNewave+"/pmo.dat").vazao_defluente_minima
            #pd.set_option('display.max_rows', df.shape[0]+1)
            defluencia_minima = df.loc[(df["usina"] == identificador)]["valor"].tolist()[0]
            self.__qDefluenteMinimo = [defluencia_minima]*59
            return self.__qDefluenteMinimo


    def vazaoVertida(self, identificador):
        if(identificador is None):
            return self.retornaValoresSINAgrupadosPorUsina("QVER_UHE_EST.parquet.gzip")
            #df = self.leSINRetornaDataFrameCenarioMedio("QVER_SIN_EST.parquet.gzip")
            #return df/2.63
        if(identificador in self.listaSubmercados):
            return self.retornaValoresSubmercadoAgrupadosPorUsina(submercado = identificador, arquivo="QVER_UHE_EST.parquet.gzip")
            #df = self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "QVER_SBM_EST.parquet.gzip")
            #return 0
        else:
            return self.leUsinaRetornaDataFrameCenarioMedio(identificador, "QVER_UHE_EST.parquet.gzip")