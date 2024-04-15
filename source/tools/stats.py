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
        elif self.dataset.data_type == 'brain-diffusion-cc':
            self.database = {
                'genu': [],
                'body': [],
                'splenium': []
            }
            self.database['genu'] = self.dataset.extract_data('genu', default_val=np.nan)
            self.database['body'] = self.dataset.extract_data('body',default_val=np.nan)
            self.database['splenium'] = self.dataset.extract_data('splenium',default_val=np.nan)
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
            'GMT2w': 'GM area (T2s)'
        }
        

    def build_df(self, tissue = None):
        df = pd.DataFrame.from_dict(self.database)

        if tissue is not None:
            self.df = df[tissue]
        else:
            self.df = df

    def ICC(self, metric):
        
        if 'WM' in self.database.keys() or 'CC_1' in self.database.keys() or 'genu' in self.database.keys():
            df = self.df[metric]
        else:
            df = self.df[metric].to_list()

        num_subjects = len(df)

        ICC = np.zeros(6)

        subjectVariance = np.zeros(6) # Array of variance within each subject
        subjectMeans = np.zeros(6) # Array of mean within each subject

        wsVariance = None # within-subject variance (i.e. mean of subjectVariance)
        bsVariance = None # between-subject variance (i.e. variance of subjectMeans)

        # wsVariance
        for idx, subject in enumerate(df):
            subject_data =  np.array([x for x in subject if str(x) != 'nan'])
            
            num_sessions = len(subject_data)
            subjectMeans[idx] = np.mean(subject_data)
            
            subjectVariance[idx] = np.divide(np.sum(np.square(subject_data-subjectMeans[idx])), (num_sessions-1))
        
        wsVariance = np.mean(subjectVariance)

        # wsVariance
        grandMean = np.nanmean(df)

        bsVariance =  np.divide(np.sum(np.square(subjectMeans-grandMean)), (num_subjects-1))

        # ICC (intraclass correlation coefficient)

        ICC = np.divide(np.square(bsVariance), (np.square(bsVariance) + np.square(wsVariance)))

        ## COVs

        # wsVariance
        subjectCOVs = np.zeros(6)
        for idx, subject in enumerate(subjectVariance):
            subjectCOVs[idx] = np.sqrt(subjectVariance[idx])/subjectMeans[idx]

        wsCOV = np.mean(subjectCOVs) * 100

        #bsVariance
        bsCOV = np.std(subjectMeans)/grandMean * 100

        return ICC, wsCOV, bsCOV

    def build_stats_table(self):
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
            'ICC': col_vals,
            'wsCOV': col_vals,
            'bsCOV': col_vals
            }
        
        self.stats_table = pd.DataFrame.from_dict(df_setup, orient='index', columns=columns)

        for metric in metrics:
            if 'WM' in self.database.keys() or 'CC_1' in self.database.keys() or 'genu' in self.database.keys():
                intrasub_cov = np.divide(np.nanstd(self.df[metric], axis=1), np.nanmean(self.df[metric], axis=1)) * 100
                self.stats_table[self.database2table[metric]]['intrasubject COV mean [%]'] = np.mean(intrasub_cov)
                self.stats_table[self.database2table[metric]]['intrasubject COV std [%]'] = np.std(intrasub_cov)

                intrasub_mean = np.nanmean(self.df[metric], axis=1)
                self.stats_table[self.database2table[metric]]['intersubject mean COV [%]'] = np.divide(np.std(intrasub_mean),np.mean(intrasub_mean)) * 100

                ICC, wsCOV, bsCOV = self.ICC(metric)
                self.stats_table[self.database2table[metric]]['ICC'] = ICC
                self.stats_table[self.database2table[metric]]['wsCOV'] = wsCOV
                self.stats_table[self.database2table[metric]]['bsCOV'] = bsCOV

            else:
                intrasub_cov = np.divide(np.nanstd(self.df[metric].tolist(), axis=1), np.nanmean(self.df[metric].tolist(), axis=1)) * 100
                self.stats_table[self.database2table[metric]]['intrasubject COV mean [%]'] = np.mean(intrasub_cov)
                self.stats_table[self.database2table[metric]]['intrasubject COV std [%]'] = np.std(intrasub_cov)

                intrasub_mean = np.nanmean(self.df[metric].tolist(), axis=1)
                self.stats_table[self.database2table[metric]]['intersubject mean COV [%]'] = np.divide(np.std(intrasub_mean),np.mean(intrasub_mean)) * 100

                ICC, wsCOV, bsCOV = self.ICC(metric)
                self.stats_table[self.database2table[metric]]['ICC'] = ICC
                self.stats_table[self.database2table[metric]]['wsCOV'] = wsCOV
                self.stats_table[self.database2table[metric]]['bsCOV'] = bsCOV

    def calc_loa(self, metric1, metric2):
    # Calculate the limit of agreement
        data_metric1 = np.array(self.df[metric1]).flatten()
        data_metric2 = np.array(self.df[metric2]).flatten()

        data_metric1 = data_metric1[~np.isnan(data_metric1)]
        data_metric2 = data_metric2[~np.isnan(data_metric2)]

        assert len(data_metric1)==len(data_metric2)

        difference = np.subtract(data_metric1, data_metric2)

        mean = np.mean(difference)

        std = np.std(difference)

        loa =  1.96*std

        return mean, loa

