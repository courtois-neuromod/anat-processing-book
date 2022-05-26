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
    
    def get_symbols(self):
        # Get different symbols (See for reference: https://plotly.com/python/marker-style/)
        raw_symbols = SymbolValidator().values
        symbols = []
        for i in range(0,len(raw_symbols),3):
            symbols.append(raw_symbols[i])
        
        return symbols

    def display(self, env, tissue):

        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={'showLink': False, 'displayModeBar': False}

        # Get database
        matrix = self.dataset.extract_data(tissue)

        symbols = self.get_symbols()

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
        for trace in range(0, len(matrix['MP2RAGE'])):
            t = [trace -0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False

            figb.add_trace(go.Scatter(x=t, 
                                    y=matrix['MP2RAGE'][trace], 
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
        for trace in range(0, len(matrix['MTS'])):
            t = [trace - 0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False
            
            figb.add_trace(go.Scatter(x=t, 
                                    y=matrix['MTS'][trace], 
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
        for trace in range(0, len(matrix['MTR'])):
            t = [trace -0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False

            figb.add_trace(go.Scatter(x=t, 
                                    y=matrix['MTR'][trace], 
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
        for trace in range(0, len(matrix['MTsat'])):
            t = [trace -0.2 + i*0.14 for i in range(0, 4)]
            
            if trace == 0: 
                showlegend = True
            else:
                showlegend = False

            figb.add_trace(go.Scatter(x=t, 
                                    y=matrix['MTsat'][trace], 
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

        line['T<sub>1</sub>(mp2rage)'] =  self.get_val(matrix['MP2RAGE'], 'mean')    # MP2RAGE_t1 --- mean 
        line['T<sub>1</sub>(mts)'] =  self.get_val(matrix['MTS'], 'mean')        # MTS_t1     --- mean 
        line['MTR'] = self.get_val(matrix['MTR'], 'mean')           # MTR   --- mean
        line['MTsat'] = self.get_val(matrix['MTsat'], 'mean')         # MTsat  --- mean

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

        # Calculate means 
        std_area = {
            'T<sub>1</sub>(mp2rage)': None,
            'T<sub>1</sub>(mts)': None,
            'MTR': None,
            'MTsat': None
        }

        std_area['T<sub>1</sub>(mp2rage)'] =  self.get_val(matrix['MP2RAGE'], 'std')   # MP2RAGE_t1      --- std 
        std_area['T<sub>1</sub>(mts)'] =  self.get_val(matrix['MTS'], 'std')       # MTS_t1          --- std 
        std_area['MTR'] = self.get_val(matrix['MTR'], 'std')          # N/A_mtr         --- std
        std_area['MTsat'] = self.get_val(matrix['MTsat'], 'std')        # MTS_mtsat       --- std

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
                x=x+x[::-1],
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
                                                                
                                                                {"yaxis": dict(range=[self.get_val(np.append(matrix['MP2RAGE'], matrix['MTS'], axis=0), 'min'), self.get_val(np.append(matrix['MP2RAGE'], matrix['MTS'], axis=0), 'max')],
                                                                                title='T<sub>1</sub> [s]',
                                                                                mirror=True,
                                                                                ticks='outside', 
                                                                                showline=True, 
                                                                                linecolor='#000',
                                                                                tickfont = dict(size=self.y_label_tick_font_size))}]),
                                                
                                                dict(label="MTR",
                                                            method="update",
                                                            args=[{"visible": [True] + [False]*12 + [True]*6 + [False]*6 + [False]*2 + [True]*1 +[False]*1 + [False]*2 + [True]*1 +[False]*1},
                                                                
                                                                {"yaxis": dict(range=[self.get_val(matrix['MTR'], 'min'), self.get_val(matrix['MTR'], 'max')],
                                                                                title='MTR [a.u.]',
                                                                                mirror=True,
                                                                                ticks='outside', 
                                                                                showline=True, 
                                                                                linecolor='#000',
                                                                                tickfont = dict(size=self.y_label_tick_font_size))}]),
                                                
                                                dict(label="MTsat",
                                                            method="update",
                                                            args=[{"visible":  [True] + [False]*18 + [True]*6 + [False]*3 + [True]*1 + [False]*3 + [True]*1},
                                                                
                                                                {"yaxis": dict(range=[self.get_val(matrix['MTsat'], 'min'), self.get_val(matrix['MTsat'], 'max')],
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
                        yaxis=dict(range=[self.get_val(np.append(matrix['MP2RAGE'], matrix['MTS'], axis=0), 'min'), self.get_val(np.append(matrix['MP2RAGE'], matrix['MTS'], axis=0), 'max')], 
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
