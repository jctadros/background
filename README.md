This is a thresholding+inpainting toolkit for astronomic photometric images. The different scripts allow for the identification of ROI in photometric images using an Otsu thresholding and different interpolation schemes for the filling of the masked ROI based on bilinear interpolation and patch-based inpainting techniques based on Criminisi et. al (2005) https://www.irisa.fr/vista/Papers/2004_ip_criminisi.pdf 

![Comparision](/images/out.jpg)
<img align="right" src="images/ROI_GEN.gif" width="276" height="276">


##### Usage
1. `ROI_GEN.py` is an interactive background thresholder used to identify the region of interest (ROI) in the image. This ROI will be masked for background interpolation. Two modes are available through the `-mode` argument:
  - `-mode otsu` for an interactive Otsu thresholder.
  - `-mode rect` for a rectangular ROI.

N.B: run with otsu mode before rect mode as the rectangular mask will be centered around the Otsu-generated ROI.

`python ROI_GEN.py -fn [file name] -mode [mode]`
