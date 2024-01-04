from iplot.source.go.goGrafico import goGrafico

class buscaConvergencia():

    def __init__(self):
        pass


    def interpreta(self, classe, mneumonico):
        if(mneumonico == "zinf"):
            return (classe.zinf, "R$")
        if(mneumonico == "cpuTime"):
            
            return (classe.cpuTime, "1000R$")
        else:
            return 0

"""     def interpreta(self, classe, legenda, mneumonico, cor, tipoGrafico):
        if(mneumonico == "zinf"):
            return goGrafico(classe.zinf, classe.iter, "R$", None, cor, legenda, tipoGrafico)
        if(mneumonico == "cpuTime"):
            
            return goGrafico(classe.cpuTime, classe.iter, "1000R$", None, cor, legenda, tipoGrafico)
        else:
            return 0 """
    