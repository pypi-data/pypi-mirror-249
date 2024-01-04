from iplot.source.go.dadoEixo import DadoEixo

class buscaVolume():

    def __init__(self):
        pass



    def interpreta(self, classe, mneumonico, string):
        if(mneumonico == "vturb"):
            return (classe.volumeTurbinado(string), "hm3")
        elif(mneumonico == "vvert"):
            return (classe.volumeVertido(string), "hm3")
        elif(mneumonico == "vafl"):
            return (classe.volumeAfluente(string), "hm3")
        elif(mneumonico == "vinc"):
            return (classe.volumeIncremental(string), "hm3")
        elif(mneumonico == "vdef"):
            return (classe.volumeDefluente(string), "hm3")
        elif(mneumonico == "vagua"):
            return (classe.valorAgua(string), "unidade")
        elif(mneumonico == "vaguai"):
            return (classe.valorAguaI(string), "unidade")
        elif(mneumonico == "vinc_cen"):
            return (classe.volumeIncremental_Serie(string), "hm3")
        else:
            return 0


"""     def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "vturb"):
            return goGrafico(classe.volumeTurbinado(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vvert"):
            return goGrafico(classe.volumeVertido(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vafl"):
            return goGrafico(classe.volumeAfluente(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vinc"):
            return goGrafico(classe.volumeIncremental(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vdef"):
            return goGrafico(classe.volumeDefluente(string), classe.estagio, "hm3", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vagua"):
            return goGrafico(classe.valorAgua(string), classe.estagio, "unidade", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vaguai"):
            return goGrafico(classe.valorAguaI(string), classe.estagio, "unidade", "estagios", cor, legenda, tipoGrafico)
        elif(mneumonico == "vinc_cen"):
            return goGrafico(classe.volumeIncremental_Serie(string), None, "hm3", None, cor, legenda, tipoGrafico)
        else:
            return 0 """
    