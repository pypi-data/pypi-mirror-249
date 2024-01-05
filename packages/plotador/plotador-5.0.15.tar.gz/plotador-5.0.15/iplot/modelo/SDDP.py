
import pandas as pd
import sys
#sys.path.append("/home/david/git/isddp")
from isddp.sddp import LeituraPersonalizadaSDDP
from iplot.modelo.source_SDDP.SDDP_CMO import dadosSDDP_CMO
from iplot.modelo.source_SDDP.SDDP_Energia import dadosSDDP_Energia
from iplot.modelo.source_SDDP.SDDP_Geracao import dadosSDDP_Geracao
from iplot.modelo.source_SDDP.SDDP_Vazao import dadosSDDP_Vazao
from iplot.modelo.source_SDDP.SDDP_Volume import dadosSDDP_Volume
from iplot.modelo.source_SDDP.SDDP_Convergencia import dadosSDDP_Convergencia
from iplot.modelo.source_SDDP.SDDP_Armazenamento import dadosSDDP_Armazenamento

class dadosSDDP(dadosSDDP_CMO, dadosSDDP_Energia, dadosSDDP_Geracao, dadosSDDP_Vazao, dadosSDDP_Volume, dadosSDDP_Convergencia, dadosSDDP_Armazenamento):

    def __init__(self, caminhoSDDP, nome):

        dadosSDDP_CMO.__init__(self, caminhoSDDP)
        dadosSDDP_Energia.__init__(self, caminhoSDDP)
        dadosSDDP_Geracao.__init__(self, caminhoSDDP)
        dadosSDDP_Vazao.__init__(self, caminhoSDDP)
        dadosSDDP_Volume.__init__(self, caminhoSDDP)
        dadosSDDP_Convergencia.__init__(self, caminhoSDDP)
        dadosSDDP_Armazenamento.__init__(self, caminhoSDDP)
        self.mapaAbreviacoes = { "SUDESTE" : "SE", "NORDESTE" : "NE" , "NORTE" : "NO" , "SUL" : "SU", "NOFICT1": "NI" }
        self.caminhoSDDP = caminhoSDDP
        self.nomeCaso = nome
        print("Carregou caso SDDP ", self.caminhoSDDP)

    @property
    def caminho(self):
        return self.caminhoSDDP

    @property
    def nome(self):
        return self.nomeCaso

    @property
    def estagio(self):
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_gerhid_MW.csv").tabela["estagio"].tolist()

#    def produtibilidade(self, nomeUsina):
#        gh = self.geracaoHidreletricaUsina(nomeUsina)
#        turb = self.vazaoTurbinadaUsina(nomeUsina)
#        print(gh)
#        print(turb)
#        print(gh/turb)
#        return gh/turb


    def intercambio(self, submercadoDE, submercadoPARA):     
        buscaColuna = self.mapaAbreviacoes[submercadoDE]+"->"+self.mapaAbreviacoes[submercadoPARA]
        return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_intercambio_MW.csv").tabela[buscaColuna]

    def intercambioTotalSubmercado(self, submercado):
        table = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_intercambio_MW.csv").tabela
        estagios = self.estagio.tolist()
        valores = [0]*len(estagios)        
        for subm in self.mapaAbreviacoes:
            abvDE = self.mapaAbreviacoes[submercado]
            abvPARA = self.mapaAbreviacoes[subm]
            buscaColunaPositiva = abvDE+"->"+abvPARA
            buscaColunaNegativa = abvPARA+"->"+abvDE
            if(buscaColunaPositiva in table.columns ):
                lista = table[buscaColunaPositiva].tolist()
                for i in range(0, len(estagios)):
                    valores[i] += lista[i]
                
            if(buscaColunaNegativa in table.columns ):
                lista = table[buscaColunaNegativa].tolist()
                for i in range(0, len(estagios)):
                    valores[i] -= lista[i]

        return valores
    

    
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