# Python imports 
from pathlib import Path
from IPython.core.display import display, HTML
import numpy as np
import pandas as pd
from tools.data import Data

class Stats:
    """Stats handling class

    Class objects load Data object and generate statistics.

    """

    def __init__(self, dataset):
        """Initialize object
        
        Input: 
            - dataset (Data class object)
            - plot_name (ID for plot, HTML filename)

        """

        self.dataset = dataset

        # Get number of subjects and sessions
        self.num_subjects = self.dataset.num_subjects
        self.num_sessions = self.dataset.num_sessions

        # Get database
        if self.dataset.data_type == 'brain':
            self.database = {
                'WM': [],
                'GM': []
            }
            self.database['WM'] = self.dataset.extract_data('WM', default_val=np.nan)
            self.database['GM'] = self.dataset.extract_data('GM',default_val=np.nan)
        elif self.dataset.data_type == 'brain-diffusion':
            self.database = {
                'CC_1': [],
                'MCP': []
            }
            self.database['CC_1'] = self.dataset.extract_data('CC_1', default_val=np.nan)
            self.database['MCP'] = self.dataset.extract_data('MCP',default_val=np.nan)
        else:
            self.database = self.dataset.extract_data(default_val=np.nan)
        
        # Database to table name conversion
        self.database2table = {
            'MP2RAGE': 'T1 (MP2RAGE)',
            'MTS': 'T1 (MTsat)',
            'MTR': 'MTR',
            'MTsat': 'MTsat',
            'DWI_FA': 'FA (DWI)',
            'DWI_MD': 'MD (DWI)',
            'DWI_RD': 'RD (DWI)',
            'MTSat': 'MTsat',
            'T1': 'T1 (MTsat)',
            'T1w':  'WM area (T1w)',
            'T2w': 'WM area (T2w)',
            'GMT2w': 'GM area (T2w)'
        }
        

    def build_df(self, tissue = None):
        df = pd.DataFrame.from_dict(self.database)

        if tissue is not None:
            self.df = df[tissue]
        else:
            self.df = df

    def  build_stats_table(self):
        metrics = self.df.keys()
        columns = []
        col_vals = []
        for metric in metrics:
            columns.append(self.database2table[metric])
            col_vals.append(None)
        
        df_setup = {
            'intrasubject COV mean [%]': col_vals,
            'intrasubject COV std [%]': col_vals,
            'intersubject mean COV [%]': col_vals,
            }
        
        self.stats_table = pd.DataFrame.from_dict(df_setup, orient='index', columns=columns)
        breakpoint()
        for metric in metrics:
            if 'WM' in self.database.keys() or 'CC_1' in self.database.keys():
                intrasub_cov = np.divide(np.nanstd(self.df[metric], axis=1), np.nanmean(self.df[metric], axis=1)) * 100
                self.stats_table[self.database2table[metric]]['intrasubject COV mean [%]'] = np.mean(intrasub_cov)
                self.stats_table[self.database2table[metric]]['intrasubject COV std [%]'] = np.std(intrasub_cov)

                intrasub_mean = np.nanmean(self.df[metric], axis=1)
                self.stats_table[self.database2table[metric]]['intersubject mean COV [%]'] = np.divide(np.std(intrasub_mean),np.mean(intrasub_mean)) * 100
            else:
                intrasub_cov = np.divide(np.nanstd(self.df[metric].tolist(), axis=1), np.nanmean(self.df[metric].tolist(), axis=1)) * 100
                self.stats_table[self.database2table[metric]]['intrasubject COV mean [%]'] = np.mean(intrasub_cov)
                self.stats_table[self.database2table[metric]]['intrasubject COV std [%]'] = np.std(intrasub_cov)

                intrasub_mean = np.nanmean(self.df[metric].tolist(), axis=1)
                self.stats_table[self.database2table[metric]]['intersubject mean COV [%]'] = np.divide(np.std(intrasub_mean),np.mean(intrasub_mean)) * 100
