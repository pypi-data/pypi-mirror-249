from iplot.source.case.armazenamento import buscaArmazenamento
from iplot.source.case.cmo import buscaCMO
from iplot.source.case.convergencia import buscaConvergencia
from iplot.source.case.energia import buscaEnergia
from iplot.source.case.geracao import buscaGeracao
from iplot.source.case.intercambio import buscaIntercambio
from iplot.source.case.vazao import buscaVazao
from iplot.source.case.volume import buscaVolume
from iplot.source.go.goGrafico import goGrafico
from iplot.source.go.dadoEixo import DadoEixo
import plotly.graph_objects as go
import re
import pandas as pd
class interpretador():

    def __init__(self):
        self.__mneumonicos = [
                "varmfu", "varmiu" , "varpf", "varpi",
                "vturb", "vvert", "vdef", "vafl", "vinc", "vinc_cen", "vagua", "vaguai"
                "qinc", "qafl", "qdef", "qturb", "qvert", "qinc_cen","qdefmin",
                "gh", "gt", "cmo", 
                "earm", "evert", "enaflu", "enaflu_cen",
                "zinf", "interc", "fph", "cpuTime", "custos", "legend", "caso", "earpf" , "cop", "vdefmin"]
         #cpuTime
    def help(self):
        print(self.__mneumonicos)

    def mediaPeriodoSerie(self, df, aglut):
        lista = []
        
        numeroCenarios = max([eval(i) for i in df["cenario"].tolist()]) if isinstance(df["cenario"].tolist()[0], str) else max(df["cenario"].tolist())
        for serie in range(1,(numeroCenarios+1)):
            serie = str(serie) if isinstance(df["cenario"].tolist()[0], str) else serie
            lista.append(df.loc[(df["cenario"]==serie) & (df["estagio"] <= aglut)]["valor"].mean())
        return lista

    def separaFormulaEmChaveIdentificador(self, listaFormula):

        listaParesChaveIdentificador  = []
        for elemento in listaFormula:
            if("[" in elemento):
                identificador = elemento[elemento.find("[")+1:elemento.find("]")].strip()
            else:
                identificador = None
            chave = elemento.split("[")[0].strip()
            listaParesChaveIdentificador.append((chave.lower(),identificador))
        return listaParesChaveIdentificador
    
    
    def retornaListasGO(self, frame, gerenciadorArquivos):
        listaGO = []
        tipoGrafico = frame.grafico.strip()
        listaPar = self.separaFormulaEmChaveIdentificador([tipoGrafico])
        chave, parametros = listaPar[0]
        tipoGrafico = chave
        listaParametros = parametros if parametros is None else parametros.split(",")
        

        mapaGOCaso = {}
        for caso in gerenciadorArquivos.mapaCasos:
            cor = gerenciadorArquivos.mapaCores[caso]
            dadoEixoY = self.interpreta(gerenciadorArquivos.getClasse(caso), frame.formulay)
            dadoEixoX = self.interpreta(gerenciadorArquivos.getClasse(caso), frame.formulax)
            legenda = self.legenda(gerenciadorArquivos.getClasse(caso).caminho)
            #mapaGOCaso[caso] = goGrafico(parY[0], parX[0], parY[1], parX[1], cor, legenda)
            #listaGO.append(goGrafico(parY[0], parX[0], parY[1], parX[1], cor, legenda))
            if(tipoGrafico == "plot"):
                 ObjetoGO = goGrafico(dadoEixoY.dado, dadoEixoX.dado, dadoEixoY.eixo, dadoEixoX.eixo, cor, caso)
                 #nomeLegenda = legenda if gerenciadorArquivos.getNome(caso) is None else gerenciadorArquivos.getNome(caso)
                 ObjetoGO.GO = go.Scatter(x = dadoEixoX.dado, y = dadoEixoY.dado , name = caso, legendgroup= caso,line=dict(color=cor), showlegend=frame.mostra)
                 #mapaGOCaso[caso] = ObjetoGO
                 listaGO.append(ObjetoGO)
            if(tipoGrafico == "box"):
                if(listaParametros is None):
                    print("Nao foram escolhidos estagios para plotar o BOXPLOT")
                    exit(1)
                if(listaParametros is not None):
                    ylistaPlot = []
                    xlistaPlot = []
                    for estagio in listaParametros:
                        df = dadoEixoY.dado.loc[dadoEixoY.dado["estagio"] == int(estagio)]
                        ylistaPlot += df["valor"].tolist()
                        xlistaPlot += df["estagio"].tolist()


                    valY = ylistaPlot
                    valX = xlistaPlot
                    EixoX = "meses"
                    ObjetoGO = goGrafico(dadoEixoY.dado, dadoEixoX.dado, dadoEixoY.eixo, EixoX, cor, caso)
                    ObjetoGO.GO = go.Box(x = valX, y = valY, text=EixoX,     boxpoints= False, name = caso, legendgroup = caso, fillcolor = cor, marker_color = cor, showlegend=frame.mostra) #, mode='lines+markers+text'
                    #mapaGOCaso[caso] = ObjetoGO
                    listaGO.append(ObjetoGO)
            elif(tipoGrafico == "boxaglut"):
                
                if(listaParametros is None):
                    print("Aglutinacao BOXPLOT sem Parametros para aglutinar")
                    exit(1)
                if(listaParametros is not None):
                    ylistaPlot = []
                    xlistaPlot = []
                    for aglut in listaParametros:
                        lista = self.mediaPeriodoSerie(dadoEixoY.dado, int(aglut))
                        ylistaPlot += lista
                        xlistaPlot += [str(aglut)]*len(lista)
                    Valy = ylistaPlot
                    Valx = xlistaPlot
                    Eixox = "meses"
                    ObjetoGO = goGrafico(dadoEixoY.dado, dadoEixoX.dado, dadoEixoY.eixo, Eixox, cor, caso)
                    ObjetoGO.GO = go.Box(x = Valx, y = Valy, text=Valy,     boxpoints= False,  name = caso, legendgroup = caso, fillcolor = cor, marker_color = cor, showlegend=frame.mostra) #, mode='lines+markers+text'
                    #mapaGOCaso[caso] = ObjetoGO
                    listaGO.append(ObjetoGO)
            elif(tipoGrafico == "max"):
                ObjetoGO = goGrafico(dadoEixoY.dado, dadoEixoX.dado, dadoEixoY.eixo, dadoEixoX.eixo, cor, caso)
                ObjetoGO.GO = go.Scatter(x = dadoEixoX.dado, y = dadoEixoY.dado, name = caso, legendgroup=caso, mode = "markers", marker=dict(color=cor, size = 3), showlegend=False)
                #mapaGOCaso[caso] = ObjetoGO
                listaGO.append(ObjetoGO)
                return 
            elif(tipoGrafico == "min"):
                ObjetoGO = goGrafico(dadoEixoY.dado, dadoEixoX.dado, dadoEixoY.eixo, dadoEixoX.eixo, cor, caso)
                ObjetoGO.GO = go.Scatter(x = dadoEixoX.dado, y = dadoEixoY.dado, name = caso, legendgroup=caso,line=dict(color=cor, width = 1, dash = 'dash'), showlegend=False)
                #mapaGOCaso[caso] = ObjetoGO
                listaGO.append(ObjetoGO)
            else:
                ObjetoGO = goGrafico(dadoEixoY.dado, dadoEixoX.dado, dadoEixoY.eixo, dadoEixoX.eixo, cor, legenda)
                mapaGOCaso[caso] = ObjetoGO
        if(tipoGrafico == "bar"):
            listaX = []
            listaY = []
            for caso in gerenciadorArquivos.mapaCasos:
                listaX.append(mapaGOCaso[caso].x)
                listaY.append(mapaGOCaso[caso].y.sum())
            corBar = cor if frame.corFrame is None else frame.corFrame

            ObjetoGO = goGrafico(listaY, listaX, dadoEixoY.eixo, dadoEixoX.eixo, corBar, legenda)
            ObjetoGO.GO = go.Bar(x = listaX, y = listaY, marker_color=corBar ,showlegend=frame.mostra, name = frame.nome, error_y = dict(type='data', array = [100], visible = True))
            listaGO.append(ObjetoGO)

        return listaGO
    

    def interpreta(self, classe, formula):
        flag = 0
        flag_anterior = 0
        lista_ID =[]
        lista_chave = []
        chave = ""
        identificador = ""
        for i in range(len(formula)):
            
            flag_anterior = flag
            chave = chave + formula[i]
            if(formula[i] == "]"): 
                flag = 0
                chave = ""

            if(flag == 1):
                
                identificador = identificador + formula[i]
            if(flag_anterior == 1 and flag == 0):
                lista_ID.append(identificador)
                identificador = ""
            if(formula[i] == "["): 
                flag = 1
                lista_chave.append(chave.replace("[","").replace(" ",""))
                

        lista_sinal = []
        lista_hash = []
        for i in range(len(lista_chave)):
            if(lista_chave[i][0] == "-"):
                lista_sinal.append("-")
                lista_chave[i] = lista_chave[i].replace("-","")
                
                lista_chave[i] = lista_chave[i].strip() 
            else:
                lista_chave[i] = lista_chave[i].replace("+","")
                lista_sinal.append("+")
            lista_hash.append(str(hash(lista_sinal[i]+lista_chave[i]+"["+lista_ID[i]+"]")))

        mapaFormulaGO = {}
        for i in range(len(lista_hash)):
            mapaFormulaGO[lista_hash[i]]    = []
            if(lista_ID[i].upper() == "SIN"):
                lista_ID[i] = None

        

        for j in range(len(lista_hash)):
            mneumonico = lista_chave[j]
            string = lista_ID[j]
            string = None if string is None else string.upper()
            objetoDadoEixo = DadoEixo(mneumonico, string)
            objetoDadoEixo.interpreta(classe)
            




            mapaFormulaGO[lista_hash[j]] = objetoDadoEixo
        for elemento in mapaFormulaGO:
            if(mapaFormulaGO[elemento] is None):
                print("MNEUMONICO ERRADO, REVISAR MNEUMONICOS OU CHAMAR O PROGRAMDOR")
                exit(1)


        if(len(mapaFormulaGO)> 1): 

            testeMais = formula.split("+")
            if(testeMais[0] != ""):
                testeMenos  = testeMais[0].split("-")
                if(testeMenos[0] != ""):
                    formula = "+"+formula

            todosMais = list(self.find_all_custom(formula, "+"))
            todosMenos =  list(self.find_all_custom(formula, "-"))
            todos = todosMais + todosMenos

            dfY = pd.DataFrame()
            for elemento in mapaFormulaGO:
                posicao =min(todos)    
                df_temp = pd.DataFrame({"valor":mapaFormulaGO[elemento].y.tolist()})
                if(posicao in todosMais):
                    dfY = pd.concat([dfY, df_temp["valor"]], axis = 1)
                if(posicao in todosMenos): 
                    dfY = pd.concat([dfY, df_temp["valor"]*-1], axis = 1)
                todos.remove(posicao)
            GO = mapaFormulaGO[list(mapaFormulaGO.keys())[0]]
            GO.y = dfY.sum(axis = 1)
            return GO
        else:            
            GO = mapaFormulaGO[list(mapaFormulaGO.keys())[0]]
            if(GO != 0 ): return GO
            

            if(GO == 0):
                print("MNEUMONICO ERRADO, POR FAVOR UTILIZE ALGUNS DOS MNEUMONICOS A SEGUIR:")
                print(self.__mneumonicos)
                exit(1)
                return 0

    
    def legenda(self, caso):
        return caso.split("/")[-1]
    


    def find_all_custom(self, a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches




"""     def separaFormulaEmChaveIdentificador(self, listaFormula):

        listaParesChaveIdentificador  = []
        for elemento in listaFormula:
            if("[" in elemento):
                identificador = elemento[elemento.find("[")+1:elemento.find("]")].strip()
            else:
                identificador = None
            
            chave = elemento.split("[")[0].strip()
            print("chave: ", chave, " id: ", identificador)
            listaParesChaveIdentificador.append((chave.lower(),identificador))
        return listaParesChaveIdentificador """