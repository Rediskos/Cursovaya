# Импорт необходимых модулей
import plotly
import plotly.graph_objs as go


dataMed = {'x':[], 'y':[], 'z':[]}
dataMath = {'x':[], 'y':[], 'z':[]}
dataSport = {'x':[], 'y':[], 'z':[]}
data = {'x':[], 'y':[], 'z':[]}
colors = []

def normalize(target):
    All = 0
    for i in target:
        # print("a ", int(i))
        All += int(i)
    
    return [float(i) / All for i in target]

with open("BD_Med_Sport_Math/Sport/SportPoints.txt", "r", encoding = "utf-8") as inpt:
    for i in inpt.readlines():
        tmp = normalize(i.split())
        all = tmp[0]+tmp[1]+tmp[2]
        data['x'].append(tmp[0])
        data['y'].append(tmp[1])
        data['z'].append(tmp[2])
        colors.append('#ff0000')
        
with open("BD_Med_Sport_Math/Med/MedPoints.txt", "r", encoding = "utf-8") as inpt:
    for i in inpt.readlines():
        tmp = normalize(i.split())
        all = tmp[0]+tmp[1]+tmp[2]
        data['x'].append(tmp[0])
        data['y'].append(tmp[1])
        data['z'].append(tmp[2])
        colors.append('#00ff00')
        
with open("BD_Med_Sport_Math/Math/MathPoints.txt", "r", encoding = "utf-8") as inpt:
    for i in inpt.readlines():
        tmp = normalize(i.split())
        all = tmp[0]+tmp[1]+tmp[2]
        data['x'].append(tmp[0])
        data['y'].append(tmp[1])
        data['z'].append(tmp[2])
        colors.append('#0000ff')
        

fig1 = go.Scatter3d(x=data['x'],
                    y=data['y'],
                    z=data['z'],
                    marker=dict(opacity=0.9,
                                reversescale=True,
                                color=colors,
                                size=5),
                    line=dict (width=0.02),
                    mode='markers')

#Make Plot.ly Layout
mylayout = go.Layout(scene=dict(xaxis=dict( title="x"),
                                yaxis=dict( title="y"),
                                zaxis=dict(title="z")),)

#Plot and save html
plotly.offline.plot({"data": [fig1],
                     "layout": mylayout},
                     auto_open=True,
                     filename=("3DPlot.html"))