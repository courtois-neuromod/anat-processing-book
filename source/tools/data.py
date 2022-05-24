import subprocess
from pathlib import Path

class Data:
    
    datasets = {
        'brain': {
            'version_list': ['r20210726'],
            'filename': 'neuromod-anat-brain-qmri.zip'
        },
        'spine': {
            'version_list': ['r20210610'],
            'filename': 'spinalcord_results.zip'
        },
        'url': 'https://github.com/courtois-neuromod/anat-processing/releases/download/'
    }
    
    def __init__(self, data_type):
        self.data_type = data_type
        self.available_versions = self.get_available_versions()
        self.version = None
        self.release_file = None

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
        dir = Path('data') / Path(self.data_type)

        # Download
        if dir.exists() is False:
            # Create directory
            subprocess.run(["mkdir", "-p", dir])

            # Get data from GitHub release and extract
            subprocess.run(["wget", "-O", release_file, url])
            subprocess.run(["unzip", "-j", release_file,  "-d", dir])
        
