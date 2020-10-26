This is a thresholding+inpainting toolkit for astronomic photometric images. The different scripts allow for the identification of ROI in photometric images using an Otsu thresholding and different interpolation schemes for the filling of the masked ROI based on bilinear interpolation and patch-based inpainting techniques based on Criminisi et. al (2005) https://www.irisa.fr/vista/Papers/2004_ip_criminisi.pdf 

![Comparision](/images/out.jpg)
<img align='right' src="images/ROI_GEN.gif" width="276" height="276">

##### Usage
1. `ROI_GEN.py` is an interactive background thresholder used to identify the region of interest (ROI) in the image. This ROI will be masked for background interpolation. Two modes are available through the `-mode` argument:
  - `-mode otsu` for an interactive Otsu thresholder.
  - `-mode rect` for a rectangular ROI.

  N.B: run with otsu mode before rect mode as the rectangular mask will be centered   around the Otsu-generated ROI.

<img align='right' src='images/ROI_GEN_2.gif' width='276' height='276'>

  `python ROI_GEN.py -fn [file name] -mode [mode]`

  `ROI_GEN.py` will create different directories and store the original image, ROI, mask, and masked image as well as .npy versions under an`RIO_0` directory for future use. The thresholding can be interactively manipulated through the `left-right` and (`up-down`) arrows to increment/decrement the ROI with small (large) steps as well as both `A` and `B` keys for smoothing and desmoothing of the ROI. For more information on the Otsu thresholding mechanism checkout https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4310076
