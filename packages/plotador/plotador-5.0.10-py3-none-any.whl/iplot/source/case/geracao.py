from iplot.source.go.dadoEixo import DadoEixo
class buscaGeracao():

    def __init__(self):
        pass

#    def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
#        if(mneumonico == "gh"):
#            return goGrafico(classe.geracaoHidreletrica(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
#        elif(mneumonico == "gt"):
#            return goGrafico(classe.geracaoTermica(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
#        elif(mneumonico == "fph"):
#            return goGrafico(classe.fphaUtilizada(string), classe.estagio, "MW/m3/s", None, cor, legenda, tipoGrafico)
#        else:
#            return 0


    def interpreta(self, classe, mneumonico, string):
        print("string: ", string)
        if(mneumonico == "gh"):
            return (classe.geracaoHidreletrica(string), "MW")
        elif(mneumonico == "gt"):
            return (classe.geracaoTermica(string), "MW")
        elif(mneumonico == "fph"):
            return (classe.fphaUtilizada(string), "MW/m3/s")
        elif(mneumonico == "est"):
            return (classe.estagio, "estagios")
        elif(mneumonico == "iter"):
            return (classe.iter, "iteracoes")

        
        else:
            return 0