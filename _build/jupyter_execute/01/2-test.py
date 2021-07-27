# Example notebook (brain data)

## 1: Read and organize data 

Data used in notebook is avilable [here](https://github.com/courtois-neuromod/anat-processing/releases).

import pandas as pd

df = pd.read_csv("./../neuromod-anat-brain-qmri/results-neuromod-anat-brain-qmri.csv", converters={'project_id': lambda x: str(x)})

df

df.sort_values(['subject', 'session'], ascending=[True, True]) 

# Define lists for metrics
mean_MP2RAGE_t1_matrix = []
mean_MTS_t1_matrix     = []
mean_mtr_matrix        = []
mean_mtsat_matrix      = []

# Get the values for all 4 metric [area, mean_AP, mean_RL, angle_AP]
for i in range(1, 7, 1):
    sub_values = df.loc[df['subject'] == i]
    
    mean_MP2RAGE_ses = []
    
    mean_MTS_ses     = []
    
    mean_mtr_ses     = []

    mean_mtsat_ses   = []
    
    for j in range(1, 5, 1):
        ses_values = sub_values.loc[sub_values['session'] == j]
        
        MEAN_mp2   = -100
        
        MEAN_mts   = -100
        
        MEAN_mtr   = -100
        
        MEAN_mtsat = -100

        
        for index, row in ses_values.iterrows():

            if row['acquisition'] == 'MP2RAGE' and row['metric'] == 'T1map' and row['label'] == 'GM': 
                MEAN_mp2 = row['mean']
            
            if row['acquisition'] == 'MTS' and row['metric'] == 'T1map' and row['label'] == 'GM':
                MEAN_mts = row['mean']
                
            if row['metric'] == 'MTRmap' and row['label'] == 'GM': 
                MEAN_mtr = row['mean']
                
            if row['metric'] == 'MTsat' and row['label'] == 'GM': 
                MEAN_mtsat = row['mean']
            
        # Append values to lists for sessions
        mean_MP2RAGE_ses.append(MEAN_mp2)
        
        mean_MTS_ses.append(MEAN_mts)
        
        mean_mtr_ses.append(MEAN_mtr)
        
        mean_mtsat_ses.append(MEAN_mtsat)
        
        
    # Append session lists to main matrices for each metric
    mean_MP2RAGE_t1_matrix.append(mean_MP2RAGE_ses)
    
    mean_MTS_t1_matrix.append(mean_MTS_ses)
    
    mean_mtr_matrix.append(mean_mtr_ses)
    
    mean_mtsat_matrix.append(mean_mtsat_ses)

## 2: Plot data

import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from IPython.core.display import display, HTML
import numpy as np


# Add plotly 
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}

t1 = [-0.2, -0.06, 0.08, 0.22]
t2 = [0 -0.2 + i*0.14 for i in range(0, 4)]

def get_mean(mean_matrix):
    temp = mean_matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    mean = float('{0:.2f}'.format(np.mean(mean_list)))
    return mean

def get_std(mean_matrix):
    temp = mean_matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    std = float('{0:.3f}'.format(np.std(mean_list)))
    return std

# Get different symbols (See for reference: https://plotly.com/python/marker-style/)
raw_symbols = SymbolValidator().values
namestems = []
namevariants = []
symbols = []
for i in range(0,len(raw_symbols),3):
    name = raw_symbols[i+2]
    symbols.append(raw_symbols[i])
    namestems.append(name.replace("-open", "").replace("-dot", ""))
    namevariants.append(name[len(namestems[-1]):])

# Load fancy colors
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
(188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]


# Define labels lists (just in case)
labels =["Session 1", "Session 2","Session 3","Session 4"]
labels_subjects = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Subject 6']
labels_int = [i for i in range(1, 7)]
x_rev = labels_int[::-1]

# Add first values for labels [Sub1...Sub6]
figb = go.Figure(data=go.Scatter(x=labels_int,
                                y=[-1000, -1000, -1000, -1000, -1000, -1000],
                                mode='markers',
                                showlegend=False,
                                marker_color='red'))


# Add MEAN ------ mp2rage ------ T1
for trace in range(0, len(mean_MP2RAGE_t1_matrix)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_MP2RAGE_t1_matrix[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i> sec" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'T<sub>1</sub> (mp2rage)',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_MP2RAGE_t1_matrix[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i> sec" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub> (mp2rage)',
                                  marker_color="rgb"+str(tableau20[0])))

