
import pandas as pd

class dadosNewave_Convergencia():

    def __init__(self, caminhoNewave):
        self.caminhoNewave = caminhoNewave


    @property
    def zinf(self):
        return pd.read_parquet(self.caminhoNewave+"/CONVERGENCIA.parquet.gzip", engine='pyarrow')["zinf"]*1000000
    @property
    def iter(self):
        return pd.read_parquet(self.caminhoNewave+"/CONVERGENCIA.parquet.gzip", engine='pyarrow')["iter"]
    @property
    def cpuTime(self):
        df_Convergencia = pd.read_parquet(self.caminhoNewave+"/CONVERGENCIA.parquet.gzip", engine='pyarrow')
        print("Newave: ", df_Convergencia["tempo"].sum())
        return df_Convergencia["tempo"].sum()