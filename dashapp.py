import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import sympy as sp
import numpy as np
import tetra_calc as tc

# Fix for displaying math formulas
MATHJAX_CDN = '''
https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/
MathJax.js?config=TeX-MML-AM_CHTML'''

external_scripts = [
                    {'type': 'text/javascript',
                     'id': 'MathJax-script',
                     'src': MATHJAX_CDN,
                     },
                    ]

app = dash.Dash(__name__, prevent_initial_callbacks=True, 
                external_scripts=external_scripts)

server = app.server

# Input fields
app.layout = html.Div(children=[
    html.Div(id='input-fields', className='center-full', children=[
        html.H1(children="Tetrahedron calculator"),
        html.Label('Point A: ', className='point-label'),
        html.Label('x: '), dcc.Input(id='ax', value=0, type='number', min=-10000, max=10000),
        html.Label('y: '), dcc.Input(id='ay', value=0, type='number', min=-10000, max=10000),
        html.Label('z: '), dcc.Input(id='az', value=0, type='number', min=-10000, max=10000),
        html.Br(),
        html.Label('Point B: ', className='point-label'),
        html.Label('x: '), dcc.Input(id='bx', value=0, type='number', min=-10000, max=10000),
        html.Label('y: '), dcc.Input(id='by', value=0, type='number', min=-10000, max=10000),
        html.Label('z: '), dcc.Input(id='bz', value=0, type='number', min=-10000, max=10000),
        html.Br(),
        html.Label('Point C: ', className='point-label'),
        html.Label('x: '), dcc.Input(id='cx', value=0, type='number', min=-10000, max=10000),
        html.Label('y: '), dcc.Input(id='cy', value=0, type='number', min=-10000, max=10000),
        html.Label('z: '), dcc.Input(id='cz', value=0, type='number', min=-10000, max=10000),
        html.Br(),
        html.Label('Point D: ', className='point-label'),
        html.Label('x: '), dcc.Input(id='dx', value=0, type='number', min=-10000, max=10000),
        html.Label('y: '), dcc.Input(id='dy', value=0, type='number', min=-10000, max=10000),
        html.Label('z: '), dcc.Input(id='dz', value=0, type='number', min=-10000, max=10000),
        html.Br(),
        html.Button(id='submit-points', children='Calculate')
    ]),
    html.Div(id='outputs')
])

