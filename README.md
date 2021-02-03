This is a thresholding+inpainting toolkit for astronomic photometric images. The different scripts allow for the identification of ROI in photometric images using an Otsu thresholding and different interpolation schemes for the filling of the masked ROI based on bilinear interpolation and patch-based inpainting techniques.

![Comparision](https://github.com/jctdrs/background/tree/assets/images/out.jpg?raw=True)

##### Usage
1. `ROI_GEN.py` is an interactive background thresholder used to identify the region of interest (ROI) in the image. This ROI will be masked for background interpolation. The file name is loaded through the `-fn` argument:
  - `-fn` file name
  `ROI_GEN.py` will create different directories and store the original image, ROI, mask, and masked image as well as .npy versions under an`RIO_0` directory for future use. The thresholding can be interactively manipulated through the `left-right` and `up-down` arrows to increment/decrement the ROI with small/large steps as well as through both `A` and `B` keys for smoothing/desmoothing. For more information on the Otsu thresholding mechanism checkout https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=4310076

<p float='center'>
  <img src="https://github.com/jctdrs/background/tree/assets/images/ROI_GEN.gif?raw=True" width="276" height="276">
  <img src="https://github.com/jctdrs/background/tree/assets/images/ROI_GEN_2.gif?raw=True" width="276" height="276">
</p>

2. `interpolate.py` is a basic linear interpolation scheme. At each pixel the background is linearly interpolated in the four main directions based on the mean of its four neighboring pixels. The background is interpolated from the boundary inwards in an onion-layer manner. The file name and version are loaded through both the `-fn`, `-roi` arguments:
  - `-fn` file name
  - `-roi` version of the image
`interpolate.py` will also create different directories and store the image and mask as well as the position of the target patch at each iteration for future use. The version of the image masking the source is `0` by default, other versions are designated for the masking of other parts of the image using the `ROI_SYN.py` script. 

<p float='center'>
  <img src="https://github.com/jctdrs/background/tree/assets/images/Crab_int.gif?raw=True" width="276" height="276">
  <img src="https://github.com/jctdrs/background/tree/assets/images/eye_int.gif?raw=True" width="276" height="276">
</p>

3. `inpaint.py` is a patch-based image inpainting interpolation scheme. For the details of the algorithm check https://www.irisa.fr/vista/Papers/2004_ip_criminisi.pdf. The file name, roi version, hpw, and selection option are loaded through the `-fn`, `-roi`, `-hpw`, and `-select` arguments. If `-select 1` the user gets to choose the area of the image to pick patches from for the inpainting, if `-select 0` then the whole image is included. The select option is usually useful when the inpainting takes alot of time due to the image being big. 
  - `-fn` file name
  - `-roi` roi version of the image
  - `-hpw` half-patch width (default set to 4)
  - `-select` 1 or 0  (default set to 0)

`inpaint.py` will also create different directories and store the image and mask as well as the position of the taret patch at each iteration for future use.

<p float='center'>
  <img src="https://github.com/jctdrs/background/tree/assets/images/Crab_inp.gif?raw=True" width="276" height="276">
  <img src="/https://github.com/jctdrs/background/tree/assets/images/imageseye_inp.gif?raw=True" width="276" height="276">
</p>

4. `ROI_SYN.py` is an ROI synthesizer which takes the Otsu-thresholded ROI and create a similar mask in a different part of the image. The new position of the mask is chosen interactively using the mouse. This would create a repository with roi version numbering `roi` which can then be linearily interpolated or inpainted using the scripts. The image is identified using the `-fn` arguments. 

<p float='center'>
  <img src = "https://github.com/jctdrs/background/tree/assets/images/crab_syn.gif?raw=True" width="276" height="276">
</p>
