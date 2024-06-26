# Python imports 
from pathlib import Path
import plotly.graph_objects as go
import plotly.tools as tls
from plotly.offline import plot, iplot, init_notebook_mode
from plotly.validators.scatter.marker import SymbolValidator
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd
from tools.data import Data
from tools.stats import Stats

class Plot:
    """Plot handling class

    Class objects load Data object and display Plotly figure with it.

    """

    colours = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (190, 77, 80), (229, 153, 50), (0, 132, 53),
               (255, 187, 120), (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
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
        self.x_label_tick_font_size = 22
        self.y_label_tick_font_size = 22
        self.general_font_size = 22

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
        config={
            'showLink': False,
            'displayModeBar': True,
            'toImageButtonOptions': {
                'format': 'png', # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 500,
                'width': 700,
                'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

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
        elif self.dataset.data_type == 'brain-diffusion-cc':
            matrix = {
                'genu': [],
                'body': [],
                'splenium': []
            }
            matrix['genu'] = self.dataset.extract_data('genu')
            matrix['body'] = self.dataset.extract_data('body')
            matrix['splenium'] = self.dataset.extract_data('splenium')
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
        elif self.dataset.data_type == 'brain-diffusion' or self.dataset.data_type == 'brain-diffusion-cc':
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
        elif self.dataset.data_type == 'brain-diffusion-cc':
            tissues = ['genu', 'body', 'splenium']
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
                                self.set_trace_layout(matrix=matrix, metric='MTR', title='MTR [%]', tissues=['WM', 'GM'])        ]),
                            dict(label="MTsat",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*3) + [True]*num_subjects + [False]*3 + [True]*1 + [False]*3 + [True]*1  + [False]*(num_subjects*3) + [True]*num_subjects + [False]*3 + [True]*1 + [False]*3 + [True]*1},
                                self.set_trace_layout(matrix=matrix, metric='MTsat', title='MTsat [a.u.]', tissues=['WM', 'GM'])])
                            ])
            annotations=[dict(text="Display metric: ", 
                              showarrow=False,
                              x=1.38,
                              y=0.63,
                              xref = 'paper',
                              yref="paper",
                              font = dict(size = 16),)]
        elif self.dataset.data_type == 'brain-diffusion':
            buttons = list([
                            dict(label="DWI_FA",
                                method="update",
                                args=[{"visible": [True] + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2 + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2},
                                self.set_trace_layout(matrix=matrix, metric='DWI_FA', title='DWI_FA', tissues=['CC_1', 'MCP'])]),
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
                              yref="paper",
                              font = dict(size = 16),)]
        elif self.dataset.data_type == 'brain-diffusion-cc':
            buttons = list([
                            dict(label="DWI_FA",
                                method="update",
                                args=[{"visible": [True] + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2 + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2 + [True]*num_subjects + [False]*(num_subjects*2) + [True]*1 + [False]*2 + [True]*1 + [False]*2},
                                self.set_trace_layout(matrix=matrix, metric='DWI_FA', title='DWI_FA', tissues=['genu', 'body', 'splenium'])]),
                            dict(label="DWI_MD",
                                method="update",
                                args=[{"visible": [True] + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects) + [False]*1 + [True]*1 +[False]*1 + [False]*1 + [True]*1 +[False]*1 + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects) + [False]*1 + [True]*1 +[False]*1 + [False]*1 + [True]*1 +[False]*1 + [False]*num_subjects + [True]*num_subjects + [False]*(num_subjects) + [False]*1 + [True]*1 +[False]*1 + [False]*1 + [True]*1 +[False]*1,
                                       "tickformat":'m'},
                                self.set_trace_layout(matrix=matrix, metric='DWI_MD', title='DWI_MD [mm<sup>2</sup>/s]', tissues=['genu', 'body', 'splenium'])],),        
                            dict(label="DWI_RD",
                                method="update",
                                args=[{"visible":  [True] + [False]*(num_subjects*2) + [True]*num_subjects + [False]*2 + [True]*1 + [False]*2 + [True]*1 + [False]*(num_subjects*2) + [True]*num_subjects + [False]*2 + [True]*1 + [False]*2 + [True]*1 + [False]*(num_subjects*2) + [True]*num_subjects + [False]*2 + [True]*1 + [False]*2 + [True]*1},
                                self.set_trace_layout(matrix=matrix, metric='DWI_RD', title='DWI_RD [mm<sup>2</sup>/s]', tissues=['genu', 'body', 'splenium'])]),
                            ])
            annotations=[dict(text="Display metric: ", 
                              showarrow=False,
                              x=1.33,
                              y=0.55,
                              xref = 'paper',
                              yref="paper",
                              font = dict(size = 16),)]
        elif self.dataset.data_type == 'spine':
            if fig_id == 'spine-csa-wm':
                buttons = list([
                    dict(label="T1w",
                                    method="update",
                                    args=[{
                                        "visible": [True] + ([True] + [False])*num_subjects + ([True] + [False])*2},
                                        self.set_trace_layout(matrix=matrix, metric='T1w', title='Area [mm<sup>2</sup>]')]),
                                dict(label="T2w",
                                    method="update",
                                    args=[{"visible": [True] + ([False] + [True])*num_subjects + ([False] + [True])*2},
                                        self.set_trace_layout(matrix=matrix, metric='T2w', title='Area [mm<sup>2</sup>]')]) 
                                ])
                annotations=[dict(text="Display metric: ", 
                                showarrow=False,
                                x=1.33,
                                y=0.62,
                                xref = 'paper',
                                yref="paper",
                                font = dict(size = 16),)]
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
                                yref="paper",
                                font = dict(size = 16),)]

        elif self.dataset.data_type == 'qmri':
            buttons = list([
                            dict(label="DWI_FA",
                                method="update",
                                args=[{"visible": [True] + [True]*num_subjects + [False]*(num_subjects*5) + [True]*1 + [False]*5 + [True]*1 + [False]*5},
                                self.set_trace_layout(matrix=matrix, metric='DWI_FA', title='DWI_FA')]),
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
                                self.set_trace_layout(matrix=matrix, metric='MTR', title='MTR [%]')]),
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
                              x=1.32,
                              y=0.62,
                              xref = 'paper',
                              yref="paper",
                              font = dict(size = 16),)]

        x_button=1.23
        y_button=0.58
        width = 760
        height = 520
        left=50
        right=50
        bottom=60
        top=50
    
        if self.dataset.data_type == 'brain':
            yaxis_range = [self.get_val(np.append(matrix['WM']['MP2RAGE'], matrix['GM']['MP2RAGE'], axis=0), 'min'), self.get_val(np.append(matrix['WM']['MP2RAGE'], matrix['GM']['MP2RAGE'], axis=0), 'max')]
            yaxis_title = 'T<sub>1</sub> [s]'
            x_button=1.4
        elif self.dataset.data_type == 'brain-diffusion':
            yaxis_range = [self.get_val(np.append(matrix['CC_1']['DWI_FA'], matrix['MCP']['DWI_FA'], axis=0), 'min'), self.get_val(np.append(matrix['CC_1']['DWI_FA'], matrix['MCP']['DWI_FA'], axis=0), 'max')]
            yaxis_title = 'DWI_FA'
            x_button=1.3
        elif self.dataset.data_type == 'brain-diffusion-cc':
            yaxis_range = [self.get_val(np.append(matrix['genu']['DWI_FA'], matrix['splenium']['DWI_FA'], axis=0), 'min'), self.get_val(np.append(matrix['genu']['DWI_FA'], matrix['splenium']['DWI_FA'], axis=0), 'max')]
            yaxis_title = 'DWI_FA'
            x_button=1.3
            y_button=0.5
        elif self.dataset.data_type == 'spine':
            if fig_id == 'spine-csa-wm':
                yaxis_range = [self.get_val(matrix['T1w'], 'min'), self.get_val(matrix['T1w'], 'max')]
                x_button=1.25
                width = 680
                height = 540
                right=150
            elif fig_id == 'spine-csa-gm':
                yaxis_range = [self.get_val(matrix['GMT2w'], 'min'), self.get_val(matrix['GMT2w'], 'max')]
                width = 590
                height = 540
            
            yaxis_title = 'Area [mm<sup>2</sup>]'
        else:
            yaxis_range = [self.get_val(matrix['DWI_FA'], 'min'), self.get_val(matrix['DWI_FA'], 'max')]
            yaxis_title = 'DWI_FA'
            x_button=1.28
            width = 680
            height = 540
        
        if fig_id== 'spine-csa-wm' or fig_id=='spine-qmri-wm':
            direction="up"
        else:
            direction="down"

        figb.update_layout(title = self.title,
                        updatemenus=[
                                        dict(
                                            active = 0, 
                                            x=x_button,
                                            y=y_button,
                                            direction=direction,
                                            yanchor="top",
                                            buttons=buttons,
                                            font = dict(size = 16),
                                            )],
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
                                    tickfont = dict(size=self.x_label_tick_font_size),
                                    tickangle = 45
                                    ),
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
                        margin=go.layout.Margin(l=left,
                                                r=right,
                                                b=bottom,
                                                t=top))
        
        # Plot figuregit 
        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(figb, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(figb,config=config)

    def display_paper_fig2(self, env, fig_id = None):
        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={
            'showLink': False,
            'displayModeBar': True,
            'toImageButtonOptions': {
                'format': 'png', # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 900,
                'width': 900,
                'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        matrix = {
            'WM': [],
            'GM': []
        }
        matrix['WM'] = self.dataset.extract_data('WM')
        matrix['GM'] = self.dataset.extract_data('GM')

        # Get number of subjects and sessions
        num_subjects = self.dataset.num_subjects
        num_sessions = self.dataset.num_sessions    

        labels_subjects = ['Subject ' + str(i) for i in range(1,7)]
        labels_int = [i for i in range(1, 7)]

        trace_name = {
            'MP2RAGE': 'T<sub>1</sub> (mp2rage)',
            'MTS': 'T<sub>1</sub> (mts)',
            'MTR': 'MTR',
            'MTsat': 'MTsat'
        }

        fig = make_subplots(
            rows=2, cols=2,
            horizontal_spacing = 0.13, vertical_spacing = 0.2,
            subplot_titles=("T<sub>1</sub> (MP2RAGE)", "T<sub>1</sub> (MTsat)", "MTR", "MTsat"))

        tissues = ['WM', 'GM']
        for tissue in tissues:
            # Add datapoints to plot
            fig = self.add_points(fig, matrix[tissue], trace_name, num_sessions, tissue, fig_id='paper_fig2')

            # Add mean line to plot
            fig, line = self.add_lines(fig, matrix[tissue], trace_name, tissue, fig_id='paper_fig2')

            # Add std shaded area to plot
            fig, std_area = self.add_std_area(fig, matrix[tissue], trace_name, line, tissue, fig_id='paper_fig2')

        fig.update_xaxes(
            type="linear",
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            row=1, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'T<sub>1</sub> [s]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(np.append(matrix['WM']['MP2RAGE'], matrix['GM']['MP2RAGE'], axis=0), 'min'), self.get_val(np.append(matrix['WM']['MP2RAGE'], matrix['GM']['MP2RAGE'], axis=0), 'max')],
            row=1, col=1
            )

        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            row=1, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'T<sub>1</sub> [s]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(np.append(matrix['WM']['MTS'], matrix['GM']['MTS'], axis=0), 'min'), self.get_val(np.append(matrix['WM']['MTS'], matrix['GM']['MTS'], axis=0), 'max')],
            row=1, col=2
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            row=2, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'MTR [%]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(np.append(matrix['WM']['MTR'], matrix['GM']['MTR'], axis=0), 'min'), self.get_val(np.append(matrix['WM']['MTR'], matrix['GM']['MTR'], axis=0), 'max')],
            row=2, col=1
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            row=2, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'MTsat [a.u.]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(np.append(matrix['WM']['MTsat'], matrix['GM']['MTsat'], axis=0), 'min'), self.get_val(np.append(matrix['WM']['MTsat'], matrix['GM']['MTsat'], axis=0), 'max')],
            row=2, col=2
            )

        fig.update_layout(
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            legend_title="",
        )

        fig.update_layout(legend=dict(
            orientation = 'v',
            bordercolor="Gray",
            borderwidth=1,
            yanchor="top",
            y=0.85,
            xanchor="left",
            x=0.15,
            font = dict(size = self.general_font_size),
        ))

        fig.for_each_annotation(lambda a: a.update(
            text=f'<b>{a.text}</b>',
            font = dict(size = self.general_font_size),))
        
        ## WM stats
        stats_wm = Stats(self.dataset)
        stats_wm.build_df('WM')
        stats_wm.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0.63,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['T1 (MP2RAGE)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['T1 (MP2RAGE)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.99, y=0.63,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['T1 (MTsat)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['T1 (MTsat)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0.36,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['MTR']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['MTR']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.99, y=0.36,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['MTsat']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['MTsat']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        ## GM stats   
        stats_gm = Stats(self.dataset)
        stats_gm.build_df('GM')
        stats_gm.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0.98,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_gm.stats_table['T1 (MP2RAGE)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_gm.stats_table['T1 (MP2RAGE)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.99, y=0.98,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_gm.stats_table['T1 (MTsat)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_gm.stats_table['T1 (MTsat)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0.025,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_gm.stats_table['MTR']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_gm.stats_table['MTR']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.99, y=0.025,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_gm.stats_table['MTsat']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_gm.stats_table['MTsat']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )

        fig.update_layout(height=900, width=900)

        #fig.show()

        # Plot figuregit 
        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(fig, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(fig,config=config)

    def display_paper_fig3(self, env, fig_id = None):
        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={
            'showLink': False,
            'displayModeBar': True,
            'toImageButtonOptions': {
                'format': 'png', # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 300,
                'width': 900,
                'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        matrix = {
            'genu': [],
            'body': [],
            'splenium': []
        }
        matrix['genu'] = self.dataset.extract_data('genu')
        matrix['body'] = self.dataset.extract_data('body')
        matrix['splenium'] = self.dataset.extract_data('splenium')

        # Get number of subjects and sessions
        num_subjects = self.dataset.num_subjects
        num_sessions = self.dataset.num_sessions    

        labels_subjects = ['Subject ' + str(i) for i in range(1,7)]
        labels_int = [i for i in range(1, 7)]

        trace_name = {
                'DWI_FA': 'DWI_FA',
                'DWI_MD': 'DWI_MD',
                'DWI_RD': 'DWI_RD'
        }

        fig = make_subplots(
            rows=1, cols=3,
            horizontal_spacing = 0.14,
            subplot_titles=("Fractional Anisotropy (FA)", "Mean Diffusivity (MD)", "Radial Diffusivity (RD)"))
        
        tissues = ['genu', 'body', 'splenium']
        for tissue in tissues:
            # Add datapoints to plot
            fig = self.add_points(fig, matrix[tissue], trace_name, num_sessions, tissue, fig_id="paper_fig3")

            # Add mean line to plot
            fig, line = self.add_lines(fig, matrix[tissue], trace_name, tissue, fig_id="paper_fig3")

            # Add std shaded area to plot
            fig, std_area = self.add_std_area(fig, matrix[tissue], trace_name, line, tissue, fig_id="paper_fig3")

        fig.update_xaxes(
            type="linear",
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size-5),
            tickangle = 45,
            row=1, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'DWI_FA',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size-5),
            title_font = dict(size = self.general_font_size-5),
            range = [self.get_val(np.append(matrix['genu']['DWI_FA'], matrix['splenium']['DWI_FA'], axis=0), 'min'), self.get_val(np.append(matrix['genu']['DWI_FA'], matrix['splenium']['DWI_FA'], axis=0), 'max')],
            row=1, col=1
            )

        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size-5),
            tickangle = 45,
            row=1, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'DWI_MD [mm<sup>2</sup>/s]',
                'standoff':0
                },
            showgrid=False,
            range = [0.0006,0.00099],
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size-5),
            tickformat='s',
            title_font = dict(size = self.general_font_size-5),
            #range = [self.get_val(np.append(matrix['genu']['DWI_MD'], matrix['splenium']['DWI_MD'], axis=0), 'min'), self.get_val(np.append(matrix['genu']['DWI_MD'], matrix['splenium']['DWI_MD'], axis=0), 'max')],
            row=1, col=2
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size-5),
            tickangle = 45,
            row=1, col=3
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'DWI_RD [mm<sup>2</sup>/s]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size-5),
            title_font = dict(size = self.general_font_size-5),
            tickformat='s',
            range = [self.get_val(np.append(matrix['genu']['DWI_RD'], matrix['splenium']['DWI_RD'], axis=0), 'min'), self.get_val(np.append(matrix['genu']['DWI_RD'], matrix['splenium']['DWI_RD'], axis=0), 'max')],
            row=1, col=3
            )
        
        fig.update_layout(
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            legend_title="",
        )

        fig.update_layout(legend=dict(
            orientation = 'v',
            bordercolor="Gray",
            borderwidth=1,
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=1.01,
            font = dict(size = self.general_font_size-10),
        ))

        fig.for_each_annotation(lambda a: a.update(
            y=1.05,
            text=f'<b>{a.text}</b>',
            font = dict(size = self.general_font_size-5),))

        ## Splenium stats
        stats_splenium = Stats(self.dataset)
        stats_splenium.build_df('splenium')
        stats_splenium.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0.98,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_splenium.stats_table['FA (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_splenium.stats_table['FA (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[4])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.5, y=0.0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_splenium.stats_table['MD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_splenium.stats_table['MD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[4])),
            showarrow=False
            )

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.98, y=0.0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_splenium.stats_table['RD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_splenium.stats_table['RD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[4])),
            showarrow=False
            )
        
        ## Genu stats
        stats_genu = Stats(self.dataset)
        stats_genu.build_df('genu')
        stats_genu.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_genu.stats_table['FA (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_genu.stats_table['FA (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.5, y=1,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_genu.stats_table['MD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_genu.stats_table['MD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.98, y=1,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_genu.stats_table['RD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_genu.stats_table['RD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )

        ## Body stats
        stats_body = Stats(self.dataset)
        stats_body.build_df('body')
        stats_body.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.023, y=0.08,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_body.stats_table['FA (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_body.stats_table['FA (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.5, y=0.9,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_body.stats_table['MD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_body.stats_table['MD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.973, y=0.9,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_body.stats_table['RD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_body.stats_table['RD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-12,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )


        fig.update_layout(height=300, width=1000)

        # Plot figuregit 
        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(fig, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(fig,config=config)

    def display_paper_fig4(self, env, fig_id = None):
        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={
            'showLink': False,
            'displayModeBar': True,
            'toImageButtonOptions': {
                'format': 'png', # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 300,
                'width': 900,
                'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        matrix = self.dataset.extract_data()

        # Get number of subjects and sessions
        num_subjects = self.dataset.num_subjects
        num_sessions = self.dataset.num_sessions    

        labels_subjects = ['Subject ' + str(i) for i in range(1,7)]
        labels_int = [i for i in range(1, 7)]

        trace_name = {
            'Area': 'Area (mm<sup>2</sup>)',
        }

        fig = make_subplots(
            rows=1, cols=3,
            horizontal_spacing = 0.14,
            subplot_titles=("CSA (WM, T1w)", "CSA (WM, T2w)", "CSA (GM, T2*w)"))
        
        tissues = ['WM', 'GM']
        for tissue in tissues:
            # Add datapoints to plot
            fig = self.add_points(fig, matrix, trace_name, num_sessions, tissue, fig_id='paper_fig4')

            # Add mean line to plot
            fig, line = self.add_lines(fig, matrix, trace_name, tissue, fig_id='paper_fig4')

            # Add std shaded area to plot
            fig, std_area = self.add_std_area(fig, matrix, trace_name, line, tissue, fig_id='paper_fig4')

        fig.update_xaxes(
            type="linear",
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size-5),
            tickangle = 45,
            row=1, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'Area [mm<sup>2</sup>]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size-5),
            title_font = dict(size = self.general_font_size-5),
            autorange=False,
            range = [40, 100],
            row=1, col=1
            )

        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size-5),
            tickangle = 45,
            row=1, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'Area [mm<sup>2</sup>]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size-5),
            tickformat='s',
            title_font = dict(size = self.general_font_size-5),
            autorange=False,
            range = [40, 100],
            row=1, col=2
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size-5),
            tickangle = 45,
            row=1, col=3
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'Area [mm<sup>2</sup>]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size-5),
            title_font = dict(size = self.general_font_size-5),
            tickformat='s',
            range = [self.get_val(matrix['GMT2w'], 'min'), self.get_val(matrix['GMT2w'], 'max')],
            row=1, col=3
            )
        
        fig.update_layout(
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            legend_title="",
        )

        fig.update_layout(legend=dict(
            orientation = 'v',
            bordercolor="Gray",
            borderwidth=1,
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=1.01,
            font = dict(size = self.general_font_size-10),
        ))

        fig.for_each_annotation(lambda a: a.update(
            y=1.05,
            text=f'<b>{a.text}</b>',
            font = dict(size = self.general_font_size-5),))

        ## WM stats
        stats_wm = Stats(self.dataset)
        stats_wm.build_df()
        stats_wm.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0, y=0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['WM area (T1w)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['WM area (T1w)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-10,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0.5, y=0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['WM area (T2w)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['WM area (T2w)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-10,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=1.01, y=0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['GM area (T2s)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['GM area (T2s)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-10,
                color="rgb"+str(Plot.colours[3])),
            showarrow=False
            )

        fig.update_layout(height=300, width=1000)

        # Plot figureg
        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(fig, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(fig,config=config)

    def display_paper_fig5(self, env, fig_id = None):
        # Initialize Plotly 
        init_notebook_mode(connected = True)
        config={
            'showLink': False,
            'displayModeBar': True,
            'toImageButtonOptions': {
                'format': 'png', # one of png, svg, jpeg, webp
                'filename': 'custom_image',
                'height': 300,
                'width': 900,
                'scale': 2 # Multiply title/legend/axis/canvas sizes by this factor
            }
        }

        matrix = self.dataset.extract_data()

        # Get number of subjects and sessions
        num_subjects = self.dataset.num_subjects
        num_sessions = self.dataset.num_sessions    

        labels_subjects = ['Subject ' + str(i) for i in range(1,7)]
        labels_int = [i for i in range(1, 7)]

        tissue = 'WM'
        trace_name = {
                    'DWI_FA': 'DWI_FA',
                    'DWI_MD': 'DWI_MD',
                    'DWI_RD': 'DWI_RD',
                    'MTR': 'MTR',
                    'MTSat': 'MTsat',
                    'T1': 'T<sub>1</sub>'
            }        

        fig = make_subplots(
            rows=3, cols=2,
            horizontal_spacing = 0.2, vertical_spacing = 0.15,
            subplot_titles=("T<sub>1</sub> (MTsat)", "FA (DWI)", "MTR", "MD (DWI)", "MTsat", "RD (DWI)")
        )

        # Add datapoints to plot
        fig = self.add_points(fig, matrix, trace_name, num_sessions, tissue, fig_id='paper_fig5')

        # Add mean line to plot
        fig, line = self.add_lines(fig, matrix, trace_name, tissue, fig_id='paper_fig5')

        # Add std shaded area to plot
        fig, std_area = self.add_std_area(fig, matrix, trace_name, line, tissue, fig_id='paper_fig5')  

        fig.update_xaxes(
            type="linear",
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            tickangle = 45,
            row=1, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'T<sub>1</sub> [s]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(matrix['T1'], 'min'), self.get_val(matrix['T1'], 'max')],
            row=1, col=1
            )

        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            tickangle = 45,
            row=2, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'MTR [%]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(matrix['MTR'], 'min'), self.get_val(matrix['MTR'], 'max')],
            row=2, col=1
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            tickangle = 45,
            row=3, col=1
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'MTsat [a.u.]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(matrix['MTSat'], 'min'), self.get_val(matrix['MTSat'], 'max')],
            row=3, col=1
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            tickangle = 45,
            row=1, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'DWI_FA',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            range = [self.get_val(matrix['DWI_FA'], 'min'), self.get_val(matrix['DWI_FA'], 'max')],
            row=1, col=2
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            tickangle = 45,
            row=2, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'DWI_MD [mm<sup>2</sup>/s]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            tickformat='s',
            range = [self.get_val(matrix['DWI_MD'], 'min'), self.get_val(matrix['DWI_MD'], 'max')],
            row=2, col=2
            )
        fig.update_xaxes(
            type="linear",
            showgrid=False,
            linecolor='black',
            linewidth=2,
            range=[-0.45,5.45], 
            mirror=True,
            ticks='outside',
            showline=True,
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = labels_subjects,
            tickfont = dict(size=self.x_label_tick_font_size),
            tickangle = 45,
            row=3, col=2
            )
        fig.update_yaxes(
            type="linear",
            title={
                'text':'DWI_RD [mm<sup>2</sup>/s]',
                'standoff':0
                },
            showgrid=False,
            linecolor='black',
            linewidth=2,
            tickfont = dict(size=self.y_label_tick_font_size),
            title_font = dict(size = self.general_font_size),
            tickformat='s',
            range = [self.get_val(matrix['DWI_RD'], 'min'), self.get_val(matrix['DWI_RD'], 'max')],
            row=3, col=2
            )

        fig.update_layout(
            margin=dict(l=30, r=30, t=50, b=30),
            paper_bgcolor='rgb(255, 255, 255)',
            plot_bgcolor='rgb(255, 255, 255)',
            legend_title="",
        )

        fig.for_each_annotation(lambda a: a.update(
            text=f'<b>{a.text}</b>',
            font = dict(size = self.general_font_size),))
        
        ## WM stats
        stats_wm = Stats(self.dataset)
        stats_wm.build_df()
        stats_wm.build_stats_table()

        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0, y=0.79,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['T1 (MTsat)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['T1 (MTsat)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0, y=0.4,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['MTR']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['MTR']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=0, y=0.,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['MTsat']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['MTsat']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=1, y=0.79,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['FA (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['FA (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=1, y=0.4,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['MD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['MD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )
        
        fig.add_annotation(
            xref='paper',
            yref='paper',
            x=1, y=0,
            text=
            "COV<sub>intra</sub>: " 
                + str(round(stats_wm.stats_table['RD (DWI)']['intrasubject COV mean [%]'],1))
                + "% | "
            "COV<sub>inter</sub>: " 
                + str(round(stats_wm.stats_table['RD (DWI)']['intersubject mean COV [%]'],1))
                + "%",
            font = dict(
                size = self.general_font_size-3,
                color="rgb"+str(Plot.colours[0])),
            showarrow=False
            )

        fig.update_layout(height=1400, width=900)

        # Plot figureg
        if env == 'jupyter-book':
            # For jupyter-book rendering --=-- jupyter-lab
            plot(fig, filename = self.plot_name + '.html', config = config)
            display(HTML(self.plot_name + '.html'))
        elif env == 'notebook':
            # For local jupyter notebook --== binder session
            iplot(fig,config=config)

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

        # Setting option tracking variables
        FA_legend = False
        CSA_legend = False
        CSA_gm_legend = False

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

                    # Custom settings for colours
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
                    elif tissue == 'genu':
                        marker_color = "rgb"+str(Plot.colours[0])
                        legend_group = "group1"
                        name = 'Genu'
                    elif tissue == 'body':
                        marker_color = "rgb"+str(Plot.colours[3])
                        legend_group = "group2"
                        name = 'Body'
                    elif tissue == 'splenium':
                        marker_color = "rgb"+str(Plot.colours[4])
                        legend_group = "group3"
                        name = 'Splenium'
                    else:
                        marker_color = "rgb"+str(Plot.colours[0])
                        legend_group = "group1"
                        name = trace_name[metric]


                    marker_size = 6
                    row=None
                    col=None

                    if fig_id == 'paper_fig2':
                        visible=True
                        if metric == 'MP2RAGE':
                            row=1
                            col=1
                        elif metric == 'MTS':
                            row=1
                            col=2
                            showlegend=False
                        elif metric == 'MTR':
                            row=2
                            col=1
                            showlegend=False
                        elif metric == 'MTsat':
                            row=2
                            col=2
                            showlegend=False

                    if fig_id == 'paper_fig3':
                        visible=True
                        marker_size=3
                        if metric == 'DWI_FA':
                            row=1
                            col=1
                            if FA_legend==False:
                                showlegend=True
                                FA_legend=True
                            else:
                                showlegend=False
                        elif metric == 'DWI_MD':
                            row=1
                            col=2
                            showlegend=False
                        elif metric == 'DWI_RD':
                            row=1
                            col=3
                            showlegend=False

                    if fig_id == 'paper_fig5':
                        visible=True
                        showlegend=False
                        if metric == 'T1':
                            row=1
                            col=1
                        elif metric == 'MTR':
                            row=2
                            col=1
                        elif metric == 'MTSat':
                            row=3
                            col=1
                        elif metric == 'DWI_FA':
                            row=1
                            col=2
                        elif metric == 'DWI_MD':
                            row=2
                            col=2
                        elif metric == 'DWI_RD':
                            row=3
                            col=2

                    figb.add_trace(go.Scatter(x=t, 
                                                y=matrix[metric][trace], 
                                                mode='markers',
                                                marker=dict(size=marker_size),
                                                visible=visible,
                                                legendgroup=legend_group,
                                                hovertemplate = 
                                                hover_mean + 
                                                "<br>" + 
                                                "<b>%{text}</b>", 
                                                showlegend = showlegend, 
                                                text = ['Session {}'.format(i + 1) for i in range(num_sessions)],
                                                name= name,
                                                marker_color=marker_color),
                                                row=row, col=col)
            else:
                if tissue=='WM':
                    prop = 'T1w'
                    marker_color = "rgb"+str(Plot.colours[0])
                elif tissue=='GM':
                    marker_color = "rgb"+str(Plot.colours[3])
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

                    row_T1w=None
                    col_T1w=None

                    row_T2w=None
                    col_T2w=None
                    name_T1w = 'T<sub>1</sub>w'
                    if fig_id == 'paper_fig4':
                        name_T1w = 'White matter'
                        visible=True
                        marker_size=3
                        row_T1w=1
                        col_T1w=1

                        row_T2w=1
                        col_T2w=2
                        if CSA_legend==False:
                            showlegend=True
                            CSA_legend=True
                        else:
                            showlegend=False

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
                                                    name= name_T1w,
                                                    marker_color=marker_color),
                                                    row=row_T1w, col=col_T1w)
                        marker_color="rgb"+str(Plot.colours[3])
                        marker_symbol=symbols[5]
                        if fig_id == 'spine-csa-wm' or fig_id == 'paper_fig4':
                            visible = False
                            marker_color="rgb"+str(Plot.colours[0])
                            marker_symbol = 'circle'

                        if fig_id == 'paper_fig4':
                            visible = True
                            marker_color="rgb"+str(Plot.colours[0])
                            marker_symbol = 'circle'
                            if CSA_legend==False:
                                showlegend=True
                                CSA_legend=True
                            else:
                                showlegend=False

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
                                                    marker_color=marker_color),
                                                    row=row_T2w, col=col_T2w)
                    elif tissue=='GM':
                        if fig_id == 'spine-csa-gm':
                            visible = True
                            showlegend = False
                        else:
                            visible = False
                        name_T2sw= 'T<sub>2</sub><sup>*</sup>'

                        row_T2sw=None
                        col_T2sw=None
                        if fig_id == 'paper_fig4':
                            visible=True
                            marker_size=3
                            name_T2sw = 'Gray matter'
                            row_T2sw=1
                            col_T2sw=3
                            if CSA_gm_legend==False:
                                showlegend=True
                                CSA_gm_legend=True
                            else:
                                showlegend=False

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
                                                    name= name_T2sw,
                                                    marker_color=marker_color),
                                                    row=row_T2sw, col=col_T2sw)
                                       
        return figb

    def add_lines(self, figb, matrix, trace_name, tissue=None, fig_id=None, row=None, col=None):
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
                elif tissue == 'CC_1':
                    line_color = "rgb"+str(Plot.colours[0])
                    name = 'CC_1'
                elif tissue == 'MCP': 
                    line_color = "rgb"+str(Plot.colours[3])
                    name = 'MCP'
                elif tissue == 'genu':
                    line_color = "rgb"+str(Plot.colours[0])
                    name = 'Genu'
                elif tissue == 'body': 
                    line_color = "rgb"+str(Plot.colours[3])
                    name = 'Body'
                elif tissue == 'splenium': 
                    line_color = "rgb"+str(Plot.colours[4])
                    name = 'Splenium'
                else: 
                    line_color = "rgb"+str(Plot.colours[0])
                    name = trace_name[metric]

                if metric == 'MP2RAGE' or metric == 'DWI_FA':
                    visible=True
                else:
                    visible=False

                row=None
                col=None

                if fig_id == 'paper_fig2':
                    visible=True
                    if metric == 'MP2RAGE':
                        row=1
                        col=1
                    elif metric == 'MTS':
                        row=1
                        col=2
                    elif metric == 'MTR':
                        row=2
                        col=1
                    elif metric == 'MTsat':
                        row=2
                        col=2

                if fig_id == 'paper_fig3':
                    visible=True
                    if metric == 'DWI_FA':
                        row=1
                        col=1
                    elif metric == 'DWI_MD':
                        row=1
                        col=2
                    elif metric == 'DWI_RD':
                        row=1
                        col=3

                if fig_id == 'paper_fig5':
                    visible=True
                    showlegend=False
                    if metric == 'T1':
                        row=1
                        col=1
                    elif metric == 'MTR':
                        row=2
                        col=1
                    elif metric == 'MTSat':
                        row=3
                        col=1
                    elif metric == 'DWI_FA':
                        row=1
                        col=2
                    elif metric == 'DWI_MD':
                        row=2
                        col=2
                    elif metric == 'DWI_RD':
                        row=3
                        col=2

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
                                                    dash='dot')),
                                row=row,
                                col=col)
        else:
            if tissue=='WM':
                line = {
                    'T1w':{},
                    'T2w': {}
                    }
                line_color = "rgb"+str(Plot.colours[0])
            elif tissue=='GM':
                line = {
                    'GMT2w':{}
                }
                line_color = "rgb"+str(Plot.colours[3])


            for metric in trace_name:
                    
                if tissue=='WM':
                    line['T1w']= self.get_val(matrix['T1w'], 'mean')
                    line['T2w']= self.get_val(matrix['T2w'], 'mean')
                elif tissue=='GM':
                    line['GMT2w']= self.get_val(matrix['GMT2w'], 'mean')

                visible=True

                # Add dotted line
                if tissue=='WM':

                    row_T1w=None
                    col_T1w=None
                    row_T2w=None
                    col_T2w=None

                    if fig_id == 'paper_fig4':
                        visible=True
                        row_T1w=1
                        col_T1w=1

                        row_T2w=1
                        col_T2w=2

                    figb.add_trace(go.Scatter(x=x, 
                                                y=[line['T1w']]*8,
                                                mode='lines',
                                                visible=visible,
                                                name='T<sub>1</sub>w',
                                                showlegend = False,
                                                opacity=0.5, 
                                                line=dict(color=line_color, 
                                                            width=2,
                                                            dash='dot')),
                                                row=row_T1w, col=col_T1w)
                    
                    line_dict=dict(color="rgb(255, 187, 120)", width=2, dash='dot')
                    if fig_id == 'spine-csa-wm':
                        visible = False
                        line_dict=dict(color="rgb(31, 119, 180)", width=2,dash='dot')

                    if fig_id == 'paper_fig4':
                        visible = True
                        line_dict=dict(color="rgb(31, 119, 180)", width=2,dash='dot')
                    
                    figb.add_trace(go.Scatter(x=x, 
                                                y=[line['T2w']]*8,
                                                mode='lines',
                                                visible=visible,
                                                name='T<sub>2</sub>w',
                                                showlegend = False,
                                                opacity=0.5, 
                                                line=line_dict),
                                                row=row_T2w, col=col_T2w)
                if tissue=='GM':
                    row_T2sw=None
                    col_T2sw=None
                    if fig_id == 'paper_fig4':
                        visible=True
                        row_T2sw=1
                        col_T2sw=3
                    figb.add_trace(go.Scatter(x=x, 
                                                y=[line['GMT2w']]*8,
                                                mode='lines',
                                                visible=visible,
                                                name='T<sub>2</sub><sup>*</sup>',
                                                showlegend = False,
                                                opacity=0.5, 
                                                line=dict(color=line_color, 
                                                            width=2,
                                                            dash='dot')),
                                                row=row_T2sw, col=col_T2sw)


        return figb, line

    def add_std_area(self, figb, matrix, trace_name, line, tissue=None, fig_id=None, row=None, col=None):
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

                if tissue == 'WM' or tissue == 'CC_1' or tissue=='genu':
                    fillcolor='rgba(31, 119, 180, 0.15)'
                elif tissue == 'splenium': 
                    fillcolor='rgba(229, 153, 50 0.15)'
                else: 
                    fillcolor='rgba(190, 77, 80, 0.15)'

                if metric == 'MP2RAGE' or metric == 'DWI_FA':
                    visible=True
                else:
                    visible=False

                row=None
                col=None

                if fig_id == 'paper_fig2':
                    visible=True
                    if metric == 'MP2RAGE':
                        row=1
                        col=1
                    elif metric == 'MTS':
                        row=1
                        col=2
                    elif metric == 'MTR':
                        row=2
                        col=1
                    elif metric == 'MTsat':
                        row=2
                        col=2

                if fig_id == 'paper_fig3':
                    visible=True
                    if metric == 'DWI_FA':
                        row=1
                        col=1
                    elif metric == 'DWI_MD':
                        row=1
                        col=2
                    elif metric == 'DWI_RD':
                        row=1
                        col=3

                if fig_id == 'paper_fig5':
                    visible=True
                    showlegend=False
                    if metric == 'T1':
                        row=1
                        col=1
                    elif metric == 'MTR':
                        row=2
                        col=1
                    elif metric == 'MTSat':
                        row=3
                        col=1
                    elif metric == 'DWI_FA':
                        row=1
                        col=2
                    elif metric == 'DWI_MD':
                        row=2
                        col=2
                    elif metric == 'DWI_RD':
                        row=3
                        col=2

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
                ),
                row=row,
                col=col)
        
        else:
            if tissue=='WM':
                std_area = {
                    'T1w':{},
                    'T2w': {}
                    }
                color=list(Plot.colours[0])
                color.append(0.15)
                fillcolor = "rgba"+str(tuple(color))
            elif tissue=='GM':
                std_area = {
                    'GMT2w':{}
                    }
                color=list(Plot.colours[3])
                color.append(0.15)
                fillcolor = "rgba"+str(tuple(color))

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
                fillcolor = fillcolor

                # Add STD
                if tissue=='WM':

                    row_T1w=None
                    col_T1w=None
                    row_T2w=None
                    col_T2w=None

                    if fig_id == 'paper_fig4':
                        visible=True
                        row_T1w=1
                        col_T1w=1

                        row_T2w=1
                        col_T2w=2
                    figb.add_trace(go.Scatter(
                        x=x+x[::-1],
                        y=[line['T1w']+std_area['T1w']]*8+[line['T1w']-std_area['T1w']]*8,
                        fill='toself',
                        visible=visible,
                        fillcolor=fillcolor,
                        line_color='rgba(255,255,255,0)',
                        showlegend=False,
                        hoverinfo=self.hoverinfo,
                        name='T<sub>1</sub>w STD'
                    ),
                    row=row_T1w, col=col_T1w)

                    fillcolor=fillcolor
                    if fig_id == 'spine-csa-wm':
                        visible = False
                        fillcolor=fillcolor

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
                    ),
                    row=row_T2w, col=col_T2w)

                if tissue=='GM':
                    row_T2sw=None
                    col_T2sw=None
                    if fig_id == 'paper_fig4':
                        visible=True
                        row_T2sw=1
                        col_T2sw=3
                    figb.add_trace(go.Scatter(
                        x=x+x[::-1],
                        y=[line['GMT2w']+std_area['GMT2w']]*8+[line['GMT2w']-std_area['GMT2w']]*8,
                        fill='toself',
                        visible=visible,
                        fillcolor=fillcolor,
                        line_color='rgba(255,255,255,0)',
                        showlegend=False,
                        hoverinfo=self.hoverinfo,
                        name='T<sub>2</sub><sup>*</sup> STD'
                    ),
                    row=row_T2sw, col=col_T2sw)

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
            if len(tissues)==2:
                yaxis_range = [self.get_val(np.append(matrix[tissues[0]][metric], matrix[tissues[1]][metric], axis=0), 'min'), self.get_val(np.append(matrix[tissues[0]][metric], matrix[tissues[1]][metric], axis=0), 'max')]
            elif len(tissues)==3:
                pre_concat = np.append(matrix[tissues[0]][metric], matrix[tissues[1]][metric], axis=0)
                yaxis_range = [self.get_val(np.append(pre_concat, matrix[tissues[2]][metric], axis=0), 'min'), self.get_val(np.append(pre_concat, matrix[tissues[2]][metric], axis=0), 'max')]
        else:
            yaxis_range = [self.get_val(matrix[metric], 'min'), self.get_val(matrix[metric], 'max')]
        if metric=='T1w' or metric=='T2w':
            yaxis_range = [40,100]
        if metric=='DWI_MD' or metric=='DWI_RD':
            return {"yaxis": dict(
                    range = yaxis_range,
                    title=title,
                    mirror=True,
                    ticks='outside', 
                    tickformat='s',
                    showline=True, 
                    linecolor='#000',
                    tickfont = dict(size=self.y_label_tick_font_size)
                    )
                }
        else:
            return {"yaxis": dict(
                    range = yaxis_range,
                    title=title,
                    mirror=True,
                    ticks='outside', 
                    ticklayout='f',
                    showline=True, 
                    linecolor='#000',
                    tickfont = dict(size=self.y_label_tick_font_size)
                    )
                }
