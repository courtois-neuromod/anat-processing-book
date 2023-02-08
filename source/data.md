# Data Availability Statement

In the aim of better reproducibility and transparency in research, all the data, processing pipelines, containers, and analysis code have been made available online.

The anonymized and defaced datasets are in BIDS format and managed using Datalad and git-annex in a GitHub repository, https://github.com/courtois-neuromod/anat, and the data itself is hosted on an Amazon Web Services (AWS) server. To request access to this data, we invite researchers to fill out an application form on our website https://www.cneuromod.ca/access/access/.

The brain quantitative MRI processing pipeline was written in Nextflow (brain) and shell (spine) and are available in this repository: https://github.com/courtois-neuromod/anat-processing.


The qMRI brain pipeline used two Docker containers which have been made available as saved container images on Dockerhub:  dockerhub.io/qmrlab/antsfl:latest (digest: 597de3e6e1aa, https://hub.docker.com/repository/docker/qmrlab/antsfsl)) and dockerhub.io/qmrlab/minimal:​​v2.5.0b (digest: 40270330e7b5, https://hub.docker.com/repository/docker/qmrlab/minimal)). 

The TractoFlow pipeline is built using open-source tools and is available on GitHub: https://github.com/scilus/tractoflow.

The condensed outputs of these pipelines (eg, masked and averaged values for each tissue) are shared in GitHub releases of this repository, which can be found here: https://github.com/courtois-neuromod/anat-processing/releases/.

The data figures and tables in this article were produced using analysis code integrated in an interative Jupyter Book and powered by Plotly, which is available here, https://courtois-neuromod.github.io/anat-processing-book/, and the code repository for this book is https://github.com/courtois-neuromod/anat-processing-book.