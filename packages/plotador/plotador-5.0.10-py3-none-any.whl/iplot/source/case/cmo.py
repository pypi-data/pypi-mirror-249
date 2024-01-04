from iplot.source.go.goGrafico import goGrafico
class buscaCMO():

    def __init__(self):
        pass

    def interpreta(self, classe, mneumonico, string):
        if(mneumonico == "cmo"):
            return (classe.cmo(string), "MWh/R$")
        else:
            return 0


"""     def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "cmo"):
            return goGrafico(classe.cmo(string), classe.estagio, "MWh/R$", None, cor, legenda, tipoGrafico)
        else:
            return 0 """
