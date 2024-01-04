
import pandas as pd
from iplot.modelo.source_Newave.Newave_Geracao import dadosNewave_Geracao
from iplot.modelo.source_Newave.Newave_CMO import dadosNewave_CMO
from iplot.modelo.source_Newave.Newave_Energia import dadosNewave_Energia
from iplot.modelo.source_Newave.Newave_Vazao import dadosNewave_Vazao
from iplot.modelo.source_Newave.Newave_Volume import dadosNewave_Volume
from iplot.modelo.source_Newave.Newave_Convergencia import dadosNewave_Convergencia
from iplot.modelo.source_Newave.Newave_Armazenamento import dadosNewave_Armazenamento


class dadosNewave(dadosNewave_Geracao,dadosNewave_CMO, dadosNewave_Energia, dadosNewave_Vazao, dadosNewave_Volume, dadosNewave_Convergencia, dadosNewave_Armazenamento):

    def __init__(self, caminhoNewave, nome):
        self.nomeCaso = nome
        self.caminhoNewave = caminhoNewave
        print("Carregou caso Newave ", self.caminhoNewave)

        dadosNewave_Geracao.__init__(self, caminhoNewave)
        dadosNewave_CMO.__init__(self, caminhoNewave)
        dadosNewave_Energia.__init__(self, caminhoNewave)
        dadosNewave_Vazao.__init__(self, caminhoNewave)
        dadosNewave_Volume.__init__(self, caminhoNewave)
        dadosNewave_Convergencia.__init__(self, caminhoNewave)
        dadosNewave_Armazenamento.__init__(self, caminhoNewave)
           
    @property
    def caminho(self):
        return self.caminhoNewave

    @property
    def nome(self):
        return self.nomeCaso


    def intercambio(self, submercadoDE, submercadoPARA):
        df = pd.read_parquet(self.caminhoNewave+'/INT_SBP_EST.parquet.gzip', engine='pyarrow')
        df = df.loc[(df["cenario"] == "mean") ]
        dfINTERC = df.loc[(df["submercadoDe"]==submercadoDE) & (df["submercadoPara"]==submercadoPARA)]["valor"]
        return dfINTERC
    
    def intercambioTotalSubmercado(self, submercado):
        df = pd.read_parquet(self.caminhoNewave+'/INT_SBP_EST.parquet.gzip', engine='pyarrow')
        df = df.loc[(df["cenario"] == "mean") ]
        intercDE = df.loc[(df["submercadoDe"] == submercado)]
        intercPARA = df.loc[(df["submercadoPara"] == submercado)]
        totalIntercambio = []
        for periodo in self.estagio.tolist():
            totalIntercambio.append(intercDE.loc[(intercDE["estagio"] == periodo)]["valor"].sum() - intercPARA.loc[(intercPARA["estagio"] == periodo)]["valor"].sum())
        return totalIntercambio
    
    def fphaUtilizada(self, identificador):
        if(identificador is None):
            vazaoTurb = self.vazaoTurbinada(identificador).tolist()
            gh = self.geracaoHidreletrica(identificador).tolist()
            funcaoProducao = []
            for i in range(len(vazaoTurb)):
                funcaoProducao.append(gh[i]/vazaoTurb[i])
            return funcaoProducao  
          
        if(identificador in self.listaSubmercados):
            vazaoTurb = self.vazaoTurbinada(identificador).tolist()
            gh = self.geracaoHidreletrica(identificador).tolist()
            funcaoProducao = []
            for i in range(len(vazaoTurb)):
                funcaoProducao.append(gh[i]/vazaoTurb[i])
            return funcaoProducao  
        else:
            vazaoTurb = self.vazaoTurbinada(identificador).tolist()
            gh = self.geracaoHidreletrica(identificador).tolist()
            funcaoProducao = []
            for i in range(len(vazaoTurb)):
                funcaoProducao.append(gh[i]/vazaoTurb[i])
            return funcaoProducao  