from plotly.subplots import make_subplots
import csv
import pandas as pd
class LayoutPlotDiff():
    def __init__(self, figura, tituloGrafico):
        fig0 = make_subplots(rows=figura.max_linha,cols=figura.max_coluna,subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
        for frame in figura.listaFrames:
            listaGO = frame.getListaGO()
            if(len(listaGO) > 2):
                print("LISTA GO MAIOR QUE 2, NAO E POSSIVEL UTILIZAR O GRAFICO DIFF")
                exit(1)
            else:
                
                go0 = listaGO[0]
                go1 = listaGO[1]
                diff_y = go0.y - go1.y
                diff_legenda = "G0 - G1"
                show = True if (frame.linha == 1 and frame.coluna == 1) else False  
                go0.y = diff_y
                go0.legenda = diff_legenda
                fig0.add_trace(go0.returnGoObject(show), row=frame.linha,col=frame.coluna)
                fig0.update_xaxes(title_text=go0.xaxis, row = frame.linha, col = frame.coluna)
                fig0.update_yaxes(title_text=go0.yaxis, row = frame.linha, col = frame.coluna)
            fig0.layout.annotations[figura.getPosicaoTitulo(frame.linha,frame.coluna)].update(text=frame.getTitulo())
        fig0.update_layout(title=tituloGrafico, boxmode='group')
        fig0.write_html(tituloGrafico+".html")
        print("PLOTAGEM PERSONALIZADA CONCLUIDA COM SUCESSO")

"""
        Dict_csv = {}
        with open("dados_"+figura.nome+".csv", "w") as file:
            write = csv.writer(file)
            for frame in figura.listaFrames:
                for go in frame.getListaGO():
                    show = True if (frame.linha == 1 and frame.coluna == 1) else False  
                    Dict_csv[frame.getTitulo()+"_"+go.legenda] = go.y  
                    write.writerow(frame.getTitulo()+"_"+go.legenda) 
                    write.writerows(map(lambda x: [x], go.y))
                    fig0.add_trace(go.returnGoObject(show), row=frame.linha,col=frame.coluna)
                    fig0.update_xaxes(title_text=go.xaxis)
                    fig0.update_yaxes(title_text=go.yaxis)
                fig0.layout.annotations[figura.getPosicaoTitulo(frame.linha,frame.coluna)].update(text=frame.getTitulo())
            fig0.update_layout(title=tituloGrafico, boxmode='group')
            fig0.write_html(tituloGrafico+".html")
            print("PLOTAGEM PERSONALZIADA CONCLUIDA COM SUCESSO")
            pdDict = pd.DataFrame(Dict_csv)
            print("CSV: ", Dict_csv)
            ###EXPORT CSV
"""

                   
