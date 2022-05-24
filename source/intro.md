# Introduction 

## Context

Magnetic resonance imaging (MRI) comes with different flavours-- or as physicists would call it: pulse sequences. A pulse sequence is a bit like a musical orchestra. There are different instruments and each play at a particular time and with a particular pitch (frequency) and amplitude. In an MRI pulse sequence, the instruments are the hardware (gradients, RF controller, antenna, etc.). By driving the orchestra in a smart way, we can obtain more than a pretty picture of the inside body. In fact, we can obtain numbers that reflect the state of the tissue microstructure. For example, if there is a demyelinating lesion in multiple sclerosis, some sequences would enable to quantify the amount of demyelination. These particular sequences fall under the umbrella term _Quantitative MRI_, or qMRI. 

MRI data acquired with a special pulse sequence are then analyzed. The analysis includes complex processing such as image non-linear registration, filtering and noise removal. Then, a biophysical model is usually fitted to the data, in order to extract physically meaningful parameters such as the density of neuronal cells, the orientation of white matter fibers or the relative concentration of brain metabolites. Given its important applications in the diagnosis and prognosis of traumas, neurological diseases and cancers, qMRI offers lots of promises and has become extremely popular in the neuroscience and pharmaceutical research community. 

However, many of these qMRI techniques are currently not used routinely in clinics. One of the main reason is that data processing is long and tedious, as illustrated in Figure XX. 

![Screen Shot 2021-07-26 at 9 59 18 PM](https://user-images.githubusercontent.com/2482071/127083234-6efd2c7a-352b-4ee0-81d9-9c278f4caf01.png)
_Figure XX. Illustration of a typical qMRI processing pipeline. The "start" and "finish" images are modified from the comics _Piled Higher and Deeper_ by Jorge Gabriel Cham._ 

Also, quantitative MRI data require complex analysis pipelines that are often executed manually and hence suffer from poor reproducibility. By being popular and requiring multiple high-level expertise at the same time, the field of qMRI is also cursed with an increasing amount of studies that other researchers have hard time reproducing [https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1002506, https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.27939]. A good resource illustrating this reproducibility crisis is the recent special issue about "Reproducibility in Neuroimaging" in the highly-respected NeuroImage journal (https://www.sciencedirect.com/journal/neuroimage/special-issue/102ML28LZ8W). It has become clear that in order to properly use of qMRI, the neuroimaging community has to educate and promote transparent acquisition and analysis tools. 

In this context, the Courtois Neuromod project is an excellent opportunity to promote open-science while also contributing to neuromaging research.
While the Courtois Neuromod project is particularly focused on decyphering functional networks in the brain by using functional MRI and deep neural networks [REF], a branch of this project also includes the longitudinal follow-up of healthy participants via anatomical sequences that are sensitive to tissue microstructure, in both the brain and the cervical spinal cord. 

## Objectives

The objective of this study is two-fold:
- Develop an open-source pipeline for fully-automatic analysis pipeline of structural qMRI of the brain and spinal cord. Importantly, this pipeline is built using state-of-the-art tools in terms of pipeline management (NextFlow), structural data analyses (FSL, ANTs, qMRLab, SCT, etc.) and Jupyter notebook for presenting curated and interactive results in the present Jupyter book. 
- Study the stability of morphometric and microstructure measurements from qMRI measured across multiple time points in the brain and cervical spinal cord. 