# Add MEAN ------ mts ------ T1
for trace in range(0, len(mean_MTS_t1_matrix)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_MTS_t1_matrix[trace], 
                                  mode='markers',
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i> sec" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'T<sub>1</sub> (mts)',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))
        
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_MTS_t1_matrix[trace], 
                                  mode='markers',
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i> sec" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = False, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sup>1</sup> (mts)',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))

# Add MEAN ------ nAn ------ MTR
for trace in range(0, len(mean_mtr_matrix)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_mtr_matrix[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='MTR',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_mtr_matrix[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='MTR',
                                  marker_color="rgb"+str(tableau20[0])))
            

# Add MEAN ------ nAn ------ MTsat
for trace in range(0, len(mean_mtsat_matrix)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_mtsat_matrix[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='MTsat',
                                  marker_color="rgb"+str(tableau20[0])))
        
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_mtsat_matrix[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean : <i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='MTsat',
                                  marker_color="rgb"+str(tableau20[0])))
        

# Calculate means 
line_1   = get_mean(mean_MP2RAGE_t1_matrix)    # MP2RAGE_t1 --- mean 

line_2   = get_mean(mean_MTS_t1_matrix)        # MTS_t1     --- mean 

line_3   = get_mean(mean_mtr_matrix)           # MTR   --- mean

line_4   = get_mean(mean_mtsat_matrix)         # MTsat  --- mean



# Add dotted lines for first button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_1]*8,
                          mode='lines',
                          name='T<sub>1</sub>(mp2rage) mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_2]*8,
                          mode='lines',
                          name='T<sub>1</sub>(mts) mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[3]), 
                                    width=2,
                                    dash='dot')))

# Add dotted lines for second button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_3]*8,
                          mode='lines',
                          visible=False,
                          name='MTR mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))


# Add dotted lines for thrid button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_4]*8,
                          mode='lines',
                          visible=False,
                          name='MTsat mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))



x = [-1, 0, 1, 2, 3, 4, 5, 6]
x_rev = x[::-1]

std_1   = get_std(mean_MP2RAGE_t1_matrix)   # MP2RAGE_t1      --- std 

std_2   = get_std(mean_MTS_t1_matrix)       # MTS_t1          --- std 

std_3   = get_std(mean_mtr_matrix)          # N/A_mtr         --- std

std_4   = get_std(mean_mtsat_matrix)        # MTS_mtsat       --- std



# Add STD for 1 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_1+std_1]*8+[line_1-std_1]*8,
    fill='toself',
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='MP2RAGE_t1 STD',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_2+std_2]*8+[line_2-std_2]*8,
    fill='toself',
    fillcolor='rgba(255, 187, 120,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='MTS_t1 STD',
))

# Add STD for 2 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_3+std_3]*8+[line_3-std_3]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='MTR STD',
))

# Add STD for 3 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_4+std_4]*8+[line_4-std_4]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='MTsat STD',
))


figb.update_layout(title = '(2)  Neuromod anat QMRI (GM)',
                   updatemenus=[
                                dict(
                                    active = 0, 
                                    x=1.27,
                                    y=0.58,
                                    direction="down",
                                    yanchor="top",
                                    buttons=list([
                                        dict(label="(1) T<sub>1</sub>",
                                                     method="update",
                                                     args=[{"visible": [True] + [True]*12 + [False]*12 + [True]*2 + [False]*2 + [True]*2 + [False]*2},
                                                           
                                                           {"yaxis": dict(range=[0,3],
                                                                          title='s (seconds)',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="(2) MTR",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*12 + [True]*6 + [False]*6 + [False]*2 + [True]*1 +[False]*1 + [False]*2 + [True]*1 +[False]*1},
                                                           
                                                           {"yaxis": dict(range=[30,60],
                                                                          title='MTR (a.u)',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="(4) MTsat",
                                                     method="update",
                                                     args=[{"visible":  [True] + [False]*18 + [True]*6 + [False]*3 + [True]*1 + [False]*3 + [True]*1},
                                                           
                                                           {"yaxis": dict(range=[-10,15],
                                                                          title='MTsat (a.u.)',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]) ]) )],
                  title_x = 0.445, 
                  legend=dict(orientation = 'v',
                              bordercolor="Gray",
                              borderwidth=1),
                  xaxis=dict(range=[-0.45,5.45], 
                             mirror=True,
                             ticks='outside',
                             showline=True,
                             linecolor='#000',
                             tickvals = [0, 1, 2, 3, 4, 5],
                             ticktext = labels_subjects,
                             tickfont = dict(size=12)),
                  yaxis_title='s (seconds)',
                  yaxis=dict(range=[0,3], 
                             mirror=True,
                             ticks='outside', 
                             showline=True, 
                             linecolor='#000',
                             tickfont = dict(size=14)),
                   annotations=[
                               dict(text="Display metric: ", 
                                     showarrow=False,
                                     x=1.25,
                                     y=0.62,
                                     xref = 'paper',
                                     yref="paper")],
                  plot_bgcolor='rgba(227,233,244, 0.5)',
                  width = 760, 
                  height = 520,
                  font = dict(size = 13),
                  margin=go.layout.Margin(l=50,
                                         r=50,
                                         b=60,
                                        t=35))
# Plot figure
# For jupyter-book rendering --=-- jupyter-lab
plot(figb, filename = 'new-fig-2.html', config = config)
display(HTML('new-fig-2.html'))
# For local jupyter notebook --== binder session
# iplot(figb,config=config)