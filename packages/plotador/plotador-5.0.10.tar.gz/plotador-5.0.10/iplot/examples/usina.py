class GeraUsina():

    def __init__(self, iplot, usina, title):
        iplot.figure(usina)
        iplot.add_frame(usina, formula= "gh["+usina+"]", lin = 1 , col =1)
        iplot.add_frame(usina, formula= "qturb["+usina+"]", lin = 1 , col =2)
        iplot.add_frame(usina, formula= "qvert["+usina+"]", lin = 1 , col =3)
        iplot.add_frame(usina, formula= "varmfu["+usina+"]", lin = 2 , col =1)
        iplot.add_frame(usina, formula= "qdef["+usina+"]", lin = 2 , col =2)
        iplot.add_frame(usina, formula= "qafl["+usina+"]", lin = 2 , col =3)
        iplot.show(usina, title)


