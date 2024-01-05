
from iplot.source.go.goGrafico import goGrafico
from iplot.source.interpretador import interpretador
class frame():
    def __init__(self, formulax, formulay, linha, coluna, grafico, gerenciadorArquivos, corFrame, frameTitle, nome, mostra):
       self.formulax = formulax
       self.formulay = formulay
       self.linha = linha
       self.coluna = coluna
       self.listaGO = []
       self.titulo = None
       self.grafico = grafico
       self.gerenciadorArquivos = gerenciadorArquivos
       self.corFrame = corFrame
       self.frameTitle = frameTitle
       self.nome = nome
       self.mostra = mostra
       self.setListaGO()

    def addListaGO(self, GO):
        self.listaGO.append(GO)
    
    def setListaGO(self):
        self.listaGO = interpretador().retornaListasGO(self, self.gerenciadorArquivos)

    def getListaGO(self):
        return self.listaGO
        
    def getTitulo(self):
        self.titulo = self.formulay if self.frameTitle is None else self.frameTitle
        return self.titulo

    #def 