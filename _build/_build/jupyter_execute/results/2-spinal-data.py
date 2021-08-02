# Spinal cord data

## Spinal cord CSA

# Get data from github repo
!wget -O spinalcord_results.zip https://github.com/courtois-neuromod/anat-processing/releases/download/r20210610/spinalcord_results.zip
!unzip -j spinalcord_results.zip -d ./spinalcord_results/

# Python imports 
import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd

# Add plotly 
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}

# Load  the data
df_t1 = pd.read_csv("./spinalcord_results/csa-SC_T1w.csv", converters={'project_id': lambda x: str(x)})
df_t2 = pd.read_csv("./spinalcord_results/csa-SC_T2w.csv", converters={'project_id': lambda x: str(x)})

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


# Functions for mean and std    
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

# Functions for getting y label limits
def get_limit_max(matrix):
    temp = matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    return np.max(mean_list) + (np.max(mean_list)-np.min(mean_list))/4

def get_limit_min(matrix):
    temp = matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    return np.min(mean_list) - (np.max(mean_list)-np.min(mean_list))/4


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



# Define lists needed for plotting 
t1 = [-0.2, -0.06, 0.08, 0.22]
t2 = [0 -0.2 + i*0.14 for i in range(0, 4)]
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


# Add MEAN [area] --- > T1w
for trace in range(0, len(mean_area_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_area_matrix_1[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_area_matrix_1[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
# Add MEAN [area] --- > T2w
for trace in range(0, len(mean_area_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_area_matrix_2[trace], 
                                  mode='markers',
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'T<sub>2</sub>w',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))
        
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_area_matrix_2[trace], 
                                  mode='markers',
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = False, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))

# Add MEAN [AP] --- > T1w
for trace in range(0, len(mean_ap_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_ap_matrix_1[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean [AP]: <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_ap_matrix_1[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean [AP]: <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
            

# Add MEAN [AP] --- > T2w
for trace in range(0, len(mean_ap_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_ap_matrix_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean [AP]: <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  marker_symbol=symbols[5],
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_color="rgb"+str(tableau20[3])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_ap_matrix_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean [AP]: <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  marker_symbol=symbols[5],
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_color="rgb"+str(tableau20[3])))
    
# Add MEAN [RL] --- > T1w
for trace in range(0, len(mean_rl_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_rl_matrix_1[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean (RL): <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
        
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_rl_matrix_1[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean (RL): <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
        
    
# Add MEAN [RL] --- > T2w
for trace in range(0, len(mean_rl_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_rl_matrix_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean (RL): <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_rl_matrix_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean (RL): <i> %{y: .2f} </i> mm" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))
# Add MEAN [angle_AP] --- > T1w
for trace in range(0, len(mean_angle_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_angle_matrix_1[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean (angle_AP): <i> %{y: .2f} </i>°" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
        
    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_angle_matrix_1[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean (angle_AP): <i> %{y: .2f} </i>°" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>w',
                                  marker_color="rgb"+str(tableau20[0])))
    
# Add MEAN [angle_AP] --- > T2w
for trace in range(0, len(mean_angle_matrix_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_angle_matrix_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = True, 
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean (angle_AP): <i> %{y: .2f} </i>°" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))

    else: 
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_angle_matrix_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  showlegend = False, 
                                  legendgroup="group2",
                                  hovertemplate = 
                                  "Mean (angle_AP): <i> %{y: .2f} </i>°" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>w',
                                  marker_symbol=symbols[5],
                                  marker_color="rgb"+str(tableau20[3])))
        
# Calculate means 
line_1   = get_mean(mean_area_matrix_1)    # T1w mean area --- mean 
line_2   = get_mean(mean_area_matrix_2)    # T2w mean area --- mean 

line_3   = get_mean(mean_ap_matrix_1)      # T1w mean AP   --- mean
line_4   = get_mean(mean_ap_matrix_2)      # T2w mean AP   --- mean

line_5   = get_mean(mean_rl_matrix_1)      # T1w mean RL  --- mean
line_6   = get_mean(mean_rl_matrix_2)      # T2w mean RL  --- mean

line_7   = get_mean(mean_angle_matrix_1)   # T1w angle    --- mean
line_8   = get_mean(mean_angle_matrix_2)   # T2w angle    --- mean


# Add dotted lines for first button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_1]*8,
                          mode='lines',
                          name='T<sub>1</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_2]*8,
                          mode='lines',
                          name='T<sub>2</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[3]), 
                                    width=2,
                                    dash='dot')))

# Add dotted lines for second button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_3]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>1</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_4]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>2</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[3]), 
                                    width=2,
                                    dash='dot')))

# Add dotted lines for thrid button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_5]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>1</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_6]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>2</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[3]), 
                                    width=2,
                                    dash='dot')))

# Add dotted lines for forth button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_7]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>1</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_8]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>2</sub>w mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[3]), 
                                    width=2,
                                    dash='dot')))


x = [-1, 0, 1, 2, 3, 4, 5, 6]
x_rev = x[::-1]

std_1   = get_std(mean_area_matrix_1)    # T1w mean area --- std 
std_2   = get_std(mean_area_matrix_2)    # T2w mean area --- std 

std_3   = get_std(mean_ap_matrix_1)      # T1w mean AP   --- std
std_4   = get_std(mean_ap_matrix_2)      # T2w mean AP   --- std

std_5   = get_std(mean_rl_matrix_1)      # T1w mean RL  --- std
std_6   = get_std(mean_rl_matrix_2)      # T2w mean RL  --- std

std_7   = get_std(mean_angle_matrix_1)   # T1w angle    --- std
std_8   = get_std(mean_angle_matrix_2)   # T2w angle    --- std


# Add STD for 1 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_1+std_1]*8+[line_1-std_1]*8,
    fill='toself',
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T1w STD',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_2+std_2]*8+[line_2-std_2]*8,
    fill='toself',
    fillcolor='rgba(255, 187, 120,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T2w STD',
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
    name='T1w STD',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_4+std_4]*8+[line_4-std_4]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(255, 187, 120,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T1w STD',
))

