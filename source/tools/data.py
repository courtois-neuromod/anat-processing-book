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
                'T2w': 'csa-SC_T2w.csv'
            }
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
                'T2w': None
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
                self.data[acq].sort_values(['Subject', 'Session'], ascending=[True, True])
