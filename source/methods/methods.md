# Material and Methods

## Participants

X healthy participants were recruited. Study was IRB XXX.

## Data acquisition

Structural MRI consisted of the following sequences:
- 

For more details on the sequence parameters, please see the [full protocol](). 

## Data processing

The software requirements include:
- Nextflow and Docker for brain data analysis
- SCT for spinal cord data analysis

The repository containing the code and instructions to reproduce this analysis is available at: https://github.com/courtois-neuromod/anat-processing.

In brief, brain analysis consisted in:
- co-registering MT0 and MT1 data,
- Resampling the B1+ map to the space of the MT data,
- Masking tissue outside the brain using FSL BET [REF], 
- Smooth B1+ maps,
- Compute MTR and MTsat,
- Compute T1 using the MP2RAGE data.

Spinal cord analysis consisted in:
- From the T2w image: 
  - Segment the spinal cord on the T2w image,
  - Label vertebrae on the T2w image,
  - Register the T2w spinal cord to the PAM50 template,
  - Warp template without the white matter atlas (we don't need it at this point)
  - Generate QC report to assess vertebral labeling
  - Compute average cord CSA between C2 and C3
- From the T1w image:
  - Segment the spinal cord
  - Bring vertebral level into T1w space
  - Compute average cord CSA between C2 and C3
- From the MT data:
  - Segment spinal cord
  - Create mask around the cord
  - Crop data for faster processing
  - Register the MT0 to the T1w image
  - Register the MT1 to the T1w image
  - Register the PAM50 template to the T1w image (using the template->T1w warping field as initial transformation)
  - Warp the PAM50 template objects
  - Compute MTR and MTsat
  - Extract MTR, MTsat and T1 in the white matter between C2 and C5 vertebral levels
- From the T2*w data:
  - Bring vertebral level into T2s space
  - Segment gray matter
  - Compute the gray matter CSA between C3 and C4 levels. 
- From the DWI data:
  - Separate b=0 and DW images
  - Automatically find the spinal cord centerline
  - Create a mask around the spinal cord  to help motion correction and for faster processing
  - Perform motion correction
  - Segment the spinal cord on the mean DWI image
  - Register the PAM50 template to the mean DWI image (using the template->T1w warping field as initial transformation)
  - Warp the PAM50 template objects
  - Create a mask around the spinal cord (for faster computing)
  - Compute DTI (powered by Dipy [REF])
  - Compute FA, MD and RD in WM between C2 and C5 vertebral levels