# Add STD for 3 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_5+std_5]*8+[line_5-std_5]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T1w STD',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_6+std_6]*8+[line_6-std_6]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(255, 187, 120,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T1w STD',
))

# Add STD for 4 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_7+std_7]*8+[line_7-std_7]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T1w STD',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_8+std_8]*8+[line_8-std_8]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(255, 187, 120,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T1w STD',
))


figb.update_layout(title = '  Spinal cord CSA [T<sub>1</sub>w/T<sub>2</sub>w]',
                   updatemenus=[
                                dict(
                                    active = 0, 
                                    x=1.27,
                                    y=0.58,
                                    direction="down",
                                    yanchor="top",
                                    buttons=list([
                                        dict(label="Mean (area)",
                                                     method="update",
                                                     args=[{"visible": [True] + [True]*12 + [False]*36 + [True]*2 + [False]*6 + [True]*2 + [False]*6},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(np.append(mean_area_matrix_1, mean_area_matrix_2, axis=0)), get_limit_max(np.append(mean_area_matrix_1, mean_area_matrix_2, axis=0))],
                                                                          title='mm<sup>2</sup>',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="Mean (AP)",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*12 + [True]*12 + [False]*24 + [False]*2 + [True]*2 +[False]*4 + [False]*2 + [True]*2 +[False]*4},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(np.append(mean_ap_matrix_1, mean_ap_matrix_2, axis=0)), get_limit_max(np.append(mean_ap_matrix_1, mean_ap_matrix_2, axis=0))],
                                                                          title='mm',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                    
                                        dict(label="Mean (RL)",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*24 + [True]*12 + [False]*12 + [False]*4 + [True]*2 +[False]*2 + [False]*4 + [True]*2 +[False]*2},
                                                    
                                                           {"yaxis": dict(range=[get_limit_min(np.append(mean_rl_matrix_1, mean_rl_matrix_2, axis=0)), get_limit_max(np.append(mean_rl_matrix_1, mean_rl_matrix_2, axis=0))],
                                                                          title='mm',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="Mean (angle)",
                                                     method="update",
                                                     args=[{"visible":  [True] + [False]*36 + [True]*12 + [False]*6 + [True]*2 + [False]*6 + [True]*2 },
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(np.append(mean_angle_matrix_1, mean_angle_matrix_2, axis=0)), get_limit_max(np.append(mean_angle_matrix_1, mean_angle_matrix_2, axis=0))],
                                                                          title='degrees (°)',
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
                  yaxis_title='mm<sup>2</sup>',
                  yaxis=dict(range=[get_limit_min(np.append(mean_area_matrix_1, mean_area_matrix_2, axis=0)), get_limit_max(np.append(mean_area_matrix_1, mean_area_matrix_2, axis=0))], 
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
plot(figb, filename = 'new-fig.html', config = config)
display(HTML('new-fig.html'))
# For local jupyter notebook --== binder session
# iplot(figb,config=config)

## Gray matter CSA

import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd
# Add plotly 
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}

# Load  the data
df_3 = pd.read_csv("./spinalcord_results/csa-GM_T2s.csv", converters={'project_id': lambda x: str(x)})

# Insert new columns for Subject and Session and start inserting values
df_3.insert(0, "Subject", "Any")
df_3.insert(1, "Session", "Any")

# Get Subject and Session from csv
for index, row in df_3.iterrows():
    subject = int(row['Filename'].split("/")[6].split('-')[1])
    session = int(row['Filename'].split("/")[7].split("-")[1])
    df_3.at[index, 'Subject'] =  subject
    df_3.at[index, 'Session'] =  session

# Sort values based on Subject -- Session
df_3 = df_3.sort_values(['Subject', 'Session'], ascending=[True, True])   

# Define lists for metrics
mean_area_matrix_1 = []


# Get the values for all 4 metric [area, mean_AP, mean_RL, angle_AP]
for i in range(0, 6, 1):
    sub_values = df_3.loc[df_3['Subject'] == i+1]
    
    mean_area_ses = []
    
    
    for j in range(0, 4, 1):
        ses_values = sub_values.loc[sub_values['Session'] == j+1]
        
        mean_area = -100
        
        
        for index, row in ses_values.iterrows():
            # Read values
            MEAN_area = row['MEAN(area)']
            
            # Store values
            mean_area = MEAN_area 
        
        # Append values to lists for sessions
        mean_area_ses.append(mean_area)

        
        
    # Append session lists to main matrices for each metric
    mean_area_matrix_1.append(mean_area_ses)
    
# Functions for mean and std    
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

# Functions for getting y label limits
def get_limit_max(matrix):
    temp = matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    return np.max(mean_list) + (np.max(mean_list)-np.min(mean_list))/4

def get_limit_min(matrix):
    temp = matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    return np.min(mean_list) - (np.max(mean_list)-np.min(mean_list))/4

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



# Define lists needed for plotting 
t1 = [-0.2, -0.06, 0.08, 0.22]
t2 = [0 -0.2 + i*0.14 for i in range(0, 4)]
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


# Add MEAN [area] --- > T1w
for trace in range(0, len(mean_area_matrix_1)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_area_matrix_1[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'T<sub>2</sub>s',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=mean_area_matrix_1[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "Mean (area): <i> %{y: .2f} </i> mm<sup>2</sup>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>2</sub>s',
                                  marker_color="rgb"+str(tableau20[0])))

# Calculate means 
line_1   = get_mean(mean_area_matrix_1)    # T2s mean area --- mean 


# Add dotted lines for first button 
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_1]*8,
                          mode='lines',
                          name='T<sub>2</sub>s mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

x = [-1, 0, 1, 2, 3, 4, 5, 6]
x_rev = x[::-1]

std_1   = get_std(mean_area_matrix_1)    # T1s mean area --- std 


# Add STD for 1 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_1+std_1]*8+[line_1-std_1]*8,
    fill='toself',
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='T2s STD',
))

figb.update_layout(title = 'Spinal cord gray matter CSA',
                  title_x = 0.5, 
                  showlegend=False,
                  xaxis=dict(range=[-0.45,5.45], 
                             mirror=True,
                             ticks='outside',
                             showline=True,
                             linecolor='#000',
                             tickvals = [0, 1, 2, 3, 4, 5],
                             ticktext = labels_subjects,
                             tickfont = dict(size=12)),
                  yaxis_title='mm<sup>2</sup>',
                  yaxis=dict(range=[get_limit_min(mean_area_matrix_1), get_limit_max(mean_area_matrix_1)], 
                             mirror=True,
                             ticks='outside', 
                             showline=True, 
                             linecolor='#000',
                             tickfont = dict(size=14)),
                  plot_bgcolor='rgba(227,233,244, 0.5)',
                  width = 640, 
                  height = 520,
                  font = dict(size = 12),
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

## White matter qMRI

import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd

# Add plotly 
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}

# Read data for (DWI_FA, DWI_MD, DWI_RD, MTR, MTsat, T1)
df_dwi_fa = pd.read_csv("./spinalcord_results/DWI_FA.csv", converters={'project_id': lambda x: str(x)})
df_dwi_md = pd.read_csv("./spinalcord_results/DWI_MD.csv", converters={'project_id': lambda x: str(x)})
df_dwi_rd = pd.read_csv("./spinalcord_results/DWI_RD.csv", converters={'project_id': lambda x: str(x)})
df_mtr    = pd.read_csv("./spinalcord_results/MTR.csv", converters={'project_id': lambda x: str(x)})
df_mtsat  = pd.read_csv("./spinalcord_results/MTsat.csv", converters={'project_id': lambda x: str(x)})
df_t1_2   = pd.read_csv("./spinalcord_results/T1.csv", converters={'project_id': lambda x: str(x)})

# Function for reading session values 
def get_sessions_values(df, metric):
    '''

    :param df: pandas dataframe with results
    :param metric: column in dataframe
    :return: session values as matrix 
    '''
    df.insert(0, "Subject", "Any")
    df.insert(1, "Session", "Any")

    # Get Subject and Session from csv
    for index, row in df.iterrows():
        subject = int(row['Filename'].split("/")[6].split('-')[1])
        session = int(row['Filename'].split("/")[7].split("-")[1])
        df.at[index, 'Subject'] = subject
        df.at[index, 'Session'] = session

    # Sort values based on Subject -- Session
    df_2 = df.sort_values(['Subject', 'Session'], ascending=[True, True])

    # Define lists for metrics
    matrix_1 = []

    # Get the values for all desired column (metric)
    for i in range(0, 6, 1):
        sub_values = df_2.loc[df_2['Subject'] == i + 1]
        ses = []

        for j in range(0, 4, 1):
            ses_values = sub_values.loc[sub_values['Session'] == j + 1]

            temp = -100

            for index, row in ses_values.iterrows():
                # Read values
                my_value = row[metric]

                # Store values
                temp = my_value

                # Append values to lists for sessions
            ses.append(temp)

        # Append session lists to main matrices for each metric
        matrix_1.append(ses)

    return matrix_1

# Get values for sessions, store in lists 
matrix_dwi_fa = get_sessions_values(df=df_dwi_fa,metric="WA()")
matrix_dwi_md = get_sessions_values(df=df_dwi_md, metric="WA()")
matrix_dwi_rd = get_sessions_values(df=df_dwi_rd, metric="WA()")
matrix_mtr    = get_sessions_values(df=df_mtr, metric="WA()")
matrix_mtsat  = get_sessions_values(df=df_mtsat, metric="WA()")
matrix_t1_2   = get_sessions_values(df=df_t1_2, metric="WA()")


# Functions for calculating mean and std from lists   
def get_mean(mean_matrix):
    temp = mean_matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    mean = float('{0:.7f}'.format(np.mean(mean_list)))
    return mean

def get_std(mean_matrix):
    temp = mean_matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    std = float('{0:.7}'.format(np.std(mean_list)))
    return std

# Functions for getting y label limits
def get_limit_max(matrix):
    temp = matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    return np.max(mean_list) + (np.max(mean_list)-np.min(mean_list))/4

def get_limit_min(matrix):
    temp = matrix[::]
    mean_list = []
    for ele in temp: 
        ele = [i for i in ele if i!=-100]
        mean_list.extend(ele)
    
    return np.min(mean_list) - (np.max(mean_list)-np.min(mean_list))/4

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


# Define lists needed for plotting 
t1 = [-0.2, -0.06, 0.08, 0.22]
t2 = [0 -0.2 + i*0.14 for i in range(0, 4)]
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
# Add DWI_FA 
for trace in range(0, len(matrix_dwi_fa)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_dwi_fa[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "<i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'DWI_FA',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_dwi_fa[trace], 
                                  mode='markers',
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "<i> %{y: .2f}" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='DWI_FA',
                                  marker_color="rgb"+str(tableau20[0])))


# Add DWI_MD
for trace in range(0, len(matrix_dwi_md)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_dwi_md[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "<i> %{y: .6f} </i> mm<sup>2</sup>/s" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'DWI_MD',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_dwi_md[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "<i> %{y: .6f} mm<sup>2</sup>/s" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='DWI_MD',
                                  marker_color="rgb"+str(tableau20[0])))

        
# Add DWI_RD
for trace in range(0, len(matrix_dwi_rd)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_dwi_rd[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "<i> %{y: .6f} </i> mm<sup>2</sup>/s" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'DWI_RD',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_dwi_rd[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "<i> %{y: .6f} mm<sup>2</sup>/s" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='DWI_RD',
                                  marker_color="rgb"+str(tableau20[0])))

        
# Add MTR
for trace in range(0, len(matrix_mtr)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_mtr[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "<i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'MTR',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_mtr[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "<i> %{y: .2f}" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='MTR',
                                  marker_color="rgb"+str(tableau20[0])))

# Add MTsat
for trace in range(0, len(matrix_mtsat)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_mtsat[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "<i> %{y: .2f} </i>" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'MTsat',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_mtsat[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "<i> %{y: .2f}" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='MTsat',
                                  marker_color="rgb"+str(tableau20[0])))

# Add T1
for trace in range(0, len(matrix_t1_2)):
    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
    
    if trace == 0: 
    
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_t1_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  hovertemplate = 
                                  "<i> %{y: .7f} </i> sec" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  showlegend = True, 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name= 'T<sub>1</sub>',
                                  marker_color="rgb"+str(tableau20[0])))
    else: 
        
        figb.add_trace(go.Scatter(x=t, 
                                  y=matrix_t1_2[trace], 
                                  mode='markers',
                                  visible=False,
                                  legendgroup="group1",
                                  showlegend = False, 
                                  hovertemplate = 
                                  "<i> %{y: .7f} sec" + 
                                  "<br>" + 
                                  "<b>%{text}</b>", 
                                  text = ['Session {}'.format(i + 1) for i in range(4)],
                                  name='T<sub>1</sub>',
                                  marker_color="rgb"+str(tableau20[0])))
        
        
# Calculate means 
line_1   = get_mean(matrix_dwi_fa)      # DWI_FA  --- mean 
line_2   = get_mean(matrix_dwi_md)      # DWI_MD  --- mean 
line_3   = get_mean(matrix_dwi_rd)      # DWI_RD  --- mean
line_4   = get_mean(matrix_mtr)         # MTR     --- mean
line_5   = get_mean(matrix_mtsat)       # MTsat   --- mean
line_6   = get_mean(matrix_t1_2)        # T1      --- mean



# Add dotted lines for buttons
figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_1]*8,
                          mode='lines',
                          name='DWI_FA mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_2]*8,
                          mode='lines',
                          visible=False,
                          name='DWI_MD mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))


figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_3]*8,
                          mode='lines',
                          visible=False,
                          name='DWI_RD mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_4]*8,
                          mode='lines',
                          visible=False,
                          name='MTR mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))


figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_5]*8,
                          mode='lines',
                          visible=False,
                          name='MTsat mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))

figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                          y=[line_6]*8,
                          mode='lines',
                          visible=False,
                          name='T<sub>1</sub> mean',
                          opacity=0.5, 
                          line=dict(color="rgb"+str(tableau20[0]), 
                                    width=2,
                                    dash='dot')))


