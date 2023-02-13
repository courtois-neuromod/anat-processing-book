# Introduction 

Conventional MRI images used in clinics come from the MRI machine being used as a non-invasive medical device, not a scientific instrument. These images need interpretation by expert readers as they lack specificity and reproducibility. Quantitative MRI (qMRI) aims to produce measurements of biological or physical properties by using conventional MRI images. The calculated or fit maps from these images have values with physical units, such as T1 or T2 relaxation times, myelin water fraction, magnetization transfer ratio, and cerebral blood flow. qMRI has high specificity to biological changes and in principle should have improved stability compared to clinical MRI. However, many of these qMRI techniques are currently not used routinely in clinics. One of the main reason is that data processing is long and tedious, as illustrated in he figure below below.

![Screen Shot 2021-07-26 at 9 59 18 PM](https://user-images.githubusercontent.com/2482071/127083234-6efd2c7a-352b-4ee0-81d9-9c278f4caf01.png)
<font size="2"><i>Illustration of a typical qMRI processing pipeline. The "start" and "finish" images are modified from the comics _Piled Higher and Deeper_ by Jorge Gabriel Cham. </i></font>

The qMRI field has fallen short of this promised standardization, with fundamental qMRI techniques outputs varying among methods and sites. Efforts have been made to improve accuracy and stability, such as through the use of calibration phantoms and integrating qMRI pulse sequences into commercial scanners.

Importantly, quantitative MRI measurement stability is crucial for designing longitudinal studies, especially when clinical features change over time. It is also important to determine the expected variability to estimate the minimum detectable effect size in a power analysis. Same-day test-retest studies have shown low intra-scanner variability for fundamental quantitative MRI metrics (T1, T2) at around 1-2%. However, these studies have limitations and do not reflect the conditions in longitudinal studies. Longitudinal stability is important to quantify, but can be challenging due to changes in the subject's tissue properties over time. Quantitative MRI metrics have been shown to correlate with aging, but changes occur slowly over decades. Thus, short-term longitudinal studies (3-5 years) should provide reliable longitudinal stability measurements.

## Objectives

The objective of the work presented in this Jupyter Book is two-fold:
- Measure and report the stability of quantitative microstructure MRI measurements across multiple time points in the brain and cervical spinal cord. 
- Develop reproducible and reusable analysis pipelines for structural qMRI of the brain and spinal cord.

To achieve these objectives, two sets of quantitative MRI protocols (brain and spinal cord) were integrated within the Courtois project on neural modelling (CNeuroMod), which aims to collect longitudinal data on healthy subjects to train and improve artificial intelligence models on brain behaviour and activity. The quantitative MRI measurements of the brain and spinal cord fell within the “anatomical” imaging branch of the CNeuroMod project, and additional branches of data acquired include deep scanning with functional MRI, biosignals (eg, cardiac, respiration, eye tracking), and magnetoencephalography (MEG).

In addition, pipeline were built using state-of-the-art tools in terms of pipeline management (NextFlow), structural data analyses (FSL, ANTs, qMRLab, SCT, etc.) and Jupyter notebooks with Plotly for presenting curated and interactive results in a companion Jupyter Book.

