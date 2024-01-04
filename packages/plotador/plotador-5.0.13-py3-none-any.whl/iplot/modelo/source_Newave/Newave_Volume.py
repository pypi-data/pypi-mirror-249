
import pandas as pd
import sys
sys.path.append("/home/david/git/inewave_teste")
from iplot.modelo.source_Newave.Newave_Estruturadores import estruturas
from inewave.newave import Modif
from inewave.newave.modelos.modif import TURBMAXT
from inewave.newave import Hidr
import numpy as np
from iplot.modelo.EstruturasGerais import estruturasGerais

class dadosNewave_Volume(estruturas, estruturasGerais):

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave
        estruturas.__init__(self, caminhoNewave)
        estruturasGerais.__init__(self)

    def volumeIncremental(self, identificador):
        if(identificador is None):
            df = pd.read_parquet(self.caminhoNewave+'/VINC_SIN_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["cenario"] == "mean")]["valor"]
            return dataAux     
        if(identificador in self.listaSubmercados):
            df = pd.read_parquet(self.caminhoNewave+'/VINC_SBM_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux 
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VINC_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux

    def volumeIncremental_Serie(self, identificador):
        if(identificador is None):
            return self.leSINRetornaDataFrameCenariosValidos("VINC_SIN_EST.parquet.gzip")
        if(identificador in self.listaSubmercados):
            return self.leSubmercadoRetornaDataFrameCenariosValidos(identificador, "VINC_SBM_EST.parquet.gzip")
        else:
            return self.leUsinaRetornaDataFrameCenariosValidos(identificador, "VINC_UHE_EST.parquet.gzip")


    def volumeTurbinado(self, identificador):
        if(identificador is None):
            df = pd.read_parquet(self.caminhoNewave+'/VTUR_SIN_EST.parquet.gzip', engine='pyarrow')
            
            dataAux = df.loc[(df["cenario"] == "mean")]["valor"]
            dataAux = dataAux*2.63
            
            return dataAux
        if(identificador in self.listaSubmercados):
            df = pd.read_parquet(self.caminhoNewave+'/VTUR_SBM_EST.parquet.gzip', engine='pyarrow')
            
            dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"]
            dataAux = dataAux*2.63
            return dataAux
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VTUR_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux



    
  
    

    

        

    def volumeAfluente(self, identificador):
        if(identificador is None):
            df = pd.read_parquet(self.caminhoNewave+'/VAFL_SIN_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["cenario"] == "mean")]["valor"]
            return dataAux 
        if(identificador in self.listaSubmercados):
            df = pd.read_parquet(self.caminhoNewave+'/VAFL_SBM_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux 
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VINC_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux


    def volumeDefluente(self, identificador):
        if(identificador is None):
            #df = pd.read_parquet(self.caminhoNewave+'/VDEF_SIN_EST.parquet.gzip', engine='pyarrow')
            #dataAux = df.loc[(df["cenario"] == "mean")]["valor"].tolist()
            #return dataAux
            volumeTurb = self.volumeTurbinado(identificador).tolist()
            volumeVert = self.volumeVertido(identificador).tolist()
            volumeDef = []
            for i in range(len(volumeTurb)):
                volumeDef.append(volumeTurb[i]+ volumeVert[i])
            df = pd.DataFrame({"valor":volumeDef   }) 
            return df["valor"]
        if(identificador in self.listaSubmercados):
            #df = pd.read_parquet(self.caminhoNewave+'/VDEF_SBM_EST.parquet.gzip', engine='pyarrow')
            #dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"].tolist()
            #return dataAux  
            volumeTurb = self.volumeTurbinado(identificador).tolist()
            volumeVert = self.volumeVertido(identificador).tolist()
            volumeDef = []
            for i in range(len(volumeTurb)):
                volumeDef.append(volumeTurb[i]+ volumeVert[i])
            df = pd.DataFrame({"valor":volumeDef   }) 
            return df["valor"]
        else:
            #df = pd.read_parquet(self.caminhoNewave+'/VDEF_UHE_EST.parquet.gzip', engine='pyarrow')
            #dataAux = df.loc[(df["usina"] == nomeUsina) & (df["cenario"] == "mean")]["valor"].tolist()
            volumeTurb = self.volumeTurbinado(identificador).tolist()
            volumeVert = self.volumeVertido(identificador).tolist()
            volumeDef = []
            for i in range(len(volumeTurb)):
                volumeDef.append(volumeTurb[i]+ volumeVert[i])
            df = pd.DataFrame({"valor":volumeDef   }) 
            return df["valor"]



    def volumeVertido(self, identificador):
        if(identificador is None):
            #df = pd.read_parquet(self.caminhoNewave+'/VVER_SIN_EST.parquet.gzip', engine='pyarrow')
            #dataAux = df.loc[(df["cenario"] == "mean")]["valor"].tolist()
            #return dataAux   
            lista = self.retornaValoresSINAgrupadosPorUsina("VVER_UHE_EST.parquet.gzip")
            df = pd.DataFrame({"valor":lista})

            return df["valor"]


        if(identificador in self.listaSubmercados):
            #df = pd.read_parquet(self.caminhoNewave+'/VVER_SBM_EST.parquet.gzip', engine='pyarrow')
            #dataAux = df.loc[(df["submercado"] == identificador) & (df["cenario"] == "mean")]["valor"].tolist()
            #return dataAux  
            lista = self.retornaValoresSubmercadoAgrupadosPorUsina(submercado = identificador,arquivo="VVER_UHE_EST.parquet.gzip")
            df = pd.DataFrame({"valor":lista})
            return df["valor"]
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VVER_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux

    def valorAgua(self, identificador):
        if(identificador is None):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]


        if(identificador in self.listaSubmercados):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VAGUA_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux

    def valorAguaI(self, identificador):
        if(identificador is None):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]


        if(identificador in self.listaSubmercados):
            df = pd.DataFrame({"valor":[0]})
            return df["valor"]
        else:
            df = pd.read_parquet(self.caminhoNewave+'/VAGUAI_UHE_EST.parquet.gzip', engine='pyarrow')
            dataAux = df.loc[(df["usina"] == identificador) & (df["cenario"] == "mean")]["valor"]
            return dataAux
        

"""         listaRegistros = Modif.read(self.caminhoNewave+"/modif.dat").modificacoes_usina(34)
        for elemento in listaRegistros:
            if(isinstance(elemento,TURBMAXT)):
                elemento.turbinamento """

    #def getVolumeInicialUsina(self):
    #    return self.vIni.tolist()[0]


    #def getGeracaoHidreletricaMaximaUsina(self):
    #    return self.wGHMAX

    #def getVazaoTurbinadaMaximaUsina(self):
    #    return self.qTURBMAX
    
    #def getVazaoTurbinadaMinimaUsina(self):
    #    return self.qTURBMIN

    #def getVazaoDefluenteMaximaUsina(self):
    #    return self.qDEFMAX


   