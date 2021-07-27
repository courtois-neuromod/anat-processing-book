# anat-processing-book

Notebook that describes processing of anatomical data for the [Courtois-Neuromod Project](https://www.cneuromod.ca/). 

To visualize the notebook click [here](https://courtois-neuromod.github.io/anat-processing-book/intro.html).

## Build the Notebook locally

Install miniconda

Create and activate virtual environment:
~~~
conda create -n notebook_docs pip
conda activate notebook_docs
~~~

Install required packages
~~~
pip install -r requirements.txt
~~~

Build the notebook
~~~
jupyter-book build
~~~
