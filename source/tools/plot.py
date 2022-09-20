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
    """Plot handling class

    Class objects load Data object and display Plotly figure with it.

    """

    colours = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
               (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
               (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
               (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
               (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]

    def __init__(self, dataset, plot_name):
        """Initialize object
        
        Input: 
            - dataset (Data class object)
            - plot_name (ID for plot, HTML filename)

        """

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
        """Get values
        
        Get desired value (min, max, mean, std) from a 
        dataset matrix (metric valuesfor all subjects
        and sessions).

        Input: 
            - matrix (data extracted using Data object)
            - key (desired value in string: min, max, 
                   mean, or std)

        """

        temp = matrix[::]

        mean_list = []
        for ele in temp: 
            ele = [i for i in ele if i!=-100]
            mean_list.extend(ele)
            
        if key=='mean':
            val = float('{0:.7f}'.format(np.mean(mean_list)))
        if key=='std':
            val = float('{0:.7f}'.format(np.std(mean_list)))
        if key=='max':
            val = np.max(mean_list) + (np.max(mean_list)-np.min(mean_list))/4
        if key=='min':
            val = np.min(mean_list) - (np.max(mean_list)-np.min(mean_list))/4
            
        return val
    
    def get_symbols(self):
        """Get symbols
        
        Get specific plot markers.

        """

        # Get different symbols (See for reference: https://plotly.com/python/marker-style/)
        raw_symbols = SymbolValidator().values
        symbols = []
        for i in range(0,len(raw_symbols),3):
            symbols.append(raw_symbols[i])
        
        return symbols


    def display(self, env, fig_id = None):

        """Display figure
        
        Display Plotly figure using Data object.

        Input: 
            - env (display environment: jupyter-book or notebook)

        """
        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={'showLink': False, 'displayModeBar': False}

        # Get number of subjects and sessions
        num_subjects = self.dataset.num_subjects
        num_sessions = self.dataset.num_sessions

        # Get database
        if self.dataset.data_type == 'brain':
            matrix = {
                'WM': [],
                'GM': []
            }
            matrix['WM'] = self.dataset.extract_data('WM')
            matrix['GM'] = self.dataset.extract_data('GM')
        elif self.dataset.data_type == 'brain-diffusion':
            matrix = {
                'CC_1': [],
                'MCP': []
            }
            matrix['CC_1'] = self.dataset.extract_data('CC_1')
            matrix['MCP'] = self.dataset.extract_data('MCP')
        else:
            matrix = self.dataset.extract_data()

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
        elif self.dataset.data_type == 'brain-diffusion':
            trace_name = {
                    'DWI_FA': 'DWI_FA',
                    'DWI_MD': 'DWI_MD',
                    'DWI_RD': 'DWI_RD'
            }
        elif self.dataset.data_type == 'spine':
            trace_name = {
                'Area': 'Area (mm<sup>2</sup>)',
            }
        elif self.dataset.data_type == 'qmri':
            tissue = 'WM'
            trace_name = {
                    'DWI_FA': 'DWI_FA',
                    'DWI_MD': 'DWI_MD',
                    'DWI_RD': 'DWI_RD',
                    'MTR': 'MTR',
                    'MTSat': 'MTsat',
                    'T1': 'T<sub>1</sub>'
            }


        if self.dataset.data_type == 'brain':
            tissues = ['WM', 'GM']
            for tissue in tissues:
                # Add datapoints to plot
                figb = self.add_points(figb, matrix[tissue], trace_name, num_sessions, tissue)

                # Add mean line to plot
                figb, line = self.add_lines(figb, matrix[tissue], trace_name, tissue)

                # Add std shaded area to plot
                figb, std_area = self.add_std_area(figb, matrix[tissue], trace_name, line, tissue)
        elif self.dataset.data_type == 'brain-diffusion':
            tissues = ['CC_1', 'MCP']
            for tissue in tissues:
                # Add datapoints to plot
                figb = self.add_points(figb, matrix[tissue], trace_name, num_sessions, tissue)

                # Add mean line to plot
                figb, line = self.add_lines(figb, matrix[tissue], trace_name, tissue)

                # Add std shaded area to plot
                figb, std_area = self.add_std_area(figb, matrix[tissue], trace_name, line, tissue)
        elif self.dataset.data_type == 'spine':
            if fig_id == 'spine-csa-wm':
                tissues = ['WM']
            elif fig_id == 'spine-csa-gm':
                tissues = ['GM']
            else:
                tissues = ['WM', 'GM']

            for tissue in tissues:
                # Add datapoints to plot
                figb = self.add_points(figb, matrix, trace_name, num_sessions, tissue, fig_id)

                # Add mean line to plot
                figb, line = self.add_lines(figb, matrix, trace_name, tissue, fig_id)

                # Add std shaded area to plot
                figb, std_area = self.add_std_area(figb, matrix, trace_name, line, tissue, fig_id)
        else:
            # Add datapoints to plot
            figb = self.add_points(figb, matrix, trace_name, num_sessions, tissue, fig_id)

            # Add mean line to plot
            figb, line = self.add_lines(figb, matrix, trace_name, tissue, fig_id)

            # Add std shaded area to plot
            figb, std_area = self.add_std_area(figb, matrix, trace_name, line, tissue, fig_id)   

        # Set layout
        if self.dataset.data_type == 'brain':
            buttons = list([
                            dict(label="T<sub>1</sub> (MP2RAGE)",
                                method="update",
                                args=[{"visible": [True] + [True]*num_subjects + [False]*(num_subjects*3) + [True] + [False]*3 + [True] + [False]*3 + [True]*num_subjects + [False]*(num_subjects*3) + [True] + [False]*3 + [True] + [False]*3},
                                self.set_trace_layout(matrix=matrix, metric='MP2RAGE', title='T<sub>1</sub> [s]', tissues=['WM', 'GM'])]),
                            dict(label="T<sub>1</sub> (MTsat)",
                                method="update",
                                args=[{"visible": [True] + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects*2) + [False] + [True]*1 +[False]*2 + [False] + [True]*1 +[False]*2 + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects*2) + [False] + [True]*1 +[False]*2 + [False] + [True]*1 +[False]*2},
                                self.set_trace_layout(matrix=matrix, metric='MTS', title='T<sub>1</sub> [s]', tissues=['WM', 'GM'])]),                                                    
                            dict(label="MTR",
                                method="update",
                                args=[{"visible": [True] + [False]*(num_subjects*2) + [True]*num_subjects + [False]*num_subjects + [False]*2 + [True]*1 +[False]*1 + [False]*2 + [True]*1 +[False]*1 + [False]*(num_subjects*2) + [True]*num_subjects + [False]*num_subjects + [False]*2 + [True]*1 +[False]*1 + [False]*2 + [True]*1 +[False]*1},
                                self.set_trace_layout(matrix=matrix, metric='MTR', title='MTR [a.u.]', tissues=['WM', 'GM'])        ]),
                            dict(label="MTsat",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*3) + [True]*num_subjects + [False]*3 + [True]*1 + [False]*3 + [True]*1  + [False]*(num_subjects*3) + [True]*num_subjects + [False]*3 + [True]*1 + [False]*3 + [True]*1},
                                self.set_trace_layout(matrix=matrix, metric='MTsat', title='MTsat [a.u.]', tissues=['WM', 'GM'])])
                            ])
            annotations=[dict(text="Display metric: ", 
                              showarrow=False,
                              x=1.25,
                              y=0.62,
                              xref = 'paper',
                              yref="paper")]
        elif self.dataset.data_type == 'brain-diffusion':
            buttons = list([
                            dict(label="DWI_FA",
                                method="update",
                                args=[{"visible": [True] + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2 + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2},
                                self.set_trace_layout(matrix=matrix, metric='DWI_FA', title='DWI_FA [a.u.]', tissues=['CC_1', 'MCP'])]),
                            dict(label="DWI_MD",
                                method="update",
                                args=[{"visible": [True] + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects) + [False]*1 + [True]*1 +[False]*1 + [False]*1 + [True]*1 +[False]*1 + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects) + [False]*1 + [True]*1 +[False]*1 + [False]*1 + [True]*1 +[False]*1},
                                self.set_trace_layout(matrix=matrix, metric='DWI_MD', title='DWI_MD [mm<sup>2</sup>/s]', tissues=['CC_1', 'MCP'])]),            
                            dict(label="DWI_RD",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*2) + [True]*num_subjects + [False]*2 + [True]*1 + [False]*2 + [True]*1 + [False]*(num_subjects*2) + [True]*num_subjects + [False]*2 + [True]*1 + [False]*2 + [True]*1},
                                self.set_trace_layout(matrix=matrix, metric='DWI_RD', title='DWI_RD [mm<sup>2</sup>/s]', tissues=['CC_1', 'MCP'])]),
                            ])
            annotations=[dict(text="Display metric: ", 
                              showarrow=False,
                              x=1.25,
                              y=0.62,
                              xref = 'paper',
                              yref="paper")]
        elif self.dataset.data_type == 'spine':
            if fig_id == 'spine-csa-wm':
                buttons = list([
                                dict(label="T1w",
                                    method="update",
                                    args=[{"visible": [True] + ([True] + [False])*num_subjects + ([True] + [False])*2},
                                        self.set_trace_layout(matrix=matrix, metric='T1w', title='Area [mm<sup>2</sup>]')]),
                                dict(label="T2w",
                                    method="update",
                                    args=[{"visible": [True] + ([False] + [True])*num_subjects + ([False] + [True])*2},
                                        self.set_trace_layout(matrix=matrix, metric='T2w', title='Area [mm<sup>2</sup>]')]) 
                                ])
                annotations=[dict(text="Display metric: ", 
                                showarrow=False,
                                x=1.20,
                                y=0.62,
                                xref = 'paper',
                                yref="paper")]
            elif fig_id == 'spine-csa-gm':
                buttons = None
                annotations= None
            else:
                buttons = list([
                                dict(label="White matter",
                                    method="update",
                                    args=[{"visible": [True] + [True]*(num_subjects*2) + [True]*2 + [True]*2 + [False]*num_subjects + [False]*1 + [False]*1},
                                        self.set_trace_layout(matrix=matrix, metric='T1w', title='Area [mm<sup>2</sup>]')]),
                                dict(label="Grey matter",
                                    method="update",
                                    args=[{"visible": [True] + [False]*(num_subjects*2) + [False]*2 + [False]*2 + [True]*num_subjects + [True]*1 + [True]*1},
                                        self.set_trace_layout(matrix=matrix, metric='GMT2w', title='Area [mm<sup>2</sup>]')]) 
                                ])
                annotations=[dict(text="Display metric: ", 
                                showarrow=False,
                                x=1.25,
                                y=0.62,
                                xref = 'paper',
                                yref="paper")]

        elif self.dataset.data_type == 'qmri':
            buttons = list([
                            dict(label="DWI_FA",
                                method="update",
                                args=[{"visible": [True] + [True]*num_subjects + [False]*(num_subjects*5) + [True]*1 + [False]*5 + [True]*1 + [False]*5},
                                self.set_trace_layout(matrix=matrix, metric='DWI_FA', title='DWI_FA [a.u.]')]),
                            dict(label="DWI_MD",
                                method="update",
                                args=[{"visible": [True] + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects*4) + [False]*1 + [True]*1 +[False]*4 + [False]*1 + [True]*1 +[False]*4},
                                self.set_trace_layout(matrix=matrix, metric='DWI_MD', title='DWI_MD [mm<sup>2</sup>/s]')]),            
                            dict(label="DWI_RD",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*2) + [True]*num_subjects + [False]*(num_subjects*3) + [False]*2 + [True]*1 +[False]*3 + [False]*2 + [True]*1 +[False]*3},
                                self.set_trace_layout(matrix=matrix, metric='DWI_RD', title='DWI_RD [mm<sup>2</sup>/s]')]),
                            dict(label="MTR",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*3) + [True]*num_subjects + [False]*(num_subjects*2) + [False]*3 + [True]*1 +[False]*2 + [False]*3 + [True]*1 +[False]*2},
                                self.set_trace_layout(matrix=matrix, metric='MTR', title='MTR [a.u.]')]),
                            dict(label="MTsat",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*4) + [True]*num_subjects + [False]*num_subjects + [False]*4 + [True]*1 +[False]*1 + [False]*4 + [True]*1 +[False]*1},
                                self.set_trace_layout(matrix=matrix, metric='MTSat', title='MTsat [a.u.]')]),
                            dict(label="T<sub>1</sub>",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*5) + [True]*num_subjects + [False]*5 + [True]*1 + [False]*5 + [True]*1 },
                                self.set_trace_layout(matrix=matrix, metric='T1', title='T<sub>1</sub> [s]')]) 
                            ])
            annotations=[dict(text="Display metric: ", 
                              showarrow=False,
                              x=1.25,
                              y=0.62,
                              xref = 'paper',
                              yref="paper")]

        x_button=1.23
        y_button=0.58
        width = 760
        height = 520
    
        if self.dataset.data_type == 'brain':
            yaxis_range = [self.get_val(np.append(matrix['WM']['MP2RAGE'], matrix['GM']['MP2RAGE'], axis=0), 'min'), self.get_val(np.append(matrix['WM']['MP2RAGE'], matrix['GM']['MP2RAGE'], axis=0), 'max')]
            yaxis_title = 'T<sub>1</sub> [s]'
            x_button=1.3
        if self.dataset.data_type == 'brain-diffusion':
            yaxis_range = [self.get_val(np.append(matrix['CC_1']['DWI_FA'], matrix['MCP']['DWI_FA'], axis=0), 'min'), self.get_val(np.append(matrix['CC_1']['DWI_FA'], matrix['MCP']['DWI_FA'], axis=0), 'max')]
            yaxis_title = 'DWI_FA [a.u.]'
            x_button=1.3
        elif self.dataset.data_type == 'spine':
            x_button=1.28
            if fig_id == 'spine-csa-wm':
                yaxis_range = [self.get_val(matrix['T1w'], 'min'), self.get_val(matrix['T1w'], 'max')]
                x_button = 1.18
            elif fig_id == 'spine-csa-gm':
                yaxis_range = [self.get_val(matrix['GMT2w'], 'min'), self.get_val(matrix['GMT2w'], 'max')]
                width = 680
            else:
                yaxis_range = [self.get_val(np.append(matrix['T1w'], matrix['T2w'], axis=0), 'min'), self.get_val(np.append(matrix['T1w'], matrix['T2w'], axis=0), 'max')]
            
            yaxis_title = 'Area [mm<sup>2</sup>]'
        else:
            yaxis_range = [self.get_val(matrix['DWI_FA'], 'min'), self.get_val(matrix['DWI_FA'], 'max')]
            yaxis_title = 'DWI_FA [a.u.]'

        figb.update_layout(title = self.title,
                        updatemenus=[
                                        dict(
                                            active = 0, 
                                            x=x_button,
                                            y=y_button,
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
                        yaxis_title=yaxis_title,
                        yaxis=dict(range=yaxis_range, 
                                    mirror=True,
                                    ticks='outside', 
                                    showline=True, 
                                    linecolor='#000',
                                    tickfont = dict(size=self.y_label_tick_font_size)),
                        annotations=annotations,
                        plot_bgcolor='rgba(227,233,244, 0.5)',
                        width = width, 
                        height = height,
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

    def add_points(self, figb, matrix, trace_name, num_sessions, tissue=None, fig_id=None):
        """Add points to trace
        
        Internal function, adds datapoints to Plotly trace.

        Input: 
            - figb: Plotly figure
            - matrix: Data extracted using Data object
            - trace_name: Dictionary
            - tissue: 'WM' or 'GM', used for brain dataset

        """
        symbols = self.get_symbols()

        for metric in trace_name:
            if 'T1w' not in matrix:
                for trace in range(0, len(matrix[metric])):
                    t = [trace -0.3 + i*((0.3*2)/(num_sessions-1)) for i in range(0, num_sessions)]

                    if trace == 0: 
                        showlegend = True
                    else:
                        if metric == 'GMT2w':
                            showlegend = True
                        else:
                            showlegend = False

                    if fig_id == 'spine-qmri-wm':
                        showlegend = False

                    # Custom settings for just the T1 group/plot
                    if metric == 'MP2RAGE':
                        hover_mean = "Mean : <i> %{y: .2f} </i> sec"
                        visible=True
                    elif metric == 'Area':
                        hover_mean = "Mean : <i> %{y: .2f} </i> mm<sup>2</sup>"
                        visible=True
                    elif metric == 'DWI_FA':
                        hover_mean = "<i> %{y: .2f} </i>"
                        visible=True
                    else:
                        hover_mean = "Mean : <i> %{y: .2f} </i>" 
                        visible=False


                    marker_color = "rgb"+str(Plot.colours[0])
                    legend_group = "group1"

                    # Custom settings for just MTS
                    if tissue == 'WM':
                        marker_color = "rgb"+str(Plot.colours[0])
                        legend_group = "group1"
                        name = 'White matter'
                    elif tissue == 'GM':
                        marker_color = "rgb"+str(Plot.colours[3])
                        legend_group = "group2"
                        name = 'Grey matter'
                    elif tissue == 'CC_1':
                        marker_color = "rgb"+str(Plot.colours[0])
                        legend_group = "group1"
                        name = 'CC_1'
                    elif tissue == 'MCP':
                        marker_color = "rgb"+str(Plot.colours[3])
                        legend_group = "group2"
                        name = 'MCP'
                    else:
                        marker_color = "rgb"+str(Plot.colours[0])
                        legend_group = "group1"
                        name = trace_name[metric]

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
                                                text = ['Session {}'.format(i + 1) for i in range(num_sessions)],
                                                name= name,
                                                marker_color=marker_color))
            else:
                if tissue=='WM':
                    prop = 'T1w'
                elif tissue=='GM':
                    prop = 'GMT2w'

                for trace in range(0, len(matrix[prop])):
                    t = [trace -0.2 + i*((0.3*2)/(num_sessions-1)) for i in range(0, num_sessions)]
                        
                    if trace == 0: 
                        showlegend = True
                    else:
                        showlegend = False

                    # Custom settings for just the T1 group/plot
                    hover_mean = "Mean : <i> %{y: .2f} </i> mm<sup>2</sup>"
                    visible=True

                    if tissue=='WM':
                        if fig_id == 'spine-csa-wm':
                            showlegend = False
                        figb.add_trace(go.Scatter(x=t, 
                                                    y=matrix['T1w'][trace], 
                                                    mode='markers',
                                                    visible=visible,
                                                    legendgroup="group1",
                                                    hovertemplate = 
                                                    hover_mean + 
                                                    "<br>" + 
                                                    "<b>%{text}</b>", 
                                                    showlegend = showlegend, 
                                                    text = ['Session {}'.format(i + 1) for i in range(num_sessions)],
                                                    name= 'T<sub>1</sub>w',
                                                    marker_color="rgb"+str(Plot.colours[0])))

                        marker_color="rgb"+str(Plot.colours[3])
                        marker_symbol=symbols[5]
                        if fig_id == 'spine-csa-wm':
                            visible = False
                            marker_color="rgb"+str(Plot.colours[0])
                            marker_symbol = 'circle'

                        figb.add_trace(go.Scatter(x=t, 
                                                    y=matrix['T2w'][trace], 
                                                    mode='markers',
                                                    visible=visible,
                                                    legendgroup="group2",
                                                    hovertemplate = 
                                                    hover_mean + 
                                                    "<br>" + 
                                                    "<b>%{text}</b>", 
                                                    showlegend = showlegend, 
                                                    text = ['Session {}'.format(i + 1) for i in range(num_sessions)],
                                                    name= 'T<sub>2</sub>w',
                                                    marker_symbol=marker_symbol,
                                                    marker_color=marker_color))
                    elif tissue=='GM':
                        if fig_id == 'spine-csa-gm':
                            visible = True
                            showlegend = False
                        else:
                            visible = False
                        figb.add_trace(go.Scatter(x=t, 
                                                    y=matrix['GMT2w'][trace], 
                                                    mode='markers',
                                                    visible=visible,
                                                    legendgroup="group1",
                                                    hovertemplate = 
                                                    hover_mean + 
                                                    "<br>" + 
                                                    "<b>%{text}</b>", 
                                                    showlegend = showlegend, 
                                                    text = ['Session {}'.format(i + 1) for i in range(num_sessions)],
                                                    name= 'T<sub>2</sub><sup>*</sup>',
                                                    marker_color="rgb"+str(Plot.colours[0])))
                                       
        return figb

    def add_lines(self, figb, matrix, trace_name, tissue=None, fig_id=None):
        """Add lines (mean) to trace
        
        Internal function, adds lines to Plotly trace.

        Input: 
            - figb: Plotly figure
            - matrix: Data extracted using Data object
            - trace_name: Dictionary
            - tissue: 'WM' or 'GM', used for brain dataset

        """

        num_subjects = self.dataset.num_subjects

        x = list(np.linspace(-1, num_subjects, num=num_subjects+2, dtype=int))

        line = {}
        
        if 'T1w' not in matrix:
            for metric in trace_name:

                line[metric]= self.get_val(matrix[metric], 'mean')
                
                if tissue == 'WM':
                    line_color = "rgb"+str(Plot.colours[0])
                    name = 'White matter'
                elif tissue == 'GM': 
                    line_color = "rgb"+str(Plot.colours[3])
                    name = 'Grey matter'
                if tissue == 'CC_1':
                    line_color = "rgb"+str(Plot.colours[0])
                    name = 'CC_1'
                elif tissue == 'MCP': 
                    line_color = "rgb"+str(Plot.colours[3])
                    name = 'MCP'
                else: 
                    line_color = "rgb"+str(Plot.colours[0])
                    name = trace_name[metric]

                if metric == 'MP2RAGE' or metric == 'DWI_FA':
                    visible=True
                else:
                    visible=False

                # Add dotted line
                figb.add_trace(go.Scatter(x=x, 
                                        y=[line[metric]]*8,
                                        mode='lines',
                                        visible=visible,
                                        name=name,
                                        showlegend = False,
                                        opacity=0.5, 
                                        line=dict(color=line_color, 
                                                    width=2,
                                                    dash='dot')))
        else:
            if tissue=='WM':
                line = {
                    'T1w':{},
                    'T2w': {}
                    }
            elif tissue=='GM':
                line = {
                    'GMT2w':{}
                }

            for metric in trace_name:
                    
                if tissue=='WM':
                    line['T1w']= self.get_val(matrix['T1w'], 'mean')
                    line['T2w']= self.get_val(matrix['T2w'], 'mean')
                elif tissue=='GM':
                    line['GMT2w']= self.get_val(matrix['GMT2w'], 'mean')

                visible=True

                # Add dotted line
                if tissue=='WM':
                    figb.add_trace(go.Scatter(x=x, 
                                                y=[line['T1w']]*8,
                                                mode='lines',
                                                visible=visible,
                                                name='T<sub>1</sub>w',
                                                showlegend = False,
                                                opacity=0.5, 
                                                line=dict(color="rgb(31, 119, 180)", 
                                                            width=2,
                                                            dash='dot')))
                    
                    line_dict=dict(color="rgb(255, 187, 120)", width=2, dash='dot')
                    if fig_id == 'spine-csa-wm':
                        visible = False
                        line_dict=dict(color="rgb(31, 119, 180)", width=2,dash='dot')
                    
                    figb.add_trace(go.Scatter(x=x, 
                                                y=[line['T2w']]*8,
                                                mode='lines',
                                                visible=visible,
                                                name='T<sub>2</sub>w',
                                                showlegend = False,
                                                opacity=0.5, 
                                                line=line_dict))
                if tissue=='GM':
                    figb.add_trace(go.Scatter(x=x, 
                                                y=[line['GMT2w']]*8,
                                                mode='lines',
                                                visible=visible,
                                                name='T<sub>2</sub><sup>*</sup>',
                                                showlegend = False,
                                                opacity=0.5, 
                                                line=dict(color="rgb(31, 119, 180)", 
                                                            width=2,
                                                            dash='dot')))


        return figb, line

    def add_std_area(self, figb, matrix, trace_name, line, tissue=None, fig_id=None):
        """Add STD shaded area to trace
        
        Internal function, adds STD shaded area to Plotly trace.

        Input: 
            - figb: Plotly figure
            - matrix: Data extracted using Data object
            - trace_name: Dictionary
            - line: output from add_line, mean of dataset.
            - tissue: 'WM' or 'GM', used for brain dataset

        """
        
        num_subjects = self.dataset.num_subjects
        x = list(np.linspace(-1, num_subjects, num=num_subjects+2, dtype=int))

        std_area = {}
        if 'T1w' not in matrix:
            for metric in trace_name:
                std_area[metric] = self.get_val(matrix[metric], 'std') 

                if tissue == 'WM' or tissue == 'CC_1':
                    fillcolor='rgba(31, 119, 180, 0.15)'
                else: 
                    fillcolor='rgba(255, 187, 120, 0.15)'

                if metric == 'MP2RAGE' or metric == 'DWI_FA':
                    visible=True
                else:
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
            if tissue=='WM':
                std_area = {
                    'T1w':{},
                    'T2w': {}
                    }
            elif tissue=='GM':
                std_area = {
                    'GMT2w':{}
                    }

            for metric in trace_name:

                if tissue=='WM':
                    std_area['T1w'] = self.get_val(matrix['T1w'], 'std') 
                    std_area['T2w'] = self.get_val(matrix['T2w'], 'std') 
                if tissue=='GM':
                    std_area['GMT2w'] = self.get_val(matrix['GMT2w'], 'std') 

                visible=True
                if metric != 'Area':
                    visible=False

                 # Define name and color for STD region 
                name = metric + " STD"
                fillcolor = 'rgba(31, 119, 180,0.15)' 

                # Add STD
                if tissue=='WM':
                    figb.add_trace(go.Scatter(
                        x=x+x[::-1],
                        y=[line['T1w']+std_area['T1w']]*8+[line['T1w']-std_area['T1w']]*8,
                        fill='toself',
                        visible=visible,
                        fillcolor='rgba(31, 119, 180,0.15)',
                        line_color='rgba(255,255,255,0)',
                        showlegend=False,
                        hoverinfo=self.hoverinfo,
                        name='T<sub>1</sub>w STD'
                    ))

                    fillcolor='rgba(255, 187, 120,0.15)'
                    if fig_id == 'spine-csa-wm':
                        visible = False
                        fillcolor='rgba(31, 119, 180,0.15)'

                    figb.add_trace(go.Scatter(
                        x=x+x[::-1],
                        y=[line['T2w']+std_area['T2w']]*8+[line['T2w']-std_area['T2w']]*8,
                        fill='toself',
                        visible=visible,
                        fillcolor=fillcolor,
                        line_color='rgba(255,255,255,0)',
                        showlegend=False,
                        hoverinfo=self.hoverinfo,
                        name='T<sub>2</sub>w STD'
                    ))
                if tissue=='GM':
                    figb.add_trace(go.Scatter(
                        x=x+x[::-1],
                        y=[line['GMT2w']+std_area['GMT2w']]*8+[line['GMT2w']-std_area['GMT2w']]*8,
                        fill='toself',
                        visible=visible,
                        fillcolor='rgba(31, 119, 180,0.15)',
                        line_color='rgba(255,255,255,0)',
                        showlegend=False,
                        hoverinfo=self.hoverinfo,
                        name='T<sub>2</sub><sup>*</sup> STD'
                    ))

        return figb, std_area

    def set_trace_layout(self, matrix, metric, title, tissues=None):
        """Set trace layout
        
        Internal function, sets up y_axis layout details

        Input: 
            - figb: Plotly figure
            - matrix: Data extracted using Data object
            - metric: metric being ploted
            - title: y axis title
            - tissue: 'WM' or 'GM', used for brain dataset

        """
        if tissues is not None:
            yaxis_range = [self.get_val(np.append(matrix[tissues[0]][metric], matrix[tissues[1]][metric], axis=0), 'min'), self.get_val(np.append(matrix[tissues[0]][metric], matrix[tissues[1]][metric], axis=0), 'max')]
        else:
            yaxis_range = [self.get_val(matrix[metric], 'min'), self.get_val(matrix[metric], 'max')]
        return {"yaxis": dict(
                range = yaxis_range,
                title=title,
                mirror=True,
                ticks='outside', 
                showline=True, 
                linecolor='#000',
                tickfont = dict(size=self.y_label_tick_font_size)
                )
            }
