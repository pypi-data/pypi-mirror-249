
from iplot.layout.Layout_Plot_Personalizado import LayoutPlotPersonalizado
from iplot.layout.Layout_Plot_Diff import LayoutPlotDiff

from iplot.source.interpretador import interpretador
from iplot.source.figure import Figura
from iplot.examples.cascata import GeraCascata
from iplot.examples.usina import GeraUsina
from iplot.examples.sin import GeraSIN
from iplot.examples.submercado import GeraSubmercado
from iplot.examples.boxplot import GeraBoxplot
from iplot.examples.plot import GeraPlotSimples
from iplot.examples.plotRapido import GeraPlotRapido
from iplot.examples.intercambios import GeraIntercambios
from iplot.source.gerenciadorArquivos import gerenciadorArquivos

from iplot.examples.baraglut import GeraBarAglut
class iPlot():

    def __init__(self, nomeAnalise):
        self.nomeAnalise = nomeAnalise
        self.gerenciador = gerenciadorArquivos()
        self.mapaNomeFiguras = {}
        interpretador().help()

    def help(self):
        interpretador().help()
                
    def add(self, path, nome, color = None):
        self.gerenciador.add(path = path, color = color, nome = nome)
        
    def addSADHI(self, path, nome,  color = None):
        self.gerenciador.addSADHI(path = path, color = color, nome = nome)








    def figure(self, figure):
        figura = Figura(figure)
        self.mapaNomeFiguras[figure] = figura

    #def add_frame(self, figure, key, lin = 1, col = 1, identificator= None):
    #    self.mapaNomeFiguras[figure].createFrame(key, identificator, lin, col, self.gerenciador)


    def add_frame(self, figure, formulax, formulay, lin = 1, col = 1, grafico = "plot", corFrame = None, frameTitle = None, nome = None, mostra = True):

        self.mapaNomeFiguras[figure].createFrame(formulax, formulay, lin, col, self.gerenciador, grafico, corFrame, frameTitle, nome, mostra)


    def show(self, figure, layout = "personalizado" ,  tituloGrafico = None):
        tituloGrafico = self.mapaNomeFiguras[figure].titulo+"_"+self.nomeAnalise if tituloGrafico is None else tituloGrafico
        if(len(self.mapaNomeFiguras[figure].listaFrames) == 0):
            print("NAO FORAM CADASTRADOS PLOTS PERSONALIZADOS")
            exit(1)

        if(layout == "personalizado"):
            LayoutPlotPersonalizado(self.mapaNomeFiguras[figure],  tituloGrafico)
        elif(layout == "diff"):
            LayoutPlotDiff(self.mapaNomeFiguras[figure],  tituloGrafico)







 


    def plot(self, key , sameGraph = None, id = None, title = None):
        GeraPlotSimples(self, key, sameGraph, id, title)
    def boxPlot(self, key, id = None, title = None):
        GeraBoxplot(self, key, id, title)
    def df_plot(self, y, x = None, legend = None, title= None):
        GeraPlotRapido(y, x, legend, title)
    def intercambios(self, title = None):
        GeraIntercambios(self, title)
    def submercado(self, submercado, title = None):
        GeraSubmercado(self, submercado, title)
    def cascata(self, nomeCascata, key, title = None):
        GeraCascata(self, nomeCascata, key, title)
    def usina(self,usina, title = None):
        GeraUsina(self, usina, title)
    def sin(self, title = None):
        GeraSIN(self, title)
    def barAglut(self, title = None):
        GeraBarAglut(self, title)