This is a thresholding+inpainting toolkit for astronomic photometric images. The different scripts allow for the identification of ROI in photometric images using an Otsu thresholding and different interpolation schemes for the filling of the masked ROI based on bilinear interpolation and patch-based inpainting techniques based on Criminisi et. al (2005) https://www.irisa.fr/vista/Papers/2004_ip_criminisi.pdf 

![Comparision](/images/out.jpg)

##### Usage
1. `ROI_GEN.py` is an interactive background thresholder used to identify the region of interest (ROI) in the image. This ROI will be masked for background interpolation. Two modes are available through the `-mode` argument:
  - `-mode otsu` for an interactive Otsu thresholder.
  - `-mode rect` for a rectangular ROI.
  `ROI_GEN.py` will create different directories and store the original imag    e, ROI, mask, and masked image as well as .npy versions under an`RIO_0` dire    ctory for future use. The thresholding can be interactively manipulated thro    ugh the `left-right` and (`up-down`) arrows to increment/decrement the ROI w    ith small (large) steps as well as both `A` and `B` keys for smoothing and d    esmoothing of the ROI. For more information on the Otsu thresholding mechani    sm checkout https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4310076

N.B: run with otsu mode before rect mode as the rectangular mask will be centered   around the Otsu-generated ROI.

<p float='center'>
  <img src="/images/ROI_GEN.gif" width="276" height="276">
  <img src="/images/ROI_GEN_2.gif" width="276" height="276">
</p>



2. `interpolate.py` is a basic linear interpolation scheme. At each pixel the background is linearly interpolated in the four main directions based on the mean of its four neighboring pixels. The background is interpolated from the boundary inwards in an onion-layer way. The image to interpolate needs to be identified using the `-fn`, `-mode`, and `-v` arguments:
  - `-fn` file name
  - `-mode` otsu or rect
  - `-v` version of the image

`interpolate.py` will also create different directories and store the image and mask as well as the position of the target patch at each iteration for future use or analysis. The version of the image masking the source is `0` by default, other versions are designated for the masking of other parts of the image using the `ROI_SYN.py` script. 

<p float='center'>
  <img src="/images/Crab_int.gif" width="276" height="276">
  <img src="/images/eye_int.gif" width="276" height="276">
</p>
