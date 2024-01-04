
import pandas as pd
import sys
sys.path.append("/home/david/git/inewave_teste")
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
from inewave.newave import Modif
from inewave.newave.modelos.modif import TURBMAXT
from inewave.newave import Hidr
import numpy as np
from iplot.modelo.EstruturasGerais import estruturasGerais


class dadosNewave_Armazenamento(estruturas, estruturasGerais):

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        estruturas.__init__(self, caminhoNewave)
        self.__vMinimo = None
        self.__vMaximoOperativo = None
        self.__volUtilInicial = None
        self.__volFIM = None
        estruturasGerais.__init__(self)

        self.dicionarioSubsistemaUsinasFicticias = { "SUDESTE": ["FICT.MAUA"], 
                                                      "SUL" : [], 
                                                       "NORTE" : ["FICT.SERRA M", "FICT.CANA BR", "FICT.LAJEADO", "FICT.PEIXE A", "FICT.SAO SAL"] , 
                                                    "NORDESTE" : ["FICT.QUEIMAD", "FICT.TRES MA", "FICT.RETIRO", "FICT.IRAPE"]  }
        


    def volumeUtilFinal(self, identificador):
        if(identificador is None):
            df = pd.read_parquet(self.caminhoNewave+'/VARMF_SIN_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["cenario"] == "mean")]["valor"]
            #listaVfim = dataAux
            #vUtilIni = self.volumeUtilInicialSIN
            #listaVfim.insert(0,vUtilIni[0])
            return dataAux
        if(identificador in self.listaSubmercados):
            df = pd.read_parquet(self.caminhoNewave+'/VARMF_SBM_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"]
            #listaVfim = dataAux
            #vUtilIni = self.volumeUtilInicialSubmercado(nomeSubmercado)
            #listaVfim.insert(0,vUtilIni[0])
            return dataAux
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VARMF_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            #listaVfim = dataAux
            #vUtilIni = self.volumeUtilInicialUsina(nomeUsina)
            #listaVfim.insert(0,vUtilIni[0])
            return dataAux


    def volumeUtilInicial(self, identificador):
        if(identificador is None):
            df = pd.read_parquet(self.caminhoNewave+'/VARMI_SIN_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["cenario"] == "mean")]["valor"].tolist()
            for submercado in self.dicionarioSubsistemaUsinasFicticias:
                for ficticia in self.dicionarioSubsistemaUsinasFicticias[submercado]:
                    volIniFict = self.volumeUtilInicial(ficticia).tolist()
                    #print(volIniFict)
                    #print(dataAux)
                    dataAux[0] = dataAux[0] - volIniFict[0]
            df = pd.DataFrame({"valor":dataAux})
            #print(df["valor"])
            return df["valor"]
        if(identificador in self.listaSubmercados):
            df = pd.read_parquet(self.caminhoNewave+'/VARMI_SBM_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"].tolist()
            
            for ficticia in self.dicionarioSubsistemaUsinasFicticias[identificador]:
                volIniFict = self.volumeUtilInicial(ficticia).tolist()
                dataAux[0] = dataAux[0] - volIniFict[0]
            
            df = pd.DataFrame({"valor":dataAux})
            return df["valor"]
        else:
            if(self.__volUtilInicial is None):
                self.__volUtilInicial = pd.read_parquet(self.caminhoNewave+'/VARMI_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = self.__volUtilInicial.loc[(self.__volUtilInicial["usina"] == identificador) & (self.__volUtilInicial["cenario"] == "mean")]["valor"]
            return dataAux




    def volumeMaximoOperativo(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            return 0
        else:
            df = Hidr.read(self.caminhoNewave+"/hidr.dat").cadastro
            volume_maximo = df.loc[(df["nome_usina"] == identificador)]["volume_maximo"].tolist()[0]
            self.__vMaximoOperativo =  [volume_maximo]*59
            return self.__vMaximoOperativo


    def volumeMinimo(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            return 0
        else:
            #uhe = pd.read_parquet(self.caminhoNewave+'/UHE.parquet.gzip', engine='pyarrow')
            
            #print(uhe.loc[(uhe["nome"] == nomeUsina)]["id"].tolist()[0])
            #codigo = uhe.loc[(uhe["nome"] == nomeUsina)]["id"].tolist()[0]



            df = Hidr.read(self.caminhoNewave+"/hidr.dat").cadastro
            volume_minimo = df.loc[(df["nome_usina"] == identificador)]["volume_minimo"].tolist()[0]
            self.__vMinimo =  [volume_minimo]*59        
            return self.__vMinimo


    def volumeFinalPercentual(self, identificador):
        if(identificador is None):
            return [0]
        if(identificador in self.listaSubmercados):
            return [0]
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VARPF_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"].tolist()
            return dataAux


    def volumeInicialPercentual(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            return 0
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VARPI_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"].tolist()
            return dataAux

 
