import plotly
import plotly.graph_objs as go
import pandas as pd
from search_comics import *
import squarify
from plot_bits import petrichor

plotly.offline.init_notebook_mode()
x = 0.
y = 0.
width = 10000.
height = 10000.

df=pd.read_csv('/Users/ksakamoto/Desktop/new_orange.csv')
df.sort_values(by='Publisher',inplace=True)
c=list(df['Publisher'].drop_duplicates())

values = [500, 433, 78, 25, 25, 7]
values=map(int,array(df['Size'])[:3000])

normed = squarify.normalize_sizes(values, width, height)
rects = squarify.squarify(normed, x, y, width, height)

# Choose colors from http://colorbrewer2.org/ under "Export"
color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(178,223,138)',
                'rgb(51,160,44)','rgb(251,154,153)','rgb(227,26,28)',
                'rgb(253,191,111)','rgb(255,127,0)','rgb(202,178,214)',
                'rgb(106,61,154)','rgb(255,255,153)','rgb(177,89,40)']

colls=dict(zip(c,petrichor))

shapes = []
annotations = []
counter = 0

for r in rects:
    shapes.append( 
        dict(
            type = 'rect', 
            x0 = r['x'], 
            y0 = r['y'], 
            x1 = r['x']+r['dx'], 
            y1 = r['y']+r['dy'],
            line = dict( width = 2 ),
            fillcolor = colls[df['Publisher'].ix[counter]]
        ) 
    )
    annotations.append(
        dict(
            x = r['x']+(r['dx']/2),
            y = r['y']+(r['dy']/2),
            text = values[counter],
            showarrow = False
        )
    )
    counter = counter + 1
    #if counter >= len(color_brewer):
    #    counter = 0

# For hover text
trace0 = go.Scatter(
    x = [ r['x']+(r['dx']/2) for r in rects ], 
    y = [ r['y']+(r['dy']/2) for r in rects ],
    text = [ str(v) for v in values ], 
    mode = 'text',
)
        
layout = dict(
    height=1500, 
    width=1500,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    shapes=shapes,
    #annotations=annotations,
    hovermode='closest'
)

# With hovertext
figure = dict(data=[trace0], layout=layout)

# Without hovertext
# figure = dict(data=[Scatter()], layout=layout)
plotly.offline.plot(figure)
#py.iplot(figure, filename='squarify-treemap')
