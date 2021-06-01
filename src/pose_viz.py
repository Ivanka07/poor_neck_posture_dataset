import json
import numpy as np
import sys
import os
import plotly.graph_objects as go
import plotly as px
import plotly.express as px

body_links = [(0,4), (0,1), (4,5),(5,6), (6,8), (1,2), (2,3), (3,7), \
			 (10,9), (12,11),(12,14),(14,16),(16,22),(16,18),(18,20),\
			 (20,16),(11,13),(11,23),(13,15),(15,21), (15, 19), (19,17), (15,17),\
			 (12,24), (24,23), (24,26),(26,28),(28,30), (30, 32),(28,32), (23,25), (25,27),\
			 (27,29),(27,31), (29,31), (29,31)]


with open('/home/ivanna/git/mmac/data/JMU2zYrLnK8_10_12.mp4.json') as f:
  data = json.load(f)
print(len(data['data']))
init_pose = data['data']['frame0002']['person00']
x = []
y = []
z = []
for body_key in init_pose:

	x.append(body_key[0])
	y.append(body_key[1])
	z.append(body_key[2])

print(len(x))



def plot_joints(x_joints, y_joints, z_joints, links=body_links):

	trace1 = go.Scatter3d(
	    x=x_joints,
	    y=y_joints,
	    z=z_joints,
	    mode='markers',
	    name='markers', 
	    marker=dict(
        	size=8,
        	color=z_joints,                # set color to an array/list of desired values
        	colorscale='Viridis',   # choose a colorscale
        	opacity=0.8
    	)
	)

	x_lines = list()
	y_lines = list()
	z_lines = list()

	#create the coordinate list for the lines
	for p in links:
	    for i in range(2):
	        x_lines.append(x_joints[p[i]])
	        y_lines.append(y_joints[p[i]])
	        z_lines.append(z_joints[p[i]])
	    x_lines.append(None)
	    y_lines.append(None)
	    z_lines.append(None)

	trace2 = go.Scatter3d(
	    x=x_lines,
	    y=y_lines,
	    z=z_lines,
	    mode='lines',
	    name='lines'
	)

	fig = go.Figure(data=[trace1, trace2])
	fig.show()


plot_joints(x,y,z)