x = [-1, 0, 1, 2, 3, 4, 5, 6]
x_rev = x[::-1]

std_1   = get_std(matrix_dwi_fa)     # DWI_FA   --- std 
std_2   = get_std(matrix_dwi_md)     # DWI_MD   --- std 

std_3   = get_std(matrix_dwi_rd)     # DWI_RD   --- std
std_4   = get_std(matrix_mtr)        # MTR      --- std

std_5   = get_std(matrix_mtsat)      # MTsat    --- std
std_6   = get_std(matrix_t1_2)       # T1       --- std




# Add STD for buttons
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_1+std_1]*8+[line_1-std_1]*8,
    fill='toself',
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_2+std_2]*8+[line_2-std_2]*8,
    fill='toself',
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='',
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
    name='',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_4+std_4]*8+[line_4-std_4]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='',
))

# Add STD for 3 button
figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_5+std_5]*8+[line_5-std_5]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='',
))

figb.add_trace(go.Scatter(
    x=x+x_rev,
    y=[line_6+std_6]*8+[line_6-std_6]*8,
    fill='toself',
    visible=False,
    fillcolor='rgba(31, 119, 180,0.15)',
    line_color='rgba(255,255,255,0)',
    showlegend=False,
    hoverinfo='skip',
    name='',
))

