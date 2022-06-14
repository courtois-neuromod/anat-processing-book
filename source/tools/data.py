import subprocess
from pathlib import Path
import pandas as pd

class Data:
    
    datasets = {
        'brain': {
            'version_list': ['r20210726'],
            'filename': 'neuromod-anat-brain-qmri.zip',
            'data_files': "results-neuromod-anat-brain-qmri.csv"
        },
        'spine': {
            'version_list': ['r20210610'],
            'filename': 'spinalcord_results.zip',
            'data_files': {
                'T1w': 'csa-SC_T1w.csv',
                'T2w': 'csa-SC_T2w.csv',
                'GMT2w': 'csa-GM_T2s.csv'
            },
        },
        'qmri':{
            'version_list': ['r20210610'],
            'filename': 'spinalcord_results.zip',
            'data_files': {
                'DWI_FA': 'DWI_FA.csv',
                'DWI_MD': 'DWI_MD.csv',
                'DWI_RD': 'DWI_RD.csv',
                'MTR': 'MTR.csv',
                'MTSat': 'MTsat.csv',
                'T1': 'T1.csv'
            },
        },
        'url': 'https://github.com/courtois-neuromod/anat-processing/releases/download/'
    }
    
    def __init__(self, data_type):
        self.data_type = data_type
        self.available_versions = self.get_available_versions()
        self.version = None
        self.release_file = None
        self.data_dir = None
        self.data = None

    def get_available_versions(self):
        version_list = Data.datasets[self.data_type]['version_list']
        version_list.sort()
        return version_list
    
    def download(self, release_version):

        # Set release version
        if release_version == 'latest':
            self.version = self.available_versions[-1]
        elif release_version in self.available_versions:
            self.version = release_version
        else:
            Exception('Release version not listed in available versions. Please update requested version and restart.')

        # Get release file name
        release_file = Data.datasets[self.data_type]['filename']

        # Get release global url
        global_url = Data.datasets['url']

        # Set release-specific url
        url = global_url + "/" + self.version + "/" + release_file

        # Set output directory
        self.data_dir = Path('data') / Path(self.data_type)

        # Download
        if self.data_dir.exists() is False:
            # Create directory
            subprocess.run(["mkdir", "-p", self.data_dir])

            # Get data from GitHub release and extract
            subprocess.run(["wget", "-O", release_file, url])
            subprocess.run(["unzip", "-j", release_file,  "-d", self.data_dir])
    
    def load(self):

        data_type = self.data_type

        if data_type == 'brain':
            data_file = Data.datasets[data_type]['data_files']
            file_path = self.data_dir / data_file

            # Read data
            self.data = pd.read_csv(file_path, converters={'project_id': lambda x: str(x)})

            # Sort data acording to subject and session columns 
            self.data.sort_values(['subject', 'session'], ascending=[True, True]) 

        elif data_type == 'spine':
            
            # Prep data property
            self.data = {
                'T1w': None,
                'T2w': None,
                'GMT2w': None
            }

            for acq in self.data:

                data_file = Data.datasets[data_type]['data_files'][acq]

                file_path = self.data_dir / data_file

                # Load  the data
                self.data[acq] = pd.read_csv(file_path, converters={'project_id': lambda x: str(x)})

                # Insert new columns for Subject and Session and start inserting values
                self.data[acq].insert(0, "Subject", "Any")
                self.data[acq].insert(1, "Session", "Any")

                # Get Subject and Session from csv
                for index, row in self.data[acq].iterrows():
                    subject = int(row['Filename'].split("/")[6].split('-')[1])
                    session = int(row['Filename'].split("/")[7].split("-")[1])
                    self.data[acq].at[index, 'Subject'] =  subject
                    self.data[acq].at[index, 'Session'] =  session

                # Sort values based on Subject -- Session
                self.data[acq]=self.data[acq].sort_values(['Subject', 'Session'], ascending=[True, True])

        elif data_type == 'qmri':
            self.data = {
                'DWI_FA': None,
                'DWI_MD': None,
                'DWI_RD': None,
                'MTR': None,
                'MTSat': None,
                'T1': None
            }


            for acq in self.data:

                data_file = Data.datasets[data_type]['data_files'][acq]

                file_path = self.data_dir / data_file

                # Load  the data
                self.data[acq] = pd.read_csv(file_path, converters={'project_id': lambda x: str(x)})

                # Insert new columns for Subject and Session and start inserting values
                self.data[acq].insert(0, "Subject", "Any")
                self.data[acq].insert(1, "Session", "Any")

                # Get Subject and Session from csv
                for index, row in self.data[acq].iterrows():
                    subject = int(row['Filename'].split("/")[6].split('-')[1])
                    session = int(row['Filename'].split("/")[7].split("-")[1])
                    self.data[acq].at[index, 'Subject'] =  subject
                    self.data[acq].at[index, 'Session'] =  session

                # Sort values based on Subject -- Session
                self.data[acq]=self.data[acq].sort_values(['Subject', 'Session'], ascending=[True, True])


    def extract_data(self, tissue):
        num_sub = 6
        num_session = 4
        if self.data_type == 'brain':
            matrix = {
                'MP2RAGE': [],
                'MTS': [],
                'MTR': [],
                'MTsat': []
            }
        elif self.data_type == 'spine':
            matrix = {
                'T1w':  [],
                'T2w': [],
                'GMT2w': []
            }
        elif self.data_type == 'qmri':
            matrix = {
                'DWI_FA': [],
                'DWI_MD': [],
                'DWI_RD': [],
                'MTR': [],
                'MTSat': [],
                'T1': []
                }

        default_val = -100

        if self.data_type == 'brain':
            for metric in matrix:
                for i in range(1, num_sub+1, 1):
                    sub_values = self.data.loc[self.data['subject'] == i]

                    metric_ses = []

                    for j in range(1, num_session+1, 1):
                        ses_values = sub_values.loc[sub_values['session'] == j]
                        
                        mean_val = default_val

                        for index, row in ses_values.iterrows():

                            if metric == 'MP2RAGE' or metric == 'MTS':
                                if row['acquisition'] == metric and row['metric'] == 'T1map' and row['label'] == tissue:
                                    mean_val = row['mean']
                            elif metric == 'MTR':
                                if row['metric'] == 'MTRmap' and row['label'] == tissue: 
                                    mean_val = row['mean']
                            elif metric == 'MTsat':
                                if row['metric'] == 'MTsat' and row['label'] == tissue:
                                    mean_val = row['mean']

                        # Append values to lists for sessions
                        metric_ses.append(mean_val)
                    
                    matrix[metric].append(metric_ses)
        elif self.data_type == 'spine':
            
            for type in matrix:

                db = self.data[type]
                
                for i in range(1, num_sub+1, 1):
                    sub_values = db.loc[db['Subject'] == i]

                    metric_ses = []

                    for j in range(1, num_session+1, 1):
                        ses_values = sub_values.loc[sub_values['Session'] == j]
                        
                        mean_val = default_val
                            
                        for index, row in ses_values.iterrows():
                            mean_val = row['MEAN(area)']

                        # Append values to lists for sessions
                        metric_ses.append(mean_val)
                        
                    matrix[type].append(metric_ses)

        elif self.data_type == 'qmri':

            for metric in matrix:
                for i in range(1, num_sub+1, 1):
                    sub_values = self.data[metric].loc[self.data[metric]['Subject'] == i]

                    metric_ses = []

                    for j in range(1, num_session+1, 1):
                        ses_values = sub_values.loc[sub_values['Session'] == j]
                        
                        mean_val = default_val

                        for index, row in ses_values.iterrows():

                            val = row['WA()']

                        # Append values to lists for sessions
                        metric_ses.append(val)
                    
                    matrix[metric].append(metric_ses)

        return matrix