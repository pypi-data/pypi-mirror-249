from plotly.subplots import make_subplots
import csv
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
 

class LayoutPlotPersonalizado():
    def __init__(self, figura, tituloGrafico):

        if(len(figura.listaFrames) > 1): 
            fig0 = make_subplots(rows=figura.max_linha,cols=figura.max_coluna,subplot_titles=(" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", 
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " ",
                                                                      " ", " ", " ", " ", " ", " ", " ", " ", " ", " "))
            for frame in figura.listaFrames:
                for goOjbect in frame.getListaGO():
                    show = True if (frame.linha == 1 and frame.coluna == 1) else False  
                    #fig0.add_trace(go.returnGoObject(show), row=frame.linha,col=frame.coluna)
                    fig0.add_trace(goOjbect.returnGoObject(), row=frame.linha,col=frame.coluna)
                    fig0.update_xaxes(title_text=goOjbect.xaxis, row = frame.linha, col = frame.coluna)
                    fig0.update_yaxes(title_text=goOjbect.yaxis, row = frame.linha, col = frame.coluna)
                fig0.layout.annotations[figura.getPosicaoTitulo(frame.linha,frame.coluna)].update(text=frame.getTitulo())
            fig0.update_layout(title=tituloGrafico, boxmode='group', barmode = 'stack')
            fig0.write_html(figura.caminhoDeSaida+tituloGrafico+".html")            
        else:
            fig0 = go.Figure()
            for frame in figura.listaFrames:
                for goOjbect in frame.getListaGO():
                    fig0.add_trace(goOjbect.returnGoObject())
                    fig0.update_xaxes(title_text=goOjbect.xaxis)
                    fig0.update_yaxes(title_text=goOjbect.yaxis)
            fig0.update_layout(title=tituloGrafico, boxmode='group', barmode = 'stack')

            fig0.write_html(figura.caminhoDeSaida+tituloGrafico+".html")
            fig0.write_image(figura.caminhoDeSaida+tituloGrafico+".png")
            #pio.write_image(fig0, tituloGrafico+".png")

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

                   