@app.callback(Output('outputs', 'children'),
            Input('submit-points', 'n_clicks'),
            State('ax', 'value'), State('ay', 'value'), State('az', 'value'),
            State('bx', 'value'), State('by', 'value'), State('bz', 'value'),
            State('cx', 'value'), State('cy', 'value'), State('cz', 'value'),
            State('dx', 'value'), State('dy', 'value'), State('dz', 'value')
)
def update_outputs(n_clicks, ax, ay, az, bx, by, bz, cx, cy, cz, dx, dy, dz):
    
    A = np.array([ax, ay, az])
    B = np.array([bx, by, bz])
    C = np.array([cx, cy, cz])
    D = np.array([dx, dy, dz])


    # Checks if points are coplanar or colinear
    err_list = []

    if tc.is_colinear(A, B, C):
        err_list.append(html.Div('Points A, B, C are colinear', className='center-full'))

    if tc.is_colinear(A, B, D):
        err_list.append(html.Div('Points A, B, D are colinear', className='center-full'))

    if tc.is_colinear(A, C, D):
        err_list.append(html.Div('Points A, C, D are colinear', className='center-full'))
    
    if tc.is_colinear(B, C, D):
        err_list.append(html.Div('Points B, C, D are colinear', className='center-full'))
        
    if tc.is_coplanar(A, B, C, D):
        err_list.append(html.Div('Points A, B, C, D are coplanar', className='center-full'))

    if err_list:
        return err_list

   
    tetra = tc.Tetrahedron(A, B, C, D)


    # 3D Plots
    tetra_fig = go.Figure(data=[
        go.Mesh3d(
            x=[A[0], B[0], C[0], D[0]],
            y=[A[1], B[1], C[1], D[1]],
            z=[A[2], B[2], C[2], D[2]],
            i=[0, 0, 0, 1],
            j=[1, 2, 3, 2],
            k=[2, 3, 1, 3],
            facecolor=['#ff1100', '#05eb1c', '#05ebe7', '#eb05bd'],
            hoverinfo='none',
            showscale=False,
        )
    ])

    tetra_fig.add_trace(go.Scatter3d(
        x=[A[0], B[0], C[0], D[0]],
        y=[A[1], B[1], C[1], D[1]],
        z=[A[2], B[2], C[2], D[2]],
        hovertext=['Point A', 'Point B', 'Point C', 'Point D'],
        hoverinfo='text+x+y+z',
        hoverlabel={'bgcolor':'#f5f5f5'},
        marker={'color':'rgba(0,0,0,0.7)'}
    ))

    tABC_fig = go.Figure(data=[
        go.Mesh3d(
            x=[A[0], B[0], C[0]],
            y=[A[1], B[1], C[1]],
            z=[A[2], B[2], C[2]],
            i=[0],
            j=[1],
            k=[2],
            facecolor=['#ff1100'],
            hoverinfo='none',
            name='y',
            showscale=False,
            contour={'show':True, 'width':10}
        )
    ])

    tABC_fig.add_trace(go.Scatter3d(
        x=[A[0], B[0], C[0]],
        y=[A[1], B[1], C[1]],
        z=[A[2], B[2], C[2]],
        hovertext=['Point A', 'Point B', 'Point C'],
        hoverinfo='text+x+y+z',
        hoverlabel={'bgcolor':'#f5f5f5'},
        marker={'color':'rgba(0,0,0,0.7)'}
    ))



    tABD_fig = go.Figure(data=[
        go.Mesh3d(
            x=[A[0], B[0], D[0]],
            y=[A[1], B[1], D[1]],
            z=[A[2], B[2], D[2]],
            i=[0],
            j=[1],
            k=[2],
            facecolor=['#05ebe7'],
            hoverinfo='none',
            name='y',
            showscale=False,
            contour={'show':True, 'width':10}
        )
    ])
    
    tABD_fig.add_trace(go.Scatter3d(
        x=[A[0], B[0], D[0]],
        y=[A[1], B[1], D[1]],
        z=[A[2], B[2], D[2]],
        hovertext=['Point A', 'Point B', 'Point D'],
        hoverinfo='text+x+y+z',
        hoverlabel={'bgcolor':'#f5f5f5'},
        marker={'color':'rgba(0,0,0,0.7)'}
    ))



    tACD_fig = go.Figure(data=[
        go.Mesh3d(
            x=[A[0], C[0], D[0]],
            y=[A[1], C[1], D[1]],
            z=[A[2], C[2], D[2]],
            i=[0],
            j=[1],
            k=[2],
            facecolor=['#05eb1c'],
            hoverinfo='none',
            name='y',
            showscale=False,
            contour={'show':True, 'width':10}
        )
    ])

    tACD_fig.add_trace(go.Scatter3d(
        x=[A[0], C[0], D[0]],
        y=[A[1], C[1], D[1]],
        z=[A[2], C[2], D[2]],
        hovertext=['Point A', 'Point C', 'Point D'],
        hoverinfo='text+x+y+z',
        hoverlabel={'bgcolor':'#f5f5f5'},
        marker={'color':'rgba(0,0,0,0.7)'}
    ))



    tBCD_fig = go.Figure(data=[
        go.Mesh3d(
            x=[B[0], C[0], D[0]],
            y=[B[1], C[1], D[1]],
            z=[B[2], C[2], D[2]],
            i=[0],
            j=[1],
            k=[2],
            facecolor=['#eb05bd'],
            hoverinfo='none',
            name='y',
            showscale=False,
            contour={'show':True, 'width':10}
        )
    ])

    tBCD_fig.add_trace(go.Scatter3d(
        x=[B[0], C[0], D[0]],
        y=[B[1], C[1], D[1]],
        z=[B[2], C[2], D[2]],
        hovertext=['Point B', 'Point C', 'Point D'],
        hoverinfo='text+x+y+z',
        hoverlabel={'bgcolor':'#f5f5f5'},
        marker={'color':'rgba(0,0,0,0.7)'}
    ))


    # Page content
    tetra_html = html.Div(className='center-full', children=[
        html.H2('Tetrahedron ABCD:'),
        html.P(f'''Surface area: \({sp.latex(tetra.surface_area)} \\approx \) {round(tetra.surface_area, 4)}'''),
        html.P(f'''Volume: \({sp.latex(tetra.volume)} \\approx \) {round(tetra.volume, 4)}'''),
        html.P('Height from an apex to a base'),
        html.P(f'''A to BCD: \({sp.latex(tetra.ha)} \\approx \) {round(tetra.ha, 4)}'''),
        html.P(f'''B to ACD: \({sp.latex(tetra.hb)} \\approx \) {round(tetra.hb, 4)}'''),
        html.P(f'''C to ABD: \({sp.latex(tetra.hc)} \\approx \) {round(tetra.hc, 4)}'''),
        html.P(f'''D to ABC: \({sp.latex(tetra.hd)} \\approx \) {round(tetra.hd, 4)}'''),
        dcc.Graph(figure=tetra_fig)
    ])

    tABC_html = html.Div(className='t-col', children=[
        html.H2('Triangle ABC:'),
        html.P('Sides'),
        html.P(f'''a = BC = \({sp.latex(tetra.fABC.BC)} \\approx \) {round(tetra.fABC.BC, 4)}'''),
        html.P(f'''b = AC = \({sp.latex(tetra.fABC.AC)} \\approx \) {round(tetra.fABC.AC, 4)}'''),
        html.P(f'''c = AB = \({sp.latex(tetra.fABC.AB)} \\approx \) {round(tetra.fABC.AB, 4)}'''), html.Br(),
        html.P(f'''Area: \({sp.latex(tetra.fABC.area)} \\approx \) {round(tetra.fABC.area, 4)}'''), html.Br(),
        html.P('Heights'),
        html.P(f'''From vertex A: \({sp.latex(tetra.fABC.ha)} \\approx \) {round(tetra.fABC.ha, 4)}'''),
        html.P(f'''From vertex B: \({sp.latex(tetra.fABC.hb)} \\approx \) {round(tetra.fABC.hb, 4)}'''),
        html.P(f'''From vertex C: \({sp.latex(tetra.fABC.hc)} \\approx \) {round(tetra.fABC.hc, 4)}'''), html.Br(),
        html.P('Internal angles'),
        html.P(f'''At vertex A: {round(tetra.fABC.alpha, 1)}'''),
        html.P(f'''At vertex B: {round(tetra.fABC.beta, 1)}'''),
        html.P(f'''At vertex C:  {round(tetra.fABC.gamma, 1)}'''),
        dcc.Graph(figure=tABC_fig)
    ])

    tABD_html = html.Div(className='t-col', children=[
        html.H2('Triangle ABD:'),
        html.P('Sides'),
        html.P(f'''c = AB = \({sp.latex(tetra.fABD.AB)} \\approx \) {round(tetra.fABD.AB, 4)}'''),
        html.P(f'''d = BD = \({sp.latex(tetra.fABD.BC)} \\approx \) {round(tetra.fABD.BC, 4)}'''),
        html.P(f'''e = AD = \({sp.latex(tetra.fABD.AC)} \\approx \) {round(tetra.fABD.AC, 4)}'''), html.Br(),
        html.P(f'''Area: \({sp.latex(tetra.fABD.area)} \\approx \) {round(tetra.fABD.area, 4)}'''), html.Br(),
        html.P('Heights'),
        html.P(f'''From vertex A: \({sp.latex(tetra.fABD.ha)} \\approx \) {round(tetra.fABD.ha, 4)}'''),
        html.P(f'''From vertex B: \({sp.latex(tetra.fABD.hb)} \\approx \) {round(tetra.fABD.hb, 4)}'''),
        html.P(f'''From vertex D: \({sp.latex(tetra.fABD.hc)} \\approx \) {round(tetra.fABD.hc, 4)}'''), html.Br(),
        html.P('Internal angles'),
        html.P(f'''At vertex A:  {round(tetra.fABD.alpha, 1)}'''), 
        html.P(f'''At vertex B: {round(tetra.fABD.beta, 1)}'''),
        html.P(f'''At vertex D:  {round(tetra.fABD.gamma, 1)}'''),
        dcc.Graph(figure=tABD_fig)
    ])

    tACD_html = html.Div(className='t-col', children=[
        html.H2('Triangle ACD:'),
        html.P('Sides'),
        html.P(f'''b = AC = \({sp.latex(tetra.fACD.AB)} \\approx \) {round(tetra.fACD.AB, 4)}'''),
        html.P(f'''e = AD = \({sp.latex(tetra.fACD.AC)} \\approx \) {round(tetra.fACD.AC, 4)}'''),
        html.P(f'''f = CD = \({sp.latex(tetra.fACD.BC)} \\approx \) {round(tetra.fACD.BC, 4)}'''), html.Br(),
        html.P(f'''Area: \({sp.latex(tetra.fACD.area)} \\approx \) {round(tetra.fACD.area, 4)}'''), html.Br(),
        html.P('Heights'),
        html.P(f'''From vertex A: \({sp.latex(tetra.fACD.ha)} \\approx \) {round(tetra.fACD.ha, 4)}'''),
        html.P(f'''From vertex C: \({sp.latex(tetra.fACD.hb)} \\approx \) {round(tetra.fACD.hb, 4)}'''), 
        html.P(f'''From vertex D: \({sp.latex(tetra.fACD.hc)} \\approx \) {round(tetra.fACD.hc, 4)}'''), html.Br(),
        html.P('Internal angles'),
        html.P(f'''At vertex A: {round(tetra.fACD.alpha, 1)}'''),
        html.P(f'''At vertex C: {round(tetra.fACD.beta, 1)}'''),
        html.P(f'''At vertex D: {round(tetra.fACD.gamma, 1)}'''),
        dcc.Graph(figure=tACD_fig)
    ])

    tBCD_html = html.Div(className='t-col', children=[
        html.H2('Triangle BCD:'),
        html.P('Sides'),
        html.P(f'''a = BC = \({sp.latex(tetra.fBCD.AB)} \\approx \) {round(tetra.fBCD.AB, 4)}'''),
        html.P(f'''d = BD = \({sp.latex(tetra.fBCD.AC)} \\approx \) {round(tetra.fBCD.AC, 4)}'''),
        html.P(f'''f = CD = \({sp.latex(tetra.fBCD.BC)} \\approx \) {round(tetra.fBCD.BC, 4)}'''), html.Br(),
        html.P(f'''Area: \({sp.latex(tetra.fBCD.area)} \\approx \) {round(tetra.fBCD.area, 4)}'''), html.Br(),
        html.P('Heights'),
        html.P(f'''From vertex D: \({sp.latex(tetra.fBCD.ha)} \\approx \) {round(tetra.fBCD.ha, 4)}'''),
        html.P(f'''From vertex C: \({sp.latex(tetra.fBCD.hb)} \\approx \) {round(tetra.fBCD.hb, 4)}'''),
        html.P(f'''From vertex B: \({sp.latex(tetra.fBCD.hc)} \\approx \) {round(tetra.fBCD.hc, 4)}'''), html.Br(),
        html.P('Internal angles'),
        html.P(f'''At vertex B: {round(tetra.fBCD.alpha, 1)}'''),
        html.P(f'''At vertex C: {round(tetra.fBCD.beta, 1)}'''),
        html.P(f'''At vertex D: {round(tetra.fBCD.gamma, 1)}'''),
        dcc.Graph(figure=tBCD_fig)
    ])
    

    return [tetra_html, html.Div(className='center-full', children=[tABC_html, tABD_html]), html.Div(className='center-full', children=[tACD_html, tBCD_html])]

if __name__ == '__main__':
    app.run_server(debug=False,dev_tools_ui=False,dev_tools_props_check=False)