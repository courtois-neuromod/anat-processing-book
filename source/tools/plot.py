# Python imports 
from pathlib import Path
import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd
from tools.data import Data

class Plot:

    colours = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
               (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
               (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
               (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
               (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

    def __init__(self, dataset, plot_name):
        self.dataset = dataset
        self.plot_name = plot_name
        self.title = None
        self.xlabel = None

        self.hoverinfo = 'skip'

        # Text
        self.x_label_tick_font_size = 13
        self.y_label_tick_font_size = 13
        self.general_font_size = 13

    def get_val(self, matrix, key):
        temp = matrix[::]
        mean_list = []
        for ele in temp: 
            ele = [i for i in ele if i!=-100]
            mean_list.extend(ele)
            
        if key=='mean':
            val = float('{0:.2f}'.format(np.mean(mean_list)))
        if key=='std':
            val = float('{0:.3f}'.format(np.std(mean_list)))
        if key=='max':
            val = np.max(mean_list) + (np.max(mean_list)-np.min(mean_list))/4
        if key=='min':
            val = np.min(mean_list) - (np.max(mean_list)-np.min(mean_list))/4
            
        return val

    def display(self, env, tissue):

        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={'showLink': False, 'displayModeBar': False}

        # Get database
        df = self.dataset.data

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

                    if row['acquisition'] == 'MP2RAGE' and row['metric'] == 'T1map' and row['label'] == tissue: 
                        MEAN_mp2 = row['mean']
                    
                    if row['acquisition'] == 'MTS' and row['metric'] == 'T1map' and row['label'] == tissue:
                        MEAN_mts = row['mean']
                        
                    if row['metric'] == 'MTRmap' and row['label'] == tissue: 
                        MEAN_mtr = row['mean']
                        
                    if row['metric'] == 'MTsat' and row['label'] == tissue: 
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

        # Define labels lists (just in case)
        labels_subjects = ['Subject 1', 'Subject 2', 'Subject 3', 'Subject 4', 'Subject 5', 'Subject 6']
        labels_int = [i for i in range(1, 7)]

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
                showlegend = True
            else:
                showlegend = False

            figb.add_trace(go.Scatter(x=t, 
                                    y=mean_MP2RAGE_t1_matrix[trace], 
                                    mode='markers',
                                    legendgroup="group1",
                                    hovertemplate = 
                                    "Mean : <i> %{y: .2f} </i> sec" + 
                                    "<br>" + 
                                    "<b>%{text}</b>", 
                                    showlegend = showlegend, 
                                    text = ['Session {}'.format(i + 1) for i in range(4)],
                                    name= 'T<sub>1</sub> (mp2rage)',
                                    marker_color="rgb"+str(Plot.colours[0])))

        # Add MEAN ------ mts ------ T1
        for trace in range(0, len(mean_MTS_t1_matrix)):
            t = [trace - 0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False
            
            figb.add_trace(go.Scatter(x=t, 
                                    y=mean_MTS_t1_matrix[trace], 
                                    mode='markers',
                                    legendgroup="group2",
                                    hovertemplate = 
                                    "Mean : <i> %{y: .2f} </i> sec" + 
                                    "<br>" + 
                                    "<b>%{text}</b>", 
                                    showlegend = showlegend, 
                                    text = ['Session {}'.format(i + 1) for i in range(4)],
                                    name= 'T<sub>1</sub> (mts)',
                                    marker_symbol=symbols[5],
                                    marker_color="rgb"+str(Plot.colours[3])))

        # Add MEAN ------ nAn ------ MTR
        for trace in range(0, len(mean_mtr_matrix)):
            t = [trace -0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False

            figb.add_trace(go.Scatter(x=t, 
                                    y=mean_mtr_matrix[trace], 
                                    mode='markers',
                                    visible=False,
                                    showlegend = showlegend, 
                                    legendgroup="group1",
                                    hovertemplate = 
                                    "Mean : <i> %{y: .2f} </i>" + 
                                    "<br>" + 
                                    "<b>%{text}</b>", 
                                    text = ['Session {}'.format(i + 1) for i in range(4)],
                                    name='MTR',
                                    marker_color="rgb"+str(Plot.colours[0])))
                    

        # Add MEAN ------ nAn ------ MTsat
        for trace in range(0, len(mean_mtsat_matrix)):
            t = [trace -0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False

            figb.add_trace(go.Scatter(x=t, 
                                    y=mean_mtsat_matrix[trace], 
                                    mode='markers',
                                    visible=False,
                                    showlegend = showlegend, 
                                    legendgroup="group1",
                                    hovertemplate = 
                                    "Mean : <i> %{y: .2f} </i>" + 
                                    "<br>" + 
                                    "<b>%{text}</b>", 
                                    text = ['Session {}'.format(i + 1) for i in range(4)],
                                    name='MTsat',
                                    marker_color="rgb"+str(Plot.colours[0])))          

        # Calculate means 
        line = {
            'T<sub>1</sub>(mp2rage)': None,
            'T<sub>1</sub>(mts)': None,
            'MTR': None,
            'MTsat': None
        }

        line['T<sub>1</sub>(mp2rage)'] =  self.get_val(mean_MP2RAGE_t1_matrix, 'mean')    # MP2RAGE_t1 --- mean 
        line['T<sub>1</sub>(mts)'] =  self.get_val(mean_MTS_t1_matrix, 'mean')        # MTS_t1     --- mean 
        line['MTR'] = self.get_val(mean_mtr_matrix, 'mean')           # MTR   --- mean
        line['MTsat'] = self.get_val(mean_mtsat_matrix, 'mean')         # MTsat  --- mean

        for key in line:

            if key == 'T<sub>1</sub>(mts)':
                line_color = "rgb"+str(Plot.colours[3])
            else: 
                line_color = "rgb"+str(Plot.colours[0])

            visible=True
            if key == 'MTR' or key == 'MTsat':
                visible=False

            # Add dotted line
            figb.add_trace(go.Scatter(x=[-1, 0, 1, 2, 3, 4, 5, 6], 
                                    y=[line[key]]*8,
                                    mode='lines',
                                    visible=visible,
                                    name=key,
                                    opacity=0.5, 
                                    line=dict(color=line_color, 
                                                width=2,
                                                dash='dot')))

        x = [-1, 0, 1, 2, 3, 4, 5, 6]
        x_rev = x[::-1]

        # Calculate means 
        std_area = {
            'T<sub>1</sub>(mp2rage)': None,
            'T<sub>1</sub>(mts)': None,
            'MTR': None,
            'MTsat': None
        }

        std_area['T<sub>1</sub>(mp2rage)'] =  self.get_val(mean_MP2RAGE_t1_matrix, 'std')   # MP2RAGE_t1      --- std 
        std_area['T<sub>1</sub>(mts)'] =  self.get_val(mean_MTS_t1_matrix, 'std')       # MTS_t1          --- std 
        std_area['MTR'] = self.get_val(mean_mtr_matrix, 'std')          # N/A_mtr         --- std
        std_area['MTsat'] = self.get_val(mean_mtsat_matrix, 'std')        # MTS_mtsat       --- std

        for key in std_area:

            if key == 'T<sub>1</sub>(mts)':
                fillcolor='rgba(255, 187, 120, 0.15)'
            else: 
                fillcolor='rgba(31, 119, 180, 0.15)'

            visible=True
            if key == 'MTR' or key == 'MTsat':
                visible=False

            # Add STD
            figb.add_trace(go.Scatter(
                x=x+x_rev,
                y=[line[key]+std_area[key]]*8+[line[key]-std_area[key]]*8,
                fill='toself',
                visible=visible,
                fillcolor=fillcolor,
                line_color='rgba(255,255,255,0)',
                showlegend=False,
                hoverinfo=self.hoverinfo,
            ))

        figb.update_layout(title = self.title,
                        updatemenus=[
                                        dict(
                                            active = 0, 
                                            x=1.23,
                                            y=0.58,
                                            direction="down",
                                            yanchor="top",
                                            buttons=list([
                                                dict(label="T<sub>1</sub>",
                                                            method="update",
                                                            args=[{"visible": [True] + [True]*12 + [False]*12 + [True]*2 + [False]*2 + [True]*2 + [False]*2},
                                                                
                                                                {"yaxis": dict(range=[self.get_val(np.append(mean_MP2RAGE_t1_matrix, mean_MTS_t1_matrix, axis=0), 'min'), self.get_val(np.append(mean_MP2RAGE_t1_matrix, mean_MTS_t1_matrix, axis=0), 'max')],
                                                                                title='T<sub>1</sub> [s]',
                                                                                mirror=True,
                                                                                ticks='outside', 
                                                                                showline=True, 
                                                                                linecolor='#000',
                                                                                tickfont = dict(size=self.y_label_tick_font_size))}]),
                                                
                                                dict(label="MTR",
                                                            method="update",
                                                            args=[{"visible": [True] + [False]*12 + [True]*6 + [False]*6 + [False]*2 + [True]*1 +[False]*1 + [False]*2 + [True]*1 +[False]*1},
                                                                
                                                                {"yaxis": dict(range=[self.get_val(mean_mtr_matrix, 'min'), self.get_val(mean_mtr_matrix, 'max')],
                                                                                title='MTR [a.u.]',
                                                                                mirror=True,
                                                                                ticks='outside', 
                                                                                showline=True, 
                                                                                linecolor='#000',
                                                                                tickfont = dict(size=self.y_label_tick_font_size))}]),
                                                
                                                dict(label="MTsat",
                                                            method="update",
                                                            args=[{"visible":  [True] + [False]*18 + [True]*6 + [False]*3 + [True]*1 + [False]*3 + [True]*1},
                                                                
                                                                {"yaxis": dict(range=[self.get_val(mean_mtsat_matrix, 'min'), self.get_val(mean_mtsat_matrix, 'max')],
                                                                                title='MTsat [a.u.]',
                                                                                mirror=True,
                                                                                ticks='outside', 
                                                                                showline=True, 
                                                                                linecolor='#000',
                                                                                tickfont = dict(size=self.y_label_tick_font_size))}]) ]) )],
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
                                    tickfont = dict(size=self.x_label_tick_font_size)),
                        yaxis_title='T<sub>1</sub> [s]',
                        yaxis=dict(range=[self.get_val(np.append(mean_MP2RAGE_t1_matrix, mean_MTS_t1_matrix, axis=0), 'min'), self.get_val(np.append(mean_MP2RAGE_t1_matrix, mean_MTS_t1_matrix, axis=0), 'max')], 
                                    mirror=True,
                                    ticks='outside', 
                                    showline=True, 
                                    linecolor='#000',
                                    tickfont = dict(size=self.y_label_tick_font_size)),
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
                        font = dict(size = self.general_font_size),
                        margin=go.layout.Margin(l=50,
                                                r=50,
                                                b=60,
                                                t=35))
        # Plot figure

        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(figb, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(figb,config=config)
