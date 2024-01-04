from iplot.source.go.goGrafico import goGrafico
class buscaVazao():

    def __init__(self):
        pass


    def interpreta(self, classe, mneumonico, string):
        if(mneumonico == "qafl"):
            return (classe.vazaoAfluente(string), "m3s")
        elif(mneumonico == "qinc"):
            return (classe.vazaoIncremental(string), "m3s")
        elif(mneumonico == "qdef"):
            return (classe.vazaoDefluente(string), "m3s")
        elif(mneumonico == "qdefmin"):
            return (classe.vazaoDefluenteMinima(string), "m3s")
        elif(mneumonico == "qturb"):
            return (classe.vazaoTurbinada(string), "m3s")
        elif(mneumonico == "qvert"):
            return (classe.vazaoVertida(string), "m3s")
        elif(mneumonico == "qinc_cen"):
            return (classe.vazaoIncremental_Serie(string), "m3s")
        
        else:
            return 0

"""     def interpreta(self, classe, legenda, mneumonico, cor, string , tipoGrafico):
        if(mneumonico == "qafl"):
            return goGrafico(classe.vazaoAfluente(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qinc"):
            return goGrafico(classe.vazaoIncremental(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qdef"):
            return goGrafico(classe.vazaoDefluente(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qdefmin"):
            return goGrafico(classe.vazaoDefluenteMinima(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qturb"):
            return goGrafico(classe.vazaoTurbinada(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qvert"):
            return goGrafico(classe.vazaoVertida(string), classe.estagio, "m3s", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "qinc_cen"):
            return goGrafico(classe.vazaoIncremental_Serie(string), None, "m3s", None, cor, legenda, tipoGrafico)
        
        else:
            return 0 """
