
import plotly.graph_objects as go
class goGrafico():
    def __init__(self, y, x, yaxis, xaxis, cor, legenda):
       self.y = y 
       self.x = x
       self.yaxis = yaxis
       self.xaxis = xaxis
       self.cor  = cor
       self.legenda = legenda
       self.GO = None

    def setGOObject(self, GO):
       self.GO = GO

    def returnGoObject(self):
       return self.GO

