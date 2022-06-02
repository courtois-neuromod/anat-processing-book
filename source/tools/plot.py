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
        labels_subjects = ['Subject ' + str(i) for i in range(1,7)]
        labels_int = [i for i in range(1, 7)]

        # Add first values for labels [Sub1...Sub6]
        figb = go.Figure(data=go.Scatter(x=labels_int,
                                        y=[-1000 for i in range(1,len(labels_subjects)+1)],
                                        mode='markers',
                                        showlegend=False,
                                        marker_color='red'))

        # Add datapoints to plot
        if self.dataset.data_type == 'brain':
            trace_name = {
                'MP2RAGE': 'T<sub>1</sub> (mp2rage)',
                'MTS': 'T<sub>1</sub> (mts)',
                'MTR': 'MTR',
                'MTsat': 'MTsat'
            }
        elif self.dataset.data_type == 'spine':
            trace_name = {
                'Area': 'T<sub>1</sub> (mp2rage)',
                'AP': 'T<sub>1</sub> (mts)',
                'RL': 'MTR',
                'Angle': 'MTsat'
            }

        # Add datapoints to plot
        figb = self.add_points(figb, matrix, trace_name)

        # Add mean line to plot
        figb, line = self.add_lines(figb, matrix, trace_name)

        # Add std shaded area to plot
        figb, std_area = self.add_std_area(figb, matrix, trace_name, line)

        # Set layout
        if self.dataset.data_type == 'brain':
            buttons = list([
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
                                                tickfont = dict(size=self.y_label_tick_font_size))}]) ])
        elif self.dataset.data_type == 'spine':
            buttons = list([
                            dict(label="Mean (area)",
                                method="update",
                                args=[{"visible": [True] + [True]*12 + [False]*36 + [True]*2 + [False]*6 + [True]*2 + [False]*6},
                                                           
                                      {"yaxis": dict(range=[self.get_val(np.append(matrix['T1w']['Area'], matrix['T2w']['Area'], axis=0), 'min'), self.get_val(np.append(matrix['T1w']['Area'], matrix['T2w']['Area'], axis=0), 'max')],
                                                    title='Mean (area) [mm<sup>2</sup>]',
                                                    mirror=True,
                                                    ticks='outside', 
                                                    showline=True, 
                                                    linecolor='#000',
                                                    tickfont = dict(size=self.y_label_tick_font_size))}]),
                            dict(label="Mean (AP)",
                                method="update",
                                args=[{"visible": [True] + [False]*12 + [True]*12 + [False]*24 + [False]*2 + [True]*2 +[False]*4 + [False]*2 + [True]*2 +[False]*4},
                                                           
                                      {"yaxis": dict(range=[self.get_val(np.append(matrix['T1w']['AP'], matrix['T2w']['AP'], axis=0), 'min'), self.get_val(np.append(matrix['T1w']['AP'], matrix['T2w']['AP'], axis=0), 'max')],
                                                    title='Mean (AP) [mm]',
                                                    mirror=True,
                                                    ticks='outside', 
                                                    showline=True, 
                                                    linecolor='#000',
                                                    tickfont = dict(size=self.y_label_tick_font_size))}]),
                                    
                            dict(label="Mean (RL)",
                                method="update",
                                args=[{"visible": [True] + [False]*24 + [True]*12 + [False]*12 + [False]*4 + [True]*2 +[False]*2 + [False]*4 + [True]*2 +[False]*2},
                                                    
                                      {"yaxis": dict(range=[self.get_val(np.append(matrix['T1w']['RL'], matrix['T2w']['RL'], axis=0), 'min'), self.get_val(np.append(matrix['T1w']['RL'], matrix['T2w']['RL'], axis=0), 'max')],
                                                    title='Mean (RL) [mm]',
                                                    mirror=True,
                                                    ticks='outside', 
                                                    showline=True, 
                                                    linecolor='#000',
                                                    tickfont = dict(size=self.y_label_tick_font_size))}]),
                                        
                            dict(label="Mean (angle)",
                                method="update",
                                args=[{"visible":  [True] + [False]*36 + [True]*12 + [False]*6 + [True]*2 + [False]*6 + [True]*2 },
                                                           
                                      {"yaxis": dict(range=[self.get_val(np.append(matrix['T1w']['Angle'], matrix['T2w']['Angle'], axis=0), 'min'), self.get_val(np.append(matrix['T1w']['Angle'], matrix['T2w']['Angle'], axis=0), 'max')],
                                                    title='Mean (angle) [°]',
                                                    mirror=True,
                                                    ticks='outside', 
                                                    showline=True, 
                                                    linecolor='#000',
                                                    tickfont = dict(size=self.y_label_tick_font_size))}]) ])
                                        
        if self.dataset.data_type == 'brain':
            yaxis_range = [self.get_val(np.append(matrix['MP2RAGE'], matrix['MTS'], axis=0), 'min'), self.get_val(np.append(matrix['MP2RAGE'], matrix['MTS'], axis=0), 'max')]
        elif self.dataset.data_type == 'spine':
            yaxis_range = [self.get_val(np.append(matrix['T1w']['Area'], matrix['T2w']['Area'], axis=0), 'min'), self.get_val(np.append(matrix['T1w']['Area'], matrix['T2w']['Area'], axis=0), 'max')]

        figb.update_layout(title = self.title,
                        updatemenus=[
                                        dict(
                                            active = 0, 
                                            x=1.23,
                                            y=0.58,
                                            direction="down",
                                            yanchor="top",
                                            buttons=buttons)],
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
                        yaxis=dict(range=yaxis_range, 
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
        
        # Plot figuregit 
        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(figb, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(figb,config=config)

    def add_points(self, figb, matrix, trace_name):
        symbols = self.get_symbols()

        for metric in trace_name:
            if 'T1w' not in matrix:

                for trace in range(0, len(matrix[metric])):
                    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
                    
                    if trace == 0: 
                        showlegend = True
                    else:
                        showlegend = False

                    # Custom settings for just the T1 group/plot
                    if metric == 'MP2RAGE' or metric == 'MTS':
                        hover_mean = "Mean : <i> %{y: .2f} </i> sec"
                        visible=True
                    elif metric == 'Area':
                        hover_mean = "Mean : <i> %{y: .2f} </i> mm<sup>2</sup>"
                        visible=True
                    elif metric == 'AP' or metric == 'RL' or metric == 'Angle':
                        hover_mean = "Mean : <i> %{y: .2f} </i> mm"
                        visible=False
                    else:
                        hover_mean = "Mean : <i> %{y: .2f} </i>" 
                        visible=False

                    # Custom settings for just MTS
                    if metric == 'MTS':
                        marker_color = "rgb"+str(Plot.colours[3])
                        legend_group = "group2"
                    else:
                        marker_color = "rgb"+str(Plot.colours[0])
                        legend_group = "group1"

                    figb.add_trace(go.Scatter(x=t, 
                                                y=matrix[metric][trace], 
                                                mode='markers',
                                                visible=visible,
                                                legendgroup=legend_group,
                                                hovertemplate = 
                                                hover_mean + 
                                                "<br>" + 
                                                "<b>%{text}</b>", 
                                                showlegend = showlegend, 
                                                text = ['Session {}'.format(i + 1) for i in range(4)],
                                                name= trace_name[metric],
                                                marker_color=marker_color))
            else:
                for trace in range(0, len(matrix['T1w'][metric])):
                    t = [trace -0.2 + i*0.14 for i in range(0, 4)]
                        
                    if trace == 0: 
                        showlegend = True
                    else:
                        showlegend = False

                    # Custom settings for just the T1 group/plot
                    if metric == 'Area':
                        hover_mean = "Mean : <i> %{y: .2f} </i> mm<sup>2</sup>"
                        visible=True
                    elif metric == 'AP' or metric == 'RL' or metric == 'Angle':
                        hover_mean = "Mean : <i> %{y: .2f} </i> mm"
                        visible=False

                    figb.add_trace(go.Scatter(x=t, 
                                                y=matrix['T1w'][metric][trace], 
                                                mode='markers',
                                                visible=visible,
                                                legendgroup="group1",
                                                hovertemplate = 
                                                hover_mean + 
                                                "<br>" + 
                                                "<b>%{text}</b>", 
                                                showlegend = showlegend, 
                                                text = ['Session {}'.format(i + 1) for i in range(4)],
                                                name= 'T<sub>1</sub>w',
                                                marker_color="rgb"+str(Plot.colours[0])))

                    figb.add_trace(go.Scatter(x=t, 
                                                y=matrix['T2w'][metric][trace], 
                                                mode='markers',
                                                visible=visible,
                                                legendgroup="group2",
                                                hovertemplate = 
                                                hover_mean + 
                                                "<br>" + 
                                                "<b>%{text}</b>", 
                                                showlegend = showlegend, 
                                                text = ['Session {}'.format(i + 1) for i in range(4)],
                                                name= 'T<sub>2</sub>w',
                                                marker_symbol=symbols[5],
                                                marker_color="rgb"+str(Plot.colours[3])))


                                       
        return figb

    def add_lines(self, figb, matrix, trace_name):
        x = [-1, 0, 1, 2, 3, 4, 5, 6]
        line = {}
        
        if 'T1w' not in matrix:
            for metric in trace_name:
                line[metric]= self.get_val(matrix[metric], 'mean')

                if metric == 'MTS':
                    line_color = "rgb"+str(Plot.colours[3])
                else: 
                    line_color = "rgb"+str(Plot.colours[0])

                visible=True
                if metric == 'MTR' or metric == 'MTsat':
                    visible=False

                # Add dotted line
                figb.add_trace(go.Scatter(x=x, 
                                        y=[line[metric]]*8,
                                        mode='lines',
                                        visible=visible,
                                        name=trace_name[metric],
                                        opacity=0.5, 
                                        line=dict(color=line_color, 
                                                    width=2,
                                                    dash='dot')))
        else:
            line = {
                'T1w':{},
                'T2w': {}
                }
            for metric in trace_name:
                    
                line['T1w'][metric]= self.get_val(matrix['T1w'][metric], 'mean')
                line['T2w'][metric]= self.get_val(matrix['T2w'][metric], 'mean')

                visible=True
                if metric != 'Area':
                    visible=False

                # Add dotted line
                figb.add_trace(go.Scatter(x=x, 
                                            y=[line['T1w'][metric]]*8,
                                            mode='lines',
                                            visible=visible,
                                            name='T<sub>1</sub>w',
                                            opacity=0.5, 
                                            line=dict(color="rgb(31, 119, 180)", 
                                                        width=2,
                                                        dash='dot')))
    
                figb.add_trace(go.Scatter(x=x, 
                                            y=[line['T2w'][metric]]*8,
                                            mode='lines',
                                            visible=visible,
                                            name='T<sub>2</sub>w',
                                            opacity=0.5, 
                                            line=dict(color="rgb(255, 187, 120)", 
                                                        width=2,
                                                        dash='dot')))


        return figb, line

    def add_std_area(self, figb, matrix, trace_name, line):
        x = [-1, 0, 1, 2, 3, 4, 5, 6]
        std_area = {}
        
        if 'T1w' not in matrix:
            for metric in trace_name:
                std_area[metric] = self.get_val(matrix[metric], 'std') 

                if metric == 'MTS':
                    fillcolor='rgba(255, 187, 120, 0.15)'
                else: 
                    fillcolor='rgba(31, 119, 180, 0.15)'

                visible=True
                if metric == 'MTR' or metric == 'MTsat':
                    visible=False

                # Add STD
                figb.add_trace(go.Scatter(
                    x=x+x[::-1],
                    y=[line[metric]+std_area[metric]]*8+[line[metric]-std_area[metric]]*8,
                    fill='toself',
                    visible=visible,
                    fillcolor=fillcolor,
                    line_color='rgba(255,255,255,0)',
                    showlegend=False,
                    hoverinfo=self.hoverinfo,
                ))
        
        else:
            std_area = {
                'T1w':{},
                'T2w': {}
                }
            for metric in trace_name:
                    
                std_area['T1w'][metric] = self.get_val(matrix['T1w'][metric], 'std') 
                std_area['T2w'][metric] = self.get_val(matrix['T2w'][metric], 'std') 

                visible=True
                if metric != 'Area':
                    visible=False

                 # Define name and color for STD region 
                name = metric + " STD"
                fillcolor = 'rgba(31, 119, 180,0.15)' 

                # Add STD
                figb.add_trace(go.Scatter(
                    x=x+x[::-1],
                    y=[line['T1w'][metric]+std_area['T1w'][metric]]*8+[line['T1w'][metric]-std_area['T1w'][metric]]*8,
                    fill='toself',
                    visible=visible,
                    fillcolor='rgba(31, 119, 180,0.15)',
                    line_color='rgba(255,255,255,0)',
                    showlegend=False,
                    hoverinfo=self.hoverinfo,
                    name='T<sub>1</sub>w STD'
                ))

                figb.add_trace(go.Scatter(
                    x=x+x[::-1],
                    y=[line['T2w'][metric]+std_area['T2w'][metric]]*8+[line['T2w'][metric]-std_area['T2w'][metric]]*8,
                    fill='toself',
                    visible=visible,
                    fillcolor='rgba(255, 187, 120,0.15)',
                    line_color='rgba(255,255,255,0)',
                    showlegend=False,
                    hoverinfo=self.hoverinfo,
                    name='T<sub>2</sub>w STD'
                ))

        return figb, std_area