
import pandas as pd
import os.path
class estruturas():

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave



    @property
    def estagio(self):
        return pd.read_parquet(self.caminhoNewave+'/'+"EST.parquet.gzip", engine='pyarrow')["idEstagio"].tolist()
    

    def leSINRetornaDataFrameCenariosValidos(self, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["cenario"].apply(lambda x: x.isnumeric()))]
        return df
    

    def leSINRetornaDataFrameCenarioMedio(self, arquivo):
        if(os.path.isfile("/"+self.caminhoNewave+'/'+arquivo)):
            df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
            df = df_NW.loc[(df_NW["cenario"] == "mean")]["valor"]
            return df
        else:
            print("Arquivo "+arquivo+" não existe para o caso "+self.caminhoNewave)
            return [0]

    

    def leSubmercadoRetornaDataFrameCenariosValidos(self, nomeSubmercado, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["submercado"] == nomeSubmercado) & (df_NW["cenario"].apply(lambda x: x.isnumeric()))]
        return df
    
    def leUsinaRetornaDataFrameCenariosValidos(self, nomeUsina, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["usina"] == nomeUsina) & (df_NW["cenario"].apply(lambda x: x.isnumeric()))]
        return df

    def leSubmercadoRetornaDataFrameCenarioMedio(self, nomeSubmercado, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["submercado"] == nomeSubmercado) & (df_NW["cenario"] == "mean")]["valor"]
        return df



    def leUsinaRetornaDataFrameCenarioMedio(self, nomeUsina, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df = df_NW.loc[(df_NW["usina"] == nomeUsina) & (df_NW["cenario"] == "mean")]["valor"]
        return df
    

    def retornaValoresSINAgrupadosPorUsina(self, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df_mean = df_NW.loc[(df_NW["cenario"] == "mean")]
        valores = []
        for est in range(1, len(self.estagio)+1):
            val = df_mean.loc[(df_mean["estagio"] == est)]["valor"].sum()
            valores.append(val)
        df = pd.DataFrame({"valor": valores})
        return df["valor"]
    
    def retornaValoresSubmercadoAgrupadosPorUsina(self, submercado, arquivo):
        df_NW = pd.read_parquet(self.caminhoNewave+'/'+arquivo, engine='pyarrow')
        df_mean = df_NW.loc[(df_NW["cenario"] == "mean")]
        df_usinas = pd.read_parquet(self.caminhoNewave+'/UHE.parquet.gzip', engine='pyarrow')#["nome"].tolist()
        df_REE = pd.read_parquet(self.caminhoNewave+'/REE.parquet.gzip', engine='pyarrow')#["nome"].tolist()
        df_SBM = pd.read_parquet(self.caminhoNewave+'/SBM.parquet.gzip', engine='pyarrow')#["nome"].tolist()

        id_sbm = df_SBM.loc[df_SBM["nome"] == submercado]["id"].tolist()[0]
        lista_id_REE_SBM = df_REE.loc[df_REE["idSubmercado"] == id_sbm]["id"].tolist()
        list_usinas_SBM = []
        for idRee in lista_id_REE_SBM:
            df_usinas_sbm = df_usinas.loc[df_usinas["idREE"] == idRee ]["nome"].tolist()
            list_usinas_SBM = list_usinas_SBM + df_usinas_sbm

        emptyDf= pd.DataFrame()
        for usina in list_usinas_SBM:
            dados = df_mean.loc[(df_mean["usina"] == usina)]["valor"].tolist()
            #df_temp = pd.DataFrame(dados)
            #emptyDf[usina] = df_temp
            df_temp = pd.DataFrame({usina: dados})
            emptyDf = pd.concat([emptyDf, df_temp], axis =1)
        return emptyDf.sum(axis = 1)