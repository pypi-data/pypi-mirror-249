
import pandas as pd
import sys
import csv
from iplot.modelo.EstruturasGerais import estruturasGerais
import numpy as np
import math as mth
class dadosSADHI(estruturasGerais):

    def __init__(self, caminhoOperacao, nome):
        self.nomeCaso = nome
        self.caminhoOperacao = caminhoOperacao
        estruturasGerais.__init__(self)
        self.listaUsinasNordeste = ["BOA ESPERANÇA" ,	"ITAPARICA" ,	"ITAPEBI", "MOXOTO" ,	"P. AFONSO 1,2,3" ,	"P. AFONSO 4" ,	"PEDRA DO CAVALO" ,	"SOBRADINHO" , "XINGO"]
        self.listaUsinasNorte = ["BALBINA", "BELO MONTE", "CACHOEIRA CALDEIRAO", "COARACY NUNES", "CURUA-UNA", "ESTREITO", "FERREIRA GOMES", "PIMENTAL", "STO ANTONIO DO JARI", "TUCURUI"]
        self.listaUsinasSul = ["14 DE JULHO","BAIXO IGUACU","BARRA GRANDE","CACHOEIRINHA","CAMPOS NOVOS", "CANASTRA", "CASTRO ALVES",
                                "D. FRANCISCA", "FOZ CHAPECO", "FUNDÃO", "G. B. MUNHOZ", "G. P. SOUZA", "GARIBALDI", "ITÁ", "ITAUBA",
                                "JACUI", "JULIO M.FILHO", "MACHADINHO", "MAUA", "MONJOLINHO" , "MONTE CLARO", "PASSO FUNDO" ,"PASSO REAL",
                                "PASSO SAO JOAO", "QUEBRA QUEIXO", "S. G.CHOPIM", "SALTO CAXIAS", "SALTO OSORIO", "SALTO PILAO", "SALTO SANTIAGO",
                                "SANTA CLARA-PR", "SAO JOAO", "SAO JOSE", "SAO ROQUE", "SEGREDO", "TIBAGI MONTANTE"]
        self.listaUsinasSudeste = [ "A. VERMELHA", "AIMORES", "B. BONITA", "B.COQUEIROS", "BAGUARI", "BARIRI", "BARRA BRAUNA", "BATALHA", "C. DOURADA", 
        "C.BRANCO-1", "C.BRANCO-2", "C.MAGALHAES", "CACONDE","CACU","CAMARGOS","CANA BRAVA","CANDONGA","CANOAS I","CANOAS II","CAPANEMA","CAPIVARA","CHAVANTES","COLIDER",
        "CORUMBA","CORUMBA-3","CORUMBA-4","DARDANELOS","E. DA CUNHA","EMBORCAÇÃO","ESPORA","FONTES","FONTES AB","FONTES C","FOZ DO RIO CLARO","FUNIL","FUNIL-MG","FURNAS",
        "GUAPORE","GUILM. AMORIM","HENRY BORDEN","I. SOLTEIRA","IBITINGA","IGARAPAVA","ILHA POMBOS","IRAPE","ITAGUACU","ITAIPU TOTAL (BR+PY)","ITIQUIRA I","ITIQUIRA II",
        "ITUMBIARA","ITUMIRIM","ITUTINGA","JAGUARA","JAGUARI","JAURU","JIRAU","JUPIA","JURUMIRIM","L. C. BARRETO","LAJEADO","LIMOEIRO","M. MORAES","MANSO","MARIMBONDO",
        "MASCARENHAS","MIRANDA","N. AVANHANDAVA","NILO PEÇANHA","NOVA PONTE","OLHO DAGUA","OURINHOS","P. COLOMBIA","PARAIBUNA","PARANAPANEMA","PEIXE ANGICAL","PEREIRA PASSOS",
        "PICADA","PIRAJU","PONTE DE PEDRA","PORTO ESTRELA","PORTO PRIMAVERA","PROMISSÃO","QUEIMADO","RETIRO BAIXO","RONDON II","ROSAL","ROSANA","S.DO FACÃO","S.R.VERDINHO",
        "SA CARVALHO","SALTO","SALTO APIACAS","SALTO GRANDE CM","SALTO GRANDE CS","SAMUEL","SANTA BRANCA","SANTA ISABEL","SANTO ANTONIO","SAO DOMINGOS","SAO DOMINGOS GO",
        "SAO JERONIMO","SAO MANOEL","SAO SALVADOR","SÃO SIMÃO","SERRA DA MESA","SIMPLICIO","SINOP","SOBRAGI","STA.CLARA-MG","SUIÇA","TAQUARUÇU","TELES PIRES","TRÊS IRMÃOS",
        "TRÊS MARIAS","VOLTA GRANDE"]
        self.dicionarioUsinas ={ "CORUMBA IV" : "CORUMBA-4",
                                "CACONDE" : "CACONDE", "PARAIBUNA":"PARAIBUNA", "RETIRO BAIXO":"RETIRO BAIXO","QUEIMADO":"QUEIMADO", "TRES MARIAS":"TRÊS MARIAS",
                                "SERRA MESA":"SERRA DA MESA", "BALBINA":"BALBINA", "SINOP":"SINOP", "RONDON II":"RONDON II", "CURUA-UNA":"CURUA-UNA", "CAMARGOS":"CAMARGOS",
                                "BATALHA":"BATALHA", "NOVA PONTE":"NOVA PONTE", "FURNAS":"FURNAS", "EMBORCACAO":"EMBORCAÇÃO", "TUCURUI":"TUCURUI", "ITAPARICA":"ITAPARICA",
                                "MACHADINHO":"MACHADINHO", "SLT.SANTIAGO":"SALTO SANTIAGO", "I. SOLTEIRA":"I. SOLTEIRA", "A. VERMELHA":"A. VERMELHA", "P. PRIMAVERA": "PORTO PRIMAVERA",
                                "JUPIA":"JUPIA", "BELO MONTE":"BELO MONTE", "SOBRADINHO":"SOBRADINHO", "ITAPARICA":"ITAPARICA", "ITAIPU":"ITAIPU TOTAL (BR+PY)", "ESPORA":"ESPORA",
                                "SLT VERDINHO":"S.R.VERDINHO", "FOZ R. CLARO":"FOZ DO RIO CLARO", "SAO SIMAO":"SÃO SIMÃO", "NAVANHANDAVA":"N. AVANHANDAVA", "CANDONGA":"CANDONGA",
                                "XINGO":"XINGO", "COMP PAF-MOX":"MOXOTO"
    
        }

    @property
    def caminho(self):
        return self.caminhoOperacao
    
    @property
    def nome(self):
        return self.nomeCaso

    @property
    def estagio(self):
        #return list(range(1, 33))
        df = pd.DataFrame({"valor": list(range(1, len(self.vazaoVertida(None)) +1))})
        return df["valor"]
    
    def retornaDFValoresSubmercado(self,identificador, arquivo):
        df = pd.read_csv(self.caminhoOperacao+'/'+arquivo)
        dfSIN = df[df.columns[1:]]
        emptyDf= pd.DataFrame()
        listaSBM = []
        if(identificador == "NORDESTE"):
            listaSBM = self.listaUsinasNordeste
        if(identificador == "NORTE"):
            listaSBM = self.listaUsinasNorte
        if(identificador == "SUL"):
            listaSBM = self.listaUsinasSul
        if(identificador == "SUDESTE"):
            listaSBM = self.listaUsinasSudeste

        for usina in listaSBM:
            if(pd.isna(df[usina].tolist()[1]) is not True ):
                valores = []
                for elemento in df[usina].tolist():
                    if(pd.isna(elemento)):
                        elemento = '0'
                    if(self.is_number(elemento)):
                        valores.append(float(elemento))
                #df_temp = pd.DataFrame(valores)
                #emptyDf[usina] = df_temp
                #emptyDf.insert(0, usina, valores)
                df_temp = pd.DataFrame({usina: valores})
                emptyDf = pd.concat([emptyDf, df_temp], axis =1)
        return emptyDf.sum(axis = 1)
        
    def retornaDFValoresSIN(self,arquivo):
        df = pd.read_csv(self.caminhoOperacao+'/'+arquivo)
        dfSIN = df[df.columns[1:]]
        emptyDf= pd.DataFrame()
        for column in dfSIN:
            if(pd.isna(df[column].tolist()[1]) is not True ):
                valores = []
                for elemento in df[column].tolist():
                    if(pd.isna(elemento)):
                        elemento = '0'
                    if(self.is_number(elemento)):
                        valores.append(float(elemento))
                #df_temp = pd.DataFrame(valores)
                #emptyDf[str(column)] = df_temp
                #emptyDf.insert(0, str(column), valores)
                df_temp = pd.DataFrame({str(column): valores})
                emptyDf = pd.concat([emptyDf, df_temp], axis =1)
        return emptyDf.sum(axis = 1)
    
    def is_number(self, string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def retornaDFValoresUsina(self, usina, arquivo):
        usina = self.dicionarioUsinas[usina]
        df = pd.read_csv(self.caminhoOperacao+'/'+arquivo)
        dfUsina = df[usina].tolist()
        valores = []
        for elemento in dfUsina:
            if(self.is_number(elemento)):
                valores.append(float(elemento))
        data = pd.DataFrame({"valores": valores})
        return data["valores"]
        
    def vazaoVertida(self, identificador):
        if(identificador is None):
            return self.retornaDFValoresSIN('vazao_vertida_mensal.csv')
        if(identificador in self.listaSubmercados):
            #print("SUBMERCADO NAO ESTA IMPLEMENTADO NA OPERACAO")
            return self.retornaDFValoresSubmercado(identificador, 'vazao_vertida_mensal.csv')
        else:
            return self.retornaDFValoresUsina(identificador, 'vazao_vertida_mensal.csv')
          
    def vazaoDefluente(self, identificador):
        if(identificador is None):
            return self.retornaDFValoresSIN('vazao_defluente_mensal.csv')
        if(identificador in self.listaSubmercados):
            return self.retornaDFValoresSubmercado(identificador, 'vazao_defluente_mensal.csv')
        else:
            return self.retornaDFValoresUsina(identificador, 'vazao_defluente_mensal.csv')

    def geracaoHidreletrica(self, identificador):
        if(identificador is None):
            return self.retornaDFValoresSIN('geracao_hidreletrica_mensal.csv')
        if(identificador in self.listaSubmercados):
            return self.retornaDFValoresSubmercado(identificador, 'geracao_hidreletrica_mensal.csv')
        else:
            value = self.retornaDFValoresUsina(identificador, 'geracao_hidreletrica_mensal.csv')
            return value
        
        

    def vazaoTurbinada(self, identificador):
        if(identificador is None):
            vazao_vertida_SIN = self.retornaDFValoresSIN('vazao_vertida_mensal.csv')
            vazao_defluente_SIN = self.retornaDFValoresSIN('vazao_defluente_mensal.csv')
            #vazaoTurbinada_SIN = vazao_defluente_SIN - vazao_vertida_SIN
            return vazao_defluente_SIN - vazao_vertida_SIN
            #vazaoTurbinada_SIN = []
            #for indice in range(len(vazao_vertida_SIN)):
            #    vazaoTurbinada_SIN.append(vazao_defluente_SIN[indice] - vazao_vertida_SIN[indice])
            #return  pd.DataFrame(vazaoTurbinada_SIN)
        if(identificador in self.listaSubmercados):
            vazao_vertida_SBM = self.retornaDFValoresSubmercado(identificador, 'vazao_vertida_mensal.csv')
            vazao_defluente_SBM = self.retornaDFValoresSubmercado(identificador, 'vazao_defluente_mensal.csv')
            return vazao_defluente_SBM - vazao_vertida_SBM
            #vazaoTurbinada_SBM = []
            #for indice in range(len(vazao_vertida_SBM)):
            #    vazaoTurbinada_SBM.append(vazao_defluente_SBM[indice] - vazao_vertida_SBM[indice])
            #return  pd.DataFrame(vazaoTurbinada_SBM)
        else:
            vazao_vertida_USI = self.retornaDFValoresUsina(identificador, 'vazao_vertida_mensal.csv')
            vazao_defluente_USI = self.retornaDFValoresUsina(identificador, 'vazao_defluente_mensal.csv')
            return vazao_defluente_USI - vazao_vertida_USI
            #vazaoTurbinada_USI = []
            #for indice in range(len(vazao_vertida_USI)):
            #    vazaoTurbinada_USI.append(vazao_defluente_USI[indice] - vazao_vertida_USI[indice])
            #return  pd.DataFrame(vazaoTurbinada_USI    )
        
    def fphaUtilizada(self, identificador):
        if(identificador is None):
            vazaoTurbinada_SIN = self.vazaoTurbinada(identificador=None)
            geracaoHidreletrica_SIN = self.retornaDFValoresSIN('geracao_hidreletrica_mensal.csv')
            return geracaoHidreletrica_SIN/vazaoTurbinada_SIN
            #fpha_SIN = []
            #for indice in range(len(vazaoTurbinada_SIN)):
            #    fpha_SIN.append(geracaoHidreletrica_SIN[indice]/vazaoTurbinada_SIN[indice])
            #return  pd.DataFrame(fpha_SIN)
        if(identificador in self.listaSubmercados):
            vazaoTurbinada_SBM = self.vazaoTurbinada(identificador=identificador)
            geracaoHidreletrica_SBM = self.retornaDFValoresSubmercado(identificador, 'geracao_hidreletrica_mensal.csv')
            return geracaoHidreletrica_SBM/vazaoTurbinada_SBM
            #fpha_SBM = []
            #for indice in range(len(vazaoTurbinada_SBM)):
            #    fpha_SBM.append(geracaoHidreletrica_SBM[indice]/vazaoTurbinada_SBM[indice])
            #return  pd.DataFrame(fpha_SBM)
        else:
            vazaoTurbinada_USI = self.vazaoTurbinada(identificador).tolist()
            geracaoHidreletrica_USI = self.retornaDFValoresUsina(identificador, 'geracao_hidreletrica_mensal.csv').tolist()
            fpha_SIN = []
            for indice in range(len(vazaoTurbinada_USI)):
                if(vazaoTurbinada_USI[indice] == 0):
                    fpha_SIN.append(0)
                else:
                    fpha_SIN.append(geracaoHidreletrica_USI[indice]/vazaoTurbinada_USI[indice])
            df = pd.DataFrame({"valor":fpha_SIN})
            return df["valor"]

    def volumeVertido(self, identificador):
        qVert = self.vazaoVertida(identificador)
        vVert = qVert*2.63
        return vVert
        #vVert = []
        #for elemento in qVert:
        #    vVert.append(elemento*2.63)
        #    dfVert = pd.DataFrame(vVert)
        #return dfVert
    def volumeDefluente(self, identificador):
        qDefl = self.vazaoDefluente(identificador)
        vDefl = qDefl*2.63
        return vDefl
        #vDefl = []
        #for elemento in qDefl:
        #    vDefl.append(elemento*2.63)
        #    dfDefl = pd.DataFrame(vDefl)
        #return dfDefl

    def vazaoDefluenteMinima(self, identificador):
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]


    def vazaoIncremental(self, identificador):
        if(identificador is None):
            return self.retornaDFValoresSIN('vazaoIncremental_mensal.csv')
        if(identificador in self.listaSubmercados):
            return self.retornaDFValoresSubmercado(identificador, 'vazaoIncremental_mensal.csv')
        else:
            return self.retornaDFValoresUsina(identificador, 'vazaoIncremental_mensal.csv')
    
    def volumeIncremental(self, identificador):
        qIncr = self.vazaoIncremental(identificador)
        vIncr = qIncr*2.63
        return vIncr
        #vIncr = []
        #for elemento in qIncr.tolist():
        #    vIncr.append(elemento*2.63)
        #return pd.DataFrame(vIncr)
    

    def volumeFinalPercentual(self, identificador):
    #    if(identificador is None):
    #        return self.retornaListaValoresSIN('volumeUtilPercent_mensal.csv')
    #    if(identificador in self.listaSubmercados):
    #        return self.retornaListaValoresSubmercado(identificador, 'volumeUtilPercent_mensal.csv')
    #    else:
    #        return self.retornaListaValoresUsina(identificador, 'volumeUtilPercent_mensal.csv')
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]
        
    

    def volumeUtilFinal(self, identificador):
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]
    def volumeUtilInicial(self, identificador):
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]

    def cmo(self, identificador):
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]
    
    def geracaoTermica(self, identificador):
        df = pd.read_csv(self.caminhoOperacao+"/geracao_termica_mensal.csv")
        dfSIN = df[df.columns[1:]]
        emptyDf= pd.DataFrame()
        for column in dfSIN:
            if(pd.isna(df[column].tolist()[1]) is not True ):
                valores = []
                for elemento in df[column].tolist():
                    if(pd.isna(elemento)):
                        elemento = '0'
                    if(self.is_number(elemento)):
                        valores.append(float(elemento))
                #df_temp = pd.DataFrame(valores)
                #emptyDf[str(column)] = df_temp
                #emptyDf.insert(0, str(column), valores)
                df_temp = pd.DataFrame({str(column): valores})
                emptyDf = pd.concat([emptyDf, df_temp], axis =1)
        if(identificador is None):
            return emptyDf["SIN"]
        if(identificador in self.listaSubmercados):
            return emptyDf[identificador]
        else:
            df = pd.DataFrame({"valor": [0]})
            return df["valor"]
    def volumeTurbinado(self, identificador):
        qTurb = self.vazaoTurbinada(identificador)
        vTurb = qTurb*2.63
        return vTurb
        #vTurb = []
        #for elemento in qTurb.tolist():
        #    vTurb.append(elemento*2.63)
        #return pd.DataFrame(vTurb)

    def volumeAfluente(self, identificador):
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]
    def vazaoAfluente(self, identificador):
        df = pd.DataFrame({"valor": [0]})
        return df["valor"]