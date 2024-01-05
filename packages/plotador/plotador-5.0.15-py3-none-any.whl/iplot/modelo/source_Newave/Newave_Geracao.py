
import pandas as pd
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
from iplot.modelo.EstruturasGerais import estruturasGerais


class dadosNewave_Geracao(estruturas, estruturasGerais):

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        self.__gHidr = None
        estruturasGerais.__init__(self)



    def geracaoTermica(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("GTER_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "GTER_SBM_EST.parquet.gzip")
        else:
            return self.leUsinaRetornaDataFrameCenarioMedio(identificador, "GTER_UTE_EST.parquet.gzip")



    def geracaoHidreletrica(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("GHID_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "GHID_SBM_EST.parquet.gzip")
        else:
            #if self.__gHidr is None:
            df = pd.read_parquet(self.caminhoNewave+'/GHID_UHE_EST.parquet.gzip', engine='pyarrow')
            if(identificador in df["usina"].tolist()):
                print("Usina existe no dataFrame do caso", self.caminhoNewave)
                self.__gHidr = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            else:
                print("Usina não existe no dataFrame do caso", self.caminhoNewave)
                df = pd.read_parquet(self.caminhoNewave+'/UHE.parquet.gzip', engine='pyarrow')
                pd.set_option('display.max_rows', df.shape[0]+1)
                print(df)
                exit(1)
            return self.__gHidr


    