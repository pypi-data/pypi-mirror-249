from iplot.modelo.SDDP import dadosSDDP
from iplot.modelo.Newave import dadosNewave
from iplot.modelo.SADHI import dadosSADHI
import os
class gerenciadorArquivos():

    def __init__(self):
        self.__mapaCasos = {}
        self.bancoCores = [ "#ffa600", "#0c255c", "#f76047", "#4b335b" , "red", "black", "blue" , "gray", "green", "magenta"] 
        self.__mapaCores = {} # #fc3a52
        self.__mapaNomes = {} # #fc3a52
        self.listaCasosNewave = []
        self.listaCasosSDDP = [] #"#870A28", "#00613C", 
        self.contador = 0
          
    def add(self, path, nome, color = None):
        
        if(os.path.exists(path+"/SIN")):
            caso = dadosSDDP(path, nome)
            self.listaCasosSDDP.append(path)
        else:
            caso = dadosNewave(path, nome)
            self.listaCasosNewave.append(path)
        self.__mapaCasos[nome] = caso
        #self.__mapaNomes[path] = nome
        self.configuracao(nome,color)


    def addSADHI(self, path, color = None, nome = None):
        caso = dadosSADHI(path, nome)
        self.__mapaCasos[nome] = caso
        #self.__mapaNomes[path] = nome
        self.configuracao(nome,color)
        
    def configuracao(self, caminhoCompletoCaso,cor):
        idCor = self.bancoCores[self.contador] if cor is None else cor
        self.__mapaCores[caminhoCompletoCaso] = idCor
        if cor is None: self.contador += 1
        return cor
    

    @property
    def mapaCores(self):
        return self.__mapaCores
    
    @property
    def mapaCasos(self):
        return self.__mapaCasos
    
    @property
    def mapaNomes(self):
        return self.__mapaNomes

    def getClasse(self, nome):
        return self.__mapaCasos[nome]
    
    #def getNome(self, nome):
    #    return self.__mapaNomes[nome]