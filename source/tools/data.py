import subprocess
from pathlib import Path
import pandas as pd
import numpy as np

class Data:
    """Data handling class

    Class objects can download data, loads it, and can be passed
    onto a Plot object to display the data using Plotly.

    """

    datasets = {
        'brain': {
            'version_list': ['r20210726', 'b20220804', 'r20220813', 'r20220916', 'r20220921'],
            'filename': 'neuromod-anat-brain-qmri.zip',
            'data_files': "results-neuromod-anat-brain-qmri.csv"
        },
        'brain-diffusion': {
            'version_list': ['r20220921b'],
            'filename': 'brain-diffusion-arnaud.zip',
            'data_files': "mean_std.json"
        },
        'spine': {
            'version_list': ['r20220623', 'r20220804'],
            'filename': 'spinalcord_results.zip',
            'data_files': {
                'T1w': 'csa-SC_T1w.csv',
                'T2w': 'csa-SC_T2w.csv',
                'GMT2w': 'csa-GM_T2s.csv'
            },
        },
        'qmri':{
            'version_list': ['r20220623', 'r20220804'],
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
        'url': 'https://github.com/courtois-neuromod/anat-processing/releases/download'
    }

    # [sub, ses, metric]
    qc_exclude = [
        ['qmri', 3, 10, 'T1w'],
        ['qmri', 4, 5, 'T1w'],
        ['qmri', 5, 7, 'T2w'],
        ['qmri', 2, 1, 'DWI_FA'], ['qmri', 2, 1, 'DWI_MD'], ['qmri', 2, 1, 'DWI_RD'],
        ['qmri', 3, 3, 'DWI_FA'], ['qmri', 3, 3, 'DWI_MD'], ['qmri', 3, 3, 'DWI_RD'],
        ['qmri', 6, 8, 'DWI_FA'], ['qmri', 6, 8, 'DWI_MD'], ['qmri', 6, 8, 'DWI_RD']
    ]
    
    def __init__(self, data_type):
        """Initialize object
        
        Input: data_type (brain, spine, qmri)

        """

        self.data_type = data_type
        self.available_versions = self.get_available_versions()
        self.version = None
        self.release_file = None
        self.data_dir = None
        self.data = None
        self.num_subjects = None
        self.num_sessions = None

    def get_available_versions(self):
        """Get available data versions

        Returns list of available dataset versions for the data_type 
        that the object was initalized with.

        """

        version_list = Data.datasets[self.data_type]['version_list']
        version_list.sort()
        return version_list
    
    def download(self, release_version):
        """Download dataset

        Downloads the dataset specified by the selected release version.

        """

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
        """Load dataset into the object

        Loads the dataset into the object as a pandas dataframe.
        Sorts it by subject and session number.

        """

        data_type = self.data_type

        if data_type == 'brain':
            data_file = Data.datasets[data_type]['data_files']
            file_path = self.data_dir / data_file

            # Read data
            self.data = pd.read_csv(file_path, converters={'project_id': lambda x: str(x)})

            # Sort data acording to subject and session columns 
            self.data.sort_values(['subject', 'session'], ascending=[True, True]) 
        elif data_type == 'brain-diffusion':
            data_file = Data.datasets[data_type]['data_files']
            file_path = self.data_dir / data_file

            # Read data
            json_data = pd.read_json(file_path)

            df = pd.DataFrame(columns=['subject', 'session', 'acquisition', 'metric', 'label', 'mean', 'std'])
            metrics = ['fa_metric', 'md_metric', 'rd_metric']

            for sub_ses in json_data.keys():
                tmp = sub_ses.split('_')

                sub = int(tmp[0].split('-')[1])
                ses = int(tmp[1].split('-')[1])
                for tract in json_data[sub_ses].keys():
                    for metric in metrics:

                        if type(json_data[sub_ses][tract]) is dict:
                            mean_val = json_data[sub_ses][tract][metric]['mean']
                            std_val = json_data[sub_ses][tract][metric]['std']
                            df = df.append(
                                {
                                    'subject': sub,
                                    'session': ses,
                                    'acquisition': 'dwi',
                                    'metric': metric,
                                    'label': tract,
                                    'mean': mean_val,
                                    'std': std_val
                                },
                                ignore_index=True
                            )
                        else:
                            df = df.append(
                                {
                                    'subject': sub,
                                    'session': ses,
                                    'acquisition': 'dti',
                                    'metric': metric,
                                    'label': tract,
                                    'mean': np.nan,
                                    'std': np.nan
                                },
                                ignore_index=True
                            )

            self.data = df

            # Sort data acording to subject and session columns 
            self.data=self.data.sort_values(['subject', 'session'], ascending=[True, True]) 
        else:
            if data_type == 'spine':
                # Prep data property
                self.data = {
                    'T1w': None,
                    'T2w': None,
                    'GMT2w': None
                }
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
                self.data[acq].insert(0, "subject", "Any")
                self.data[acq].insert(1, "session", "Any")

                # Get Subject and Session from csv
                for index, row in self.data[acq].iterrows():
                    subject = int(next((x for x in row['Filename'].split("/") if 'sub' in x), None).split('-')[1])
                    session = int(next((x for x in row['Filename'].split("/") if 'ses' in x), None).split('-')[1])
                    self.data[acq].at[index, 'subject'] =  subject
                    self.data[acq].at[index, 'session'] =  session

                # Sort values based on Subject -- Session
                self.data[acq]=self.data[acq].sort_values(['subject', 'session'], ascending=[True, True])
    
        num_subjects, num_sessions = self.set_num_subjects_sessions()

        self.num_subjects = num_subjects
        self.num_sessions = num_sessions

    def set_num_subjects_sessions(self):
        """Set the number of subjects and number of sessions in the loaded dataset

        Goes through each metric and finds the maximum number of subjects and sessions acquired, and
        sets it to the object.

        """

        subject_array = []
        session_array = []

        if self.data_type == 'brain' or self.data_type == 'brain-diffusion':
            subject_array.append(max(self.data['subject']))
            session_array.append(max(self.data['session']))
        else:
            for key in self.data:
                subject_array.append(max(self.data[key]['subject']))
                session_array.append(max(self.data[key]['session']))
        
        num_subjects = max(subject_array)
        num_sessions = max(session_array)

        return num_subjects, num_sessions


    def extract_data(self, tissue=None, default_val = -100):
        """Extract data

        Extract the metrics from the pandas datafram into a matrix format fo all
        subjects and sessions. For the brain dataset, tissue must be selected.

        """
        
        num_sub = self.num_subjects
        num_session = self.num_sessions

        if self.data_type == 'brain':
            matrix = {
                'MP2RAGE': [],
                'MTS': [],
                'MTR': [],
                'MTsat': []
            }
        elif self.data_type == 'brain-diffusion':
            matrix = {
                'DWI_FA': [],
                'DWI_MD': [],
                'DWI_RD': []
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

        for metric in matrix:
            for i in range(1, num_sub+1, 1):
                if self.data_type == 'brain' or self.data_type == 'brain-diffusion':
                    sub_values = self.data.loc[self.data['subject'] == i]
                else:
                    sub_values = self.data[metric].loc[self.data[metric]['subject'] == i]

                metric_ses = []

                for j in range(1, num_session+1, 1):
                    ses_values = sub_values.loc[sub_values['session'] == j]
                    
                    mean_val = default_val

                    if [self.data_type, i, j, metric] not in self.qc_exclude:
                        for index, row in ses_values.iterrows():
                            
                            if self.data_type == 'qmri':
                                mean_val = row['WA()']
                            elif self.data_type == 'spine':
                                mean_val = row['MEAN(area)']
                            elif metric == 'MP2RAGE' or metric == 'MTS':
                                if row['acquisition'] == metric and row['metric'] == 'T1map' and row['label'] == tissue:
                                    mean_val = row['mean']
                            elif metric == 'MTR':
                                if row['metric'] == 'MTRmap' and row['label'] == tissue: 
                                    mean_val = row['mean']
                            elif metric == 'MTsat':
                                if row['metric'] == 'MTsat' and row['label'] == tissue:
                                    mean_val = row['mean']
                            elif metric == 'DWI_FA':
                                if row['metric'] == 'fa_metric' and row['label'] == tissue:
                                    mean_val = row['mean']
                            elif metric == 'DWI_MD':
                                if row['metric'] == 'md_metric' and row['label'] == tissue:
                                    mean_val = row['mean']
                            elif metric == 'DWI_RD':
                                if row['metric'] == 'rd_metric' and row['label'] == tissue:
                                    mean_val = row['mean']

                            if np.isnan(mean_val):
                                mean_val = default_val

                        # Append values to lists for sessions
                        metric_ses.append(mean_val)
                    else:
                        metric_ses.append(default_val)
         
                matrix[metric].append(metric_ses)

        return matrix
