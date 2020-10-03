##### Usage 
1.`ROI_GEN.py` is an interactive Otsu thresholder to identify the ROI
  - inputs: -fn `fits file name`, -mode `otsu` for OTSU thresholding or `rect` for rectangular ROI
2.`ROI_SYN.py` is a tool to localize ROI in different locations of the image
  - inputs: -fn `fits file name`, -mode `otsu` for OTSU thresholding or `rect` for rectagular ROI
3.`interpolate.py` interpolates the ROI using cross-averaging
  - inputs: -fn `fits file name`, -mode `otsu` for OTSU thresholding or `rect` for rectangular ROI, -v `version of the ROI`
4.`biinterpolate.py` interpolates bilinearly 
  - inputs: -fn `fits file name`, -v `version of the ROI`
5.`inpaint.py` interpolates using patch-based inpainting 
  - inputs -fn `fits file name`, -v `version of the ROI`, -hpw `half patch width`, -select `1 for region selection. 0 for all image`, -mode `otsu` for OTSU or `rect` for rectangular ROI
