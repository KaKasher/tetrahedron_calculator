# Tetrahedron calculator
Simple app that calculates numerous measures of a tetrahedron

## Setup
1. In order to run this project you'll need to install all of the dependencies.
Do this using pip: `pip install -r requirements.txt`
2. Run *dashapp.py* file in the terminal: `python dashapp.py`
3. You should see the server running. Go to the specified ip address in your browser. Default is `http://127.0.0.1:8050/`

## Technologies
Project created using:
* Dash
* Plotly
* MathJax
* NumPy
* SymPy

## Functions
Using 4 points in 3D space, app calculates<br>
for the tetrahedron:
<ul>
  <li>Surface area</li>
  <li>Volume</li>
  <li>Height from each vertex</li>
</ul>

for each face of the tetrahedron:

* Lenght of each side
* Area
* Heights from each vertex
* Internal angles

<br>Furthermore each figure is plotted in 3d.

