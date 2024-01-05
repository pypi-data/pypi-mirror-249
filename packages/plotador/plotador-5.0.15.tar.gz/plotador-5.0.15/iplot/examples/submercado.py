class GeraSubmercado():

    def __init__(self,iplot, submercado, title):
        iplot.figure(submercado)
        iplot.add_frame(submercado, "gh", 1 , 1, submercado)
        iplot.add_frame(submercado, "gt", 1 , 2, submercado)
        iplot.add_frame(submercado, "cmo", 1 , 3, submercado)
        iplot.add_frame(submercado, "earm", 2 , 1, submercado)
        iplot.add_frame(submercado, "evert", 2 , 2, submercado)
        iplot.add_frame(submercado, "eafl", 2 , 3, submercado)
        iplot.show(submercado, title)


