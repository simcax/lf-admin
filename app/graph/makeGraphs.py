
import matplotlib
from werkzeug.utils import send_file
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class makeGraphs:

    def createXYGraph(x,y,title,xlabel,ylabel):
        fig = plt.figure(figsize=(10,4))
        #plt.figure(figsize=(10,4))
        ax = fig.subplots()
        ax.bar(y,x)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        #fig.bar(y, x)
        #fig.title(title)
        #fig.xlabel(xlabel)
        #fig.ylabel(ylabel)
        buf = BytesIO()

        fig.savefig(buf, format="png")
        #data = base64.b64encode(buf.getbuffer()).decode("ascii")
        data = base64.encodebytes(buf.getbuffer()).decode("ascii")
        return f"<img src='data:image/png;base64,{data}'/>"
        #return data
        #return data
