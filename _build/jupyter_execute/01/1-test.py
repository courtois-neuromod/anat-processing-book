# Example notebook

## 1: Read and organize anatomical data 

Data used in notebook is avilable [here](https://github.com/courtois-neuromod/anat-processing/releases).

import pandas as pd

df_t1 = pd.read_csv("./../spinalcord_results/csa-SC_T1w.csv", converters={'project_id': lambda x: str(x)})
df_t2 = pd.read_csv("./../spinalcord_results/csa-SC_T2w.csv", converters={'project_id': lambda x: str(x)})

Display results for <code>csa-SC_T1w.csv</code>: 

df_t1

Display values for <code>csa-SC_T2w.csv</code>: 

df_t2

### 1.1: Modify <code>df_t1</code>

# Insert new columns for Subject and Session and start inserting values
df_t1.insert(0, "Subject", "Any")
df_t1.insert(1, "Session", "Any")

# Get Subject and Session from csv
for index, row in df_t1.iterrows():
    subject = int(row['Filename'].split("/")[6].split('-')[1])
    session = int(row['Filename'].split("/")[7].split("-")[1])
    df_t1.at[index, 'Subject'] =  subject
    df_t1.at[index, 'Session'] =  session

# Sort values based on Subject -- Session
df_2 = df_t1.sort_values(['Subject', 'Session'], ascending=[True, True])    

# Define lists for metrics
mean_area_matrix_1 = []
mean_ap_matrix_1 = []
mean_rl_matrix_1 = []
mean_angle_matrix_1 = []

# Get the values for all 4 metric [area, mean_AP, mean_RL, angle_AP]
for i in range(0, 6, 1):
    sub_values = df_2.loc[df_2['Subject'] == i+1]
    
    mean_area_ses = []
    
    mean_ap_ses = []

    mean_rl_ses = []

    mean_angle_ses = []
    
    for j in range(0, 4, 1):
        ses_values = sub_values.loc[sub_values['Session'] == j+1]
        
        mean_area = -100
        
        mean_ap = -100

        mean_rl = -100

        mean_angle = -100
        
        for index, row in ses_values.iterrows():
            # Read values
            MEAN_area = row['MEAN(area)']
            
            MEAN_diameter_AP = row['MEAN(diameter_AP)']

            MEAN_diameter_RL = row['MEAN(diameter_RL)']
            
            MEAN_angle_AP = row['MEAN(angle_AP)']
            
            # Store values
            mean_area = MEAN_area 
            
            mean_ap = MEAN_diameter_AP
            
            mean_rl = MEAN_diameter_RL
            
            mean_angle = MEAN_angle_AP
        
        # Append values to lists for sessions
        mean_area_ses.append(mean_area)
        
        mean_ap_ses.append(mean_ap)
        
        mean_rl_ses.append(mean_rl)

        mean_angle_ses.append(mean_angle)
        
        
    # Append session lists to main matrices for each metric
    mean_area_matrix_1.append(mean_area_ses)
    
    mean_ap_matrix_1.append(mean_ap_ses)
    
    mean_rl_matrix_1.append(mean_rl_ses)
    
    mean_angle_matrix_1.append(mean_angle_ses)

Compare *extracted values* and *results* from csv for validity:

mean_area_matrix_1[2]

subs = df_2.loc[df_2['Subject'] == 3]

for index, row in subs.iterrows():
    print("Subject", row['Subject'], "----Session", row['Session'], "---- MEAN(area):", row['MEAN(area)'])

### 1.2: Modify <code>df_t2</code>

# Insert new columns for Subject and Session and start inserting values
df_t2.insert(0, "Subject", "Any")
df_t2.insert(1, "Session", "Any")

# Get Subject and Session from csv
for index, row in df_t2.iterrows():
    subject = int(row['Filename'].split("/")[6].split('-')[1])
    session = int(row['Filename'].split("/")[7].split("-")[1])
    df_t2.at[index, 'Subject'] =  subject
    df_t2.at[index, 'Session'] =  session

# Sort values based on Subject -- Session
df_3 = df_t2.sort_values(['Subject', 'Session'], ascending=[True, True])

# Define lists for metrics
mean_area_matrix_2 = []
mean_ap_matrix_2 = []
mean_rl_matrix_2 = []
mean_angle_matrix_2 = []

# Get the values for all 4 metric [area, mean_AP, mean_RL, angle_AP]
for i in range(0, 6, 1):
    sub_values = df_3.loc[df_3['Subject'] == i+1]
    
    mean_area_ses = []
    
    mean_ap_ses = []

    mean_rl_ses = []

    mean_angle_ses = []
    
    for j in range(0, 4, 1):
        ses_values = sub_values.loc[sub_values['Session'] == j+1]
        
        mean_area = -100
        
        mean_ap = -100

        mean_rl = -100

        mean_angle = -100

        
        
        for index, row in ses_values.iterrows():
            # Read values
            MEAN_area = row['MEAN(area)']
            
            MEAN_diameter_AP = row['MEAN(diameter_AP)']

            MEAN_diameter_RL = row['MEAN(diameter_RL)']
            
            MEAN_angle_AP = row['MEAN(angle_AP)']
            
            # Store values
            mean_area = MEAN_area 
            
            mean_ap = MEAN_diameter_AP
            
            mean_rl = MEAN_diameter_RL
            
            mean_angle = MEAN_angle_AP
        
        # Append values to lists for sessions
        mean_area_ses.append(mean_area)
        
        mean_ap_ses.append(mean_ap)
        
        mean_rl_ses.append(mean_rl)

        mean_angle_ses.append(mean_angle)
        
        
        
    # Append session lists to main matrices for each metric
    mean_area_matrix_2.append(mean_area_ses)
    
    mean_ap_matrix_2.append(mean_ap_ses)
    
    mean_rl_matrix_2.append(mean_rl_ses)
    
    mean_angle_matrix_2.append(mean_angle_ses)

Compare *extracted values* and *results* from csv for validity:

mean_area_matrix_2[2]

subs = df_3.loc[df_3['Subject'] == 3]

for index, row in subs.iterrows():
    print("Subject", row['Subject'], "----Session", row['Session'], "---- MEAN(area):", row['MEAN(area)'])

## 2: Plot data [T<sub>1</sub>w / T<sub>2</sub>w]

t1 = [-0.2, -0.06, 0.08, 0.22]
t2 = [0 -0.2 + i*0.14 for i in range(0, 4)]

for trace in range(0, len(mean_ap_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    print(trace, ": ", t)

import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from IPython.core.display import display, HTML

# Add plotly 
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}

# Different shapes can been seen here: https://github.com/plotly/plotly.py/issues/2182
# I used the one with index 102 (outline of a dimond)

# Load fancy colors
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (241, 119, 32),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
(188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]


# Define labels lists (just in case)
labels =["Session 1", "Session 2","Session 3","Session 4"]
labels_subjects = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Subject 6']
labels_int = [i for i in range(1, 7)]

# Add first values for labels [Sub1...Sub6]
figb = go.Figure(data=go.Scatter(x=labels_int,
                                y=[-1000, -1000, -1000, -1000, -1000, -1000],
                                mode='markers',
                                showlegend=False,
                                marker_color='red'))


# Add MEAN [area] --- > T1w
for trace in range(0, len(mean_area_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_area_matrix_1[trace], 
                              mode='markers',
                              hovertemplate = 
                              "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>1</sub>w]',
                              marker_color="rgb"+str(tableau20[0])))
# Add MEAN [area] --- > T2w
for trace in range(0, len(mean_area_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_area_matrix_2[trace], 
                              mode='markers',
                              hovertemplate = 
                              "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>2</sub>w]',
                              marker_symbol=102,
                              marker_color="rgb"+str(tableau20[3])))

# Add MEAN [AP] --- > T1w
for trace in range(0, len(mean_ap_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_ap_matrix_1[trace], 
                              mode='markers',
                              visible=False,
                              hovertemplate = 
                              "Mean [AP]: <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>1</sub>w]',
                              marker_color="rgb"+str(tableau20[0])))

# Add MEAN [AP] --- > T2w
for trace in range(0, len(mean_ap_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_ap_matrix_2[trace], 
                              mode='markers',
                              visible=False,
                              hovertemplate = 
                              "Mean [AP]: <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              marker_symbol=102,
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>2</sub>w]',
                              marker_color="rgb"+str(tableau20[3])))
    
# Add MEAN [RL] --- > T1w
for trace in range(0, len(mean_rl_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_rl_matrix_1[trace], 
                              mode='markers',
                              visible=False,
                              hovertemplate = 
                              "Mean (RL): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>1</sub>w]',
                              marker_color="rgb"+str(tableau20[0])))
    
# Add MEAN [RL] --- > T2w
for trace in range(0, len(mean_rl_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_rl_matrix_2[trace], 
                              mode='markers',
                              visible=False,
                              hovertemplate = 
                              "Mean (RL): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>2</sub>w]',
                              marker_symbol=102,
                              marker_color="rgb"+str(tableau20[3])))
    
# Add MEAN [angle_AP] --- > T1w
for trace in range(0, len(mean_angle_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_angle_matrix_1[trace], 
                              mode='markers',
                              visible=False,
                              hovertemplate = 
                              "Mean (angle_AP): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>1</sub>w]',
                              marker_color="rgb"+str(tableau20[0])))
    
# Add MEAN [angle_AP] --- > T2w
for trace in range(0, len(mean_angle_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    figb.add_trace(go.Scatter(x=t, 
                              y=mean_angle_matrix_2[trace], 
                              mode='markers',
                              visible=False,
                              hovertemplate = 
                              "Mean (angle_AP): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                              "<br>" + 
                              "<b>%{text}</b>", 
                              text = ['Session {}'.format(i + 1) for i in range(4)],
                              name=labels_subjects[trace] + ' [T<sub>2</sub>w]',
                              marker_symbol=102,
                              marker_color="rgb"+str(tableau20[3])))

# Add dotted line for first trace
figb.add_shape(type="line",
    x0=-1, y0=70, x1=6, y1=70,
    line=dict(
        color="red",
        width=1,
        dash="dot",
    )
)

figb.update_layout(title = '(1) Spinal cord CSA [T<sub>1</sub>w/T<sub>2</sub>w]',
                   updatemenus=[
                                dict(
                                    active = 0, 
                                    x=1.32,
                                    y=0.28,
                                    direction="down",
                                    yanchor="top",
                                    buttons=list([
                                        dict(label="(a) Mean (area)",
                                                     method="update",
                                                     args=[{"visible": [True] + [True]*12 + [False]*36},
                                                           
                                                           {"shapes": [dict( type="line",
                                                                            x0=-1, y0=70, x1=6, y1=70,
                                                                            line=dict(
                                                                                color="red",
                                                                                width=1,
                                                                                dash="dot",
                                                                            ))],
                                                            
                                                             "yaxis": dict(range=[0,100],
                                                                          title='mm<sup>2</sup>',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="(b) Mean (AP)",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*12 + [True]*12 + [False]*24},
                                                           
                                                           {"shapes": [dict( type="line",
                                                                            x0=-1, y0=7, x1=6, y1=7,
                                                                            line=dict(
                                                                                color="red",
                                                                                width=1,
                                                                                dash="dot",
                                                                            ))],
                                                            
                                                             "yaxis": dict(range=[0,15],
                                                                          title='mm<sup>2</sup>',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                    
                                        dict(label="(c) Mean (RL)",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*24 + [True]*12 + [False]*12},
                                                           
                                                           {"shapes": [dict( type="line",
                                                                            x0=-1, y0=12, x1=8, y1=12,
                                                                            line=dict(
                                                                                color="red",
                                                                                width=1,
                                                                                dash="dot",
                                                                            ))],
                                                            
                                                             "yaxis": dict(range=[0,15],
                                                                          title='mm<sup>2</sup>',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="(d) Mean (angle)",
                                                     method="update",
                                                     args=[{"visible":  [True] + [False]*36 + [True]*12},
                                                           
                                                           {"shapes": [dict( type="line",
                                                                            x0=-1, y0=0, x1=6, y1=0,
                                                                            line=dict(
                                                                                color="red",
                                                                                width=1,
                                                                                dash='dot'
                                                                            ))],
                                                            
                                                            "yaxis": dict(range=[-10,15],
                                                                          title='mm<sup>2</sup>',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]) ]) )],
                  title_x = 0.445, 
                  legend=dict(title='Sessions for:',
                              orientation = 'v',
                              bordercolor="Gray",
                              borderwidth=1),
#                    hovermode='y unified',
                  xaxis=dict(range=[-0.45,5.45], 
                             mirror=True,
                             ticks='outside',
                             showline=True,
                             linecolor='#000',
                             tickvals = [0, 1, 2, 3, 4, 5],
                             ticktext = labels_subjects,
                             tickfont = dict(size=13)),
                  yaxis_title='mm<sup>2</sup>',
                  yaxis=dict(range=[0,100], 
                             mirror=True,
                             ticks='outside', 
                             showline=True, 
                             linecolor='#000',
                             tickfont = dict(size=14)),
                   annotations=[
                               dict(text="Display metric: ", 
                                     showarrow=False,
                                     x=1.25,
                                     y=0.278,
                                     xref = 'paper',
                                     yref="paper")],
                  plot_bgcolor='#fff', 
                  width = 760, 
                  height = 520,
                  font = dict(size = 13),
                  margin=go.layout.Margin(l=50,
                                         r=50,
                                         b=60,
                                        t=35))
# Plot figure
# For jupyter-book rendering --=-- jupyter-lab
plot(figb, filename = './figure-outputs/new-fig.html', config = config)
display(HTML('./figure-outputs/new-fig.html'))

# For local jupyter notebook --== binder session
# iplot(figb,config=config)