figb.update_layout(title = 'Spinal cord qMRI microstructure ',
                   updatemenus=[
                                dict(
                                    active = 0, 
                                    x=1.24,
                                    y=0.58,
                                    direction="down",
                                    yanchor="top",
                                    buttons=list([
                                        dict(label="DWI_FA",
                                                     method="update",
                                                     args=[{"visible": [True] + [True]*6 + [False]*30 + [True]*1 + [False]*5 + [True]*1 + [False]*5},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(matrix_dwi_fa), get_limit_max(matrix_dwi_fa)],
                                                                          title='a.u.',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="DWI_MD",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*6 + [True]*6 + [False]*24 + [False]*1 + [True]*1 +[False]*4 + [False]*1 + [True]*1 +[False]*4},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(matrix_dwi_md), get_limit_max(matrix_dwi_md)],
                                                                          title='mm<sup>2</sup>/s',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="DWI_RD",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*12 + [True]*6 + [False]*18 + [False]*2 + [True]*1 +[False]*3 + [False]*2 + [True]*1 +[False]*3},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(matrix_dwi_rd), get_limit_max(matrix_dwi_rd)],
                                                                          title='mm<sup>2</sup>/s',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        dict(label="MTR",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*18 + [True]*6 + [False]*12 + [False]*3 + [True]*1 +[False]*2 + [False]*3 + [True]*1 +[False]*2},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(matrix_mtr), get_limit_max(matrix_mtr)],
                                                                          title='a.u.',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                    
                                        dict(label="MTsat",
                                                     method="update",
                                                     args=[{"visible": [True] + [False]*24 + [True]*6 + [False]*6 + [False]*4 + [True]*1 +[False]*1 + [False]*4 + [True]*1 +[False]*1},
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(matrix_mtsat), get_limit_max(matrix_mtsat)],
                                                                          title='a.u.',
                                                                          mirror=True,
                                                                          ticks='outside', 
                                                                          showline=True, 
                                                                          linecolor='#000',
                                                                          tickfont = dict(size=16))}]),
                                        
                                        dict(label="T<sub>1</sub>",
                                                     method="update",
                                                     args=[{"visible":  [True] + [False]*30 + [True]*6 + [False]*5 + [True]*1 + [False]*5 + [True]*1 },
                                                           
                                                           {"yaxis": dict(range=[get_limit_min(matrix_t1_2), get_limit_max(matrix_t1_2)],
                                                                          title='s (seconds)',
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
                  yaxis_title='a.u.',
                  yaxis=dict(range=[get_limit_min(matrix_dwi_fa), get_limit_max(matrix_dwi_fa)], 
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
plot(figb, filename = 'new-fig-3.html', config = config)
display(HTML('new-fig-3.html'))
# For local jupyter notebook --== binder session
# iplot(figb,config=config)