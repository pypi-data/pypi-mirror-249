
from isddp.sddp import LeituraPersonalizadaSDDP
from iplot.modelo.EstruturasGerais import estruturasGerais


class dadosSDDP_Armazenamento(estruturasGerais):

    def __init__(self, caminhoSDDP):
        self.caminhoSDDP = caminhoSDDP

        self.__volMin = None
        self.__volUtilInicial = None
        estruturasGerais.__init__(self)



    def volumeUtilFinal(self, identificador):
        if(identificador is None):
            volumeFinalSIN = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_volfin_hm3.csv").tabela["valor"]
            volmin = self.volumeMinimo(identificador)
            vfinalutil = volumeFinalSIN - volmin
            #listaVUtilFIM = vfinalutil.tolist()
            #vinicialUtil = self.volumeUtilInicialSIN[0]        
            #listaVUtilFIM.insert(0, vinicialUtil)
            return vfinalutil
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            volumeFinalSubmercado = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_volfin_hm3.csv").tabela[identificador]
            volmin = self.volumeMinimo(identificador)
            vfinalutil = volumeFinalSubmercado - volmin
            #listaVUtilFIM = vfinalutil.tolist()
            #vinicialUtil = self.volumeUtilInicialSubmercado(nomeSubmercado).tolist()[0]        
            #listaVUtilFIM.insert(0, vinicialUtil)
            return vfinalutil
        else:
            identificador = identificador.replace(" ", "")
            volumeFinalUsina = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_volfin_hm3.csv").tabela[identificador]
            volmin = self.volumeMinimo(identificador)
            vfinalutil = volumeFinalUsina - volmin
            #listaVUtilFIM = vfinalutil.tolist()
            #vinicialUtil = self.volumeUtilInicialUsina(nomeUsina).tolist()[0]        
            #listaVUtilFIM.insert(0, vinicialUtil)
            return vfinalutil



    def volumeUtilInicial(self, identificador):
        if(identificador is None):
            volumeInicialSIN = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_volini_hm3.csv").tabela["valor"]
            volmin = self.volumeMinimo(identificador)
            df = (volumeInicialSIN - volmin)
            return df
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            volumeInicialSubmercado = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_volini_hm3.csv").tabela[identificador]
            volmin = self.volumeMinimo(identificador)
            return volumeInicialSubmercado - volmin
        else:
            identificador = identificador.replace(" ", "")
            if (self.__volUtilInicial is None):
                self.__volUtilInicial = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_volini_hm3.csv").tabela
            volumeInicialUsina = self.__volUtilInicial[identificador]
            volmin = self.volumeMinimo(identificador)
            return volumeInicialUsina - volmin



    def volumeMinimo(self, identificador):
        if(identificador is None):
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/SIN/per_SIN_volmin_hm3.csv").tabela["valor"]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Submercado/per_sbm_volmin_hm3.csv").tabela[identificador]
        else:
            identificador = identificador.replace(" ", "")
            if( self.__volMin is None):
                self.__volMin = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_volminreserv_hm3.csv").tabela
            return self.__volMin[identificador]



    def volumeMaximoOperativo(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return 0
        else:
            identificador = identificador.replace(" ", "")
            return LeituraPersonalizadaSDDP.read( self.caminhoSDDP+"/Usina/per_usi_volmaxreserv_hm3.csv").tabela[identificador]

    
    def volumeFinalPercentual(self, identificador):
        if(identificador is None):
            return [0]
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return [0]
        else:
            identificador = identificador.replace(" ", "")
            per_usi_volfinvu_percentual = LeituraPersonalizadaSDDP.read(self.caminhoSDDP+"/Usina/per_usi_volfinvu_percentual.csv").tabela[identificador]
            return per_usi_volfinvu_percentual        


    
    def volumeInicialPercentual(self, identificador):
        if(identificador is None):
            return 0
        if(identificador in self.listaSubmercados):
            identificador = identificador.replace(" ", "")
            return 0
        else:
            identificador = identificador.replace(" ", "")
            return 0
    
