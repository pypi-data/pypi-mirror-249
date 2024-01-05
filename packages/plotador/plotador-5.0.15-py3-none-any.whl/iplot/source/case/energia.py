from iplot.source.go.goGrafico import goGrafico

class buscaEnergia():

    def __init__(self):
        pass

    def interpreta(self, classe, mneumonico, string):
        if(mneumonico == "earm"):
            return (classe.earm(string), "MW")
        elif(mneumonico == "ever"):
            return (classe.enevert(string), "MW")
        elif(mneumonico == "eafl"):
            return (classe.enaflu(string), "MW")
            #ADICIONAR MNEUMONICO DE VVER_SBM, VFIM_SBM, VAFL_SBM, VDEF_SBM
        elif(mneumonico == "enaflu_cen"):
            return (classe.enaflu_Serie(string), "MW")
        else:
            return 0

"""     def interpreta(self, classe, legenda, mneumonico, cor, string, tipoGrafico):
        if(mneumonico == "earm"):
            return goGrafico(classe.earm(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
        elif(mneumonico == "ever"):
            return goGrafico(classe.enevert(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
        elif(mneumonico == "eafl"):
            return goGrafico(classe.enaflu(string), classe.estagio, "MW", None, cor, legenda, tipoGrafico)
            #ADICIONAR MNEUMONICO DE VVER_SBM, VFIM_SBM, VAFL_SBM, VDEF_SBM
        elif(mneumonico == "enaflu_cen"):
            return goGrafico(classe.enaflu_Serie(string), None, "MW", None, cor, legenda, tipoGrafico)
        else:
            return 0 """
