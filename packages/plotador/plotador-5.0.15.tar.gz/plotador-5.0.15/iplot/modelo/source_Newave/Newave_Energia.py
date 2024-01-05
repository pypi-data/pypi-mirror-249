
import pandas as pd
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
from iplot.modelo.EstruturasGerais import estruturasGerais


class dadosNewave_Energia(estruturas, estruturasGerais ):

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        estruturas.__init__(self, caminhoNewave)
        estruturasGerais.__init__(self)



    def earm(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("EARMF_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "EARMF_SBM_EST.parquet.gzip")
        else:
            return 0


    def earpf(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("EARPF_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "EARPF_SBM_EST.parquet.gzip")
        else:
            return 0
        

    def enevert(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("EVER_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "EVER_SBM_EST.parquet.gzip")
        else:
            return 0



    def enaflu(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenarioMedio("ENAA_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenarioMedio(identificador, "ENAA_SBM_EST.parquet.gzip")
        else:
            return 0


    def enaflu_Serie(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenariosValidos("ENAA_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenariosValidos(identificador, "ENAA_SBM_EST.parquet.gzip")
        else:
            return 0

