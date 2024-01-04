class GeraBarAglut():

    def __init__(self, iplot, title):


        
        iplot.figure("SIN")
        iplot.add_frame("SIN", "gh[SIN]", 1 , 1, None)
        iplot.add_frame("SIN", "gt[SIN]", 1 , 2, None)
        iplot.add_frame("SIN", "earm[SIN]", 1 , 3, None)
        iplot.add_frame("SIN", "evert[SIN]", 2 , 1, None)
        iplot.add_frame("SIN", "enaflu[SIN]", 2 , 2, None)
        iplot.show("SIN",title